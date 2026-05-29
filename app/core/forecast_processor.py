import asyncio
from pprint import pprint
from .data.api_query import get_query
from .data.ideal_values import IDEAL,IMPORTANCE
from .schemas.fish_schemas import BiteForecastIdeal
import math
from datetime import datetime
import httpx
from geopy.geocoders import Nominatim


class BiteForecastManager:


	def __init__(self,client:httpx.AsyncClient,geolocator:Nominatim):

		self.asyncclient = client
		self.geolocator = geolocator


	async def get_data_from_api(self,lat,lon,typeReservoir):

		response = await self.asyncclient.post('/graphql/query',
			json={'query': 
					get_query(lat=lat,lon=lon)})

		data = response.json()

		try:
			location_obj = await self.geolocator.reverse(f"{lat},{lon}")
			location = location_obj.address if location_obj else 'Неизвестно'
		except:
			location = 'Неизвестно'

		data['point'] = {
            'lat': lat,
            'lon': lon,
            'typeReservoir': typeReservoir,
            'location':location
        }   

		return data


	def calc_weight_distribution_gauss(self,valueMin,valueMax,current,tolerance_min,tolerance_max) -> float:
	# формула гаусса без нормативного коэффициента
		if (valueMin <= current <= valueMax):

			return 1.0

		elif (current < valueMin):

			sigma_min = tolerance_min / 2.4477
			return math.exp(-((current - valueMin) ** 2) / (2 * (sigma_min ** 2)))

		else:

			sigma_max = tolerance_max / 2.4477
			return math.exp(-((current - valueMax) ** 2) / (2 * (sigma_max ** 2)))


	def calc_data(self,metric:dict) -> dict:

		forecast = BiteForecastIdeal(fish = IDEAL)
		hour = metric['data']['weatherByPoint']['forecast']['days'][0]['hours']
		day = metric['data']['weatherByPoint']['forecast']['days'][0]
		

		weight_dict_result: dict[str, dict] = {}

		for key, values in forecast.fish.items():

			moon_phase_weight = self.calc_weight_penalty(day['moonPhase'],values.moon_phase_optimal,values.moon_phase_penalty)
			weight_dict_result.setdefault(key, {})
			weight_dict_result[key]['meta'] = {

					'point':metric['point'],
					'moon_phase_weight': moon_phase_weight,
					'sunrise': day['sunrise'],
					'sunset': day['sunset']
				}

			i = 0
			while i <= 12:

				temperature_weight = self.calc_weight_distribution_gauss(values.temperature.min,
												values.temperature.max,
												hour[i]['temperature'],
												values.temperature.tolerance_min,
												values.temperature.tolerance_max)


				pressure_weight = self.calc_weight_distribution_gauss(values.pressure.min,
												values.pressure.max,
												hour[i]['pressure'],
												values.pressure.tolerance_min,
												values.pressure.tolerance_max)
				
				windSpeed_weight = self.calc_weight_distribution_gauss(values.windSpeed.min,
												values.windSpeed.max,
												hour[i]['windSpeed'],
												values.windSpeed.tolerance_min,
												values.windSpeed.tolerance_max)
				
				ideal_center = (values.windAngle.min + values.windAngle.max) / 2
				diffAngle = self.get_shortest_angle_distance(hour[i]['windAngle'],ideal_center)
				max_deviation = values.windAngle.max - ideal_center

				windAngle_weight = self.calc_weight_distribution_gauss(
												valueMin=0,                                 
												valueMax=max_deviation,                      
												current=diffAngle,                           
												tolerance_min=0,                             
												tolerance_max=values.windAngle.tolerance_max 
												)

				humidity_weight = self.calc_weight_distribution_gauss(values.humidity.min,
												values.humidity.max,
												hour[i]['humidity'],
												values.humidity.tolerance_min,
												values.humidity.tolerance_max)

				prec_weight = self.calc_weight_distribution_gauss(values.prec.min,
												values.prec.max,
												hour[i]['prec'],
												values.prec.tolerance_min,
												values.prec.tolerance_max)

				time_weight = self.calc_best_time_of_day(hour[i]['time'],values.timeOfDay.hour,values.timeOfDay.weights) 
				cloudiness_weight = self.calc_weight_penalty(hour[i]['cloudiness'],values.cloudiness_optimal,values.cloudiness_penalty)
				prec_type_weight = self.calc_weight_penalty(hour[i]['precType'],values.prec_type_optimal,values.prec_type_penalty)

				weight_dict_result.setdefault(key,{})
				weight_dict_result[key].setdefault('hourly',{}) 
				weight_dict_result[key]['hourly'][i] = {

					'time_weight':time_weight,
					'datetime': hour[i]['time'],
					'temperature_weight': temperature_weight,
					'pressure_weight': pressure_weight,
					'windSpeed_weight': windSpeed_weight,
					'windAngle_weight': windAngle_weight,
					'cloudiness_weight': cloudiness_weight,
					'humidity_weight':humidity_weight,
					'prec_weight':prec_weight,
					'prec_type_weight': prec_type_weight,

					'raw_pressure': hour[i]['pressure'],
					'raw_temperature':hour[i]['temperature'],
					'raw_windSpeed':hour[i]['windSpeed'],

				}

				i += 1

		return self.score_weight(weight_dict_result,forecast)		


	def calc_weight_penalty(self,values,data: list, penalty: float) -> float:
		if values in data:
			return 1.0
		else:
			return 1.0 - penalty


	def calc_best_time_of_day(self,time,data_hour:dict,data_weight:dict):
		dt = datetime.fromisoformat(time)
		hour = dt.hour
		if hour in data_hour['best_hours']:
			return data_weight['best']
		elif hour in data_hour['good_hours']:
			return data_weight['good']
		elif hour in data_hour['bad_hours']:
			return data_weight['bad']
		elif hour in data_hour['terrible_hours']:
			return data_weight['terrible']

	def get_shortest_angle_distance(self, current_angle: float, ideal_angle: float) -> float:

		diff = abs(current_angle - ideal_angle)

		if diff > 180:
			diff = 360 - diff
			
		return diff
	
	def score_weight(self,result:dict,forecast:BiteForecastIdeal) -> dict:
		for fish, data in result.items():

			hourly_dict = data['hourly']

			for hour, hour_data in data['hourly'].items():
				weighted_sum = 0.0
				total_weight = 0.0

				past_index = max(0, int(hour) - 3)
				past_value = hourly_dict.get(str(past_index)) or hourly_dict.get(int(past_index))
				
				if past_value is None:
					pressure_trends,windSpeed_trends,temperature_trends = 1.0,1.0,1.0
				else:
					pressure_trends,windSpeed_trends,temperature_trends = self.calc_dynamic_delta(
							abs(hour_data['raw_pressure'] - past_value['raw_pressure']),
							hour_data['raw_windSpeed'] - past_value['raw_windSpeed'],
							abs(hour_data['raw_temperature'] - past_value['raw_temperature']),
							forecast,
							fish
					)
				hour_data['pressure_trends'] = pressure_trends
				hour_data['windSpeed_trends'] = windSpeed_trends
				hour_data['temperature_trends'] = temperature_trends


				for key,imp in IMPORTANCE.items():
					val = hour_data.get(key)
					if val is not None:
						if key == 'pressure_weight':
							val *= hour_data['pressure_trends']
						elif key == 'windSpeed_weight':
							val *= hour_data['windSpeed_trends']
						elif key == 'temperature_weight':
							val *= hour_data['temperature_trends']

						weighted_sum += val*imp
						total_weight += imp

				hour_data['score'] = round((weighted_sum/total_weight),2)
		return result


	def calc_dynamic_delta(self,pressure_delta:float,windSpeed_delta:float,temperature_delta:float,forecast:BiteForecastIdeal,fish_index:str) -> float:
		
		fish_config = forecast.fish[fish_index]

		if pressure_delta <= 1.0:
			press_trend = 1.0
		elif pressure_delta <= fish_config.treands.pressure_max_delta:
			press_trend = 1.0 - fish_config.treands.pressure_penalty
		else:
			press_trend = fish_config.treands.bitekiller_pressure

		if temperature_delta <= 2.0:
			temp_trend = 1.0    
		elif temperature_delta <= fish_config.treands.temp_max_delta:
			temp_trend = 1.0 - fish_config.treands.temp_penalty  
		else:
			temp_trend = fish_config.treands.bitekiller_temp   

		if windSpeed_delta > fish_config.treands.wind_max_delta:
			wind_trend = 1.0 - fish_config.treands.wind_penalty
		else:
			wind_trend = 1.0


		return press_trend,wind_trend,temp_trend
	
