from fastapi import FastAPI,Request,Depends
from .api.endpoints import router,get_data_result
from .api.dependencies import get_BiteForecastManager
from .core.lifespan import lifespan
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI(lifespan=lifespan)
app.include_router(router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def table_dash(
    request: Request,
    lat: float = 62.00695,       
    lon: float = 50.54664,       
    typeReservoir: str = "Река",
    manager = Depends(get_BiteForecastManager)
):

    result_data = await get_data_result(
        lat=lat, 
        lon=lon, 
        typeReservoir=typeReservoir, 
        manager=manager
    )

    return templates.TemplateResponse(
        request=request,
        name="biteForecast.html", 
        context={"forecast": result_data}
    )

