from fastapi import FastAPI,Request,Depends
from .api.endpoints import router,get_data_result
from .core.lifespan import lifespan
from .core.forecast_processor import BiteForecastManager
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .api.dependencies import get_weather_adapter,get_geolocator


app = FastAPI(lifespan=lifespan)
app.include_router(router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def table_dash(
    request: Request,
    lat: float = 55.99684,       
    lon: float = 37.58011,       
    typeReservoir: str = "Река",
    weather_adapter = Depends(get_weather_adapter),
    geolocator = Depends(get_geolocator)
    ):

    result_data = await get_data_result(
        lat=lat, 
        lon=lon, 
        typeReservoir=typeReservoir,
        weather_adapter=weather_adapter,
        geolocator=geolocator
        )

    return templates.TemplateResponse(
        request=request,
        name="biteForecast.html", 
        context={"forecast": result_data}
    )

