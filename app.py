import sys

from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from routing.v1.main import router as main_router

from configs.Environment import get_environment_variables


app = FastAPI(openapi_url="/core/openapi.json", docs_url="/core/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)

env = get_environment_variables()

if not env.DEBUG:
    logger.remove()
    logger.add(sys.stdout, level="INFO")
