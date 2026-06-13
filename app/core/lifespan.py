from fastapi import FastAPI
from contextlib import asynccontextmanager
from geopy.geocoders import Nominatim
from geopy.adapters import AioHTTPAdapter
from .data.weatherAdapter import YandexWeather
import httpx
from ..database.db import engine,async_session_factory,init_models


@asynccontextmanager
async def lifespan(app: FastAPI):

	
	app.state.httpClient = httpx.AsyncClient()

	app.state.weather_adapter = YandexWeather(http_client = app.state.httpClient) 

	app.state.geolocator = Nominatim(user_agent="biteforecast",adapter_factory=AioHTTPAdapter)

	try:
		await init_models()
	except Exception as e:

		raise e


	app.state.db_session_factory = async_session_factory

	yield

	await app.state.httpClient.aclose()
	await engine.dispose()