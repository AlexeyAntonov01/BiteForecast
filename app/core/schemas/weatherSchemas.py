from pydantic import BaseModel, Field
from typing import Dict,List,Optional,Union
from datetime import datetime


class HourIndicators(BaseModel):

	time: datetime
	temperature: float
	pressure: float
	prec: float
	precType: str
	precStrength: str
	cloudiness: Union[str,float]
	windSpeed: float
	windGust: Optional[float] = None
	windAngle: Optional[float] = None
	humidity: float


class DayIndicators(BaseModel):

	moonPhase: str
	sunrise: str
	sunset: str
	hours: List[HourIndicators]


class WeatherSchema(BaseModel):

	season: str
	location: Optional[str] = None
	point: Optional[dict] = None
	precProbability: Optional[float] = None
	data:DayIndicators
