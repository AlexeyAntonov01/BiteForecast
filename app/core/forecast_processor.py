import asyncio
from pprint import pprint
from .data.api_query import get_query
from .data.ideal_values import IDEAL,IMPORTANCE
from .schemas.fish_schemas import BiteForecastIdeal
import math
from datetime import datetime



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

				windAngle_weight = self.calc_weight_distribution_gauss(values.windAngle.min,
												values.windAngle.max,
												hour[i]['windAngle'],
												values.windAngle.tolerance_min,
												values.windAngle.tolerance_max)

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

				}

				i += 1

		return self.score_weight(weight_dict_result)		


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


	def score_weight(self,result:dict) -> dict:


		for fish, data in result.items():

			for hour, hour_data in data['hourly'].items():

				weighted_sum = 0.0
				total_weight = 0.0

				for key,imp in IMPORTANCE.items():

					val = hour_data.get(key)

					weighted_sum += val*imp
					total_weight += imp

				hour_data['score'] = round((weighted_sum/total_weight),2)


		return result
