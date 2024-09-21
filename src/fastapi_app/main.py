from fastapi import FastAPI

from src.fastapi_app.api.endpoints import router

app = FastAPI()

app.include_router(router=router)