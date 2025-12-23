from fastapi import FastAPI
from Auth.auth_controller import router as auth_router

app = FastAPI(
    title="Tiffinly Auth Service"
)

#include routes from auth routers
app.include_router(auth_router)


