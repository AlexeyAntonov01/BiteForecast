from fastapi import FastAPI
from .api.endpoints import router
from .core.lifespan import lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(router)
