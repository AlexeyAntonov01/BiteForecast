from fastapi import FastAPI
from contextlib import asynccontextmanager
from geopy.geocoders import Nominatim
from geopy.adapters import AioHTTPAdapter
from .data.weatherAdapter import YandexWeather
import os
import httpx


@asynccontextmanager
async def lifespan(app: FastAPI):

	
	app.state.httpClient = httpx.AsyncClient()

	app.state.weather_adapter = YandexWeather(http_client = app.state.httpClient) 

	app.state.geolocator = Nominatim(user_agent="biteforecast",adapter_factory=AioHTTPAdapter)

	yield

	await app.state.httpClient.aclose()