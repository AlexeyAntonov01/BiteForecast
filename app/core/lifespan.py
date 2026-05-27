from fastapi import FastAPI
from contextlib import asynccontextmanager
from geopy.geocoders import Nominatim
from geopy.adapters import AioHTTPAdapter  
import asyncio
from dotenv import load_dotenv
import os
import httpx

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):


	api_key = os.getenv("API_KEY")
	headers = {'X-Yandex-Weather-Key': api_key}
	
	app.state.httpClient = httpx.AsyncClient(
			base_url='https://api.weather.yandex.ru',
			headers=headers
		)

	app.state.geolocator = Nominatim(user_agent="biteforecast",adapter_factory=AioHTTPAdapter)

	yield

	app.state.httpClient.aclose()