from fastapi import  Request
from geopy.geocoders import Nominatim
from ..core.data.weatherAdapter import WeaherAdaper
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

def get_weather_adapter(request:Request) -> WeaherAdaper:

	return request.app.state.weather_adapter

def get_geolocator(request:Request) -> Nominatim:

	return request.app.state.geolocator

async def get_db_session(request:Request) -> AsyncGenerator[AsyncSession,None]:

	async with request.app.state.db_session_factory() as session:
	
		yield session
