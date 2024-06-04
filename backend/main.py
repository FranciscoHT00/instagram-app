from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from routers import user
import models


app = FastAPI()
app.include_router(user.router)


@app.get("/", include_in_schema=False)
async def documentacion():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run("main:app",port=8000,reload=True)