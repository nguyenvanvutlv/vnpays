import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware

from api import __version__
from api import create_payment_route



load_dotenv()

def create_application() -> FastAPI:
    application = FastAPI(
        title = "VNPAY API",
        description = "VNPAY",
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(create_payment_route, prefix=f"/api/{__version__}")
    return application


app = create_application()
if __name__ == "__main__":
    
    uvicorn.run(app)