from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from routers import user, instagram, concursos, publicaciones
import models
from contextlib import asynccontextmanager
import httpx

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with httpx.AsyncClient() as client:
        yield {'client': client}

app = FastAPI(lifespan=lifespan)
app.include_router(user.router)
app.include_router(instagram.router)
app.include_router(concursos.router)
app.include_router(publicaciones.router)

@app.get("/", include_in_schema=False)
async def documentacion():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run("main:app",port=8000,reload=True)