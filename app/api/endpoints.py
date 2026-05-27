from fastapi import APIRouter, Depends
from .dependencies import get_BiteForecastManager
import asyncio


router = APIRouter()


@router.get("/get_result_data_score")
async def get_data_result(lat:float,lon:float,typeReservoir:str,manager=Depends(get_BiteForecastManager)):

	response = await manager.get_data_from_api(lat,lon,typeReservoir)

	loop = asyncio.get_running_loop()

	def calc():

		return manager.calc_data(response)


	result = await loop.run_in_executor(None,calc)

	return result




