from fastapi import APIRouter, Depends
from app.core.forecast_processor import BiteForecastManager
from .dependencies import get_weather_adapter, get_geolocator
import asyncio
from geopy.geocoders import Nominatim

router = APIRouter()


@router.get("/get_result_data_score")
async def get_data_result(
				lat:float,
				lon:float,
				typeReservoir:str,
				weather_adapter = Depends(get_weather_adapter),
				geolocator = Depends(get_geolocator)
				):

	response = await weather_adapter.get_weather(lat,lon)

	try:
		location_obj = await geolocator.reverse(f"{lat},{lon}")
		location = location_obj.address if location_obj else 'Неизвестно'
	except:
		location = 'Неизвестно'

	response.location = location


	response.point = {
	    'lat': lat,
	    'lon': lon,
	    'typeReservoir': typeReservoir,
	    'location': location
	}

	loop = asyncio.get_running_loop()

	def calc():

		manager = BiteForecastManager() 
		return manager.calc_data(response)


	result = await loop.run_in_executor(None,calc)

	return result




