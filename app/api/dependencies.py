from fastapi import  Request
from geopy.geocoders import Nominatim


def get_weather_adapter(request:Request) -> WeaherAdaper:

	return request.app.state.weather_adapter

def get_geolocator(request:Request) -> Nominatim:

	return request.app.state.geolocator

