from fastapi import FastAPI,Request,Depends
from ..schemas.weatherSchemas import WeatherSchema
import abc
import os
from .api_query import get_query
from dotenv import load_dotenv

load_dotenv()

class WeaherAdaper(abc.ABC):

	@abc.abstractmethod
	async def get_weather(self,lat,lon):
		pass


class YandexWeather(WeaherAdaper):

	def __init__(self,http_client):

		self.http_client = http_client
		self.api_key = os.getenv("API_KEY")
		self.headers = {'X-Yandex-Weather-Key': self.api_key}
		self.url = 'https://api.weather.yandex.ru/graphql/query'
	

	async def get_weather(self,lat,lon):

		response = await self.http_client.post(self.url,
					headers=self.headers,
					json={'query': 
					get_query(lat=lat,lon=lon)})

		if response.status_code != 200:
			response.raise_for_status()
			return 'Ошибка при получении данных!'


		raw = response.json()
		day_data = raw['data']['weatherByPoint']['forecast']['days'][0]
		
		return WeatherSchema(data=day_data,season=raw['data']['weatherByPoint']['now']['season'],precProbability=raw['data']['weatherByPoint']['now']['precProbability'])











