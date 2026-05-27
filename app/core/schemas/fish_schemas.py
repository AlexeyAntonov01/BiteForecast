from pydantic import BaseModel, Field
from typing import Dict,List

class MeteorologicalDataRanges(BaseModel):

	min: float
	max: float
	tolerance_min: float | int
	tolerance_max: float | int


class TimeOfDayConfig(BaseModel):

	hour: Dict[str,List[int]]
	weights: Dict[str,float]


class WeatherParameters(BaseModel):

	temperature: MeteorologicalDataRanges
	pressure: MeteorologicalDataRanges
	windSpeed: MeteorologicalDataRanges
	windAngle: MeteorologicalDataRanges
	humidity: MeteorologicalDataRanges
	prec: MeteorologicalDataRanges

	cloudiness_optimal: List[str]
	cloudiness_penalty: float

	prec_type_optimal: List[str]
	prec_type_penalty: float

	moon_phase_optimal: List[str]
	moon_phase_penalty: float

	timeOfDay:TimeOfDayConfig


class BiteForecastIdeal(BaseModel):

	fish: Dict[str,WeatherParameters]





