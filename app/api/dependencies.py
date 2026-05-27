from fastapi import  Request
from app.core.forecast_processor import BiteForecastManager


def get_BiteForecastManager(request:Request) -> BiteForecastManager:

	client = request.app.state.httpClient
	geolocator = request.app.state.geolocator

	return BiteForecastManager(client=client,geolocator=geolocator)