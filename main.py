from dotenv import load_dotenv
load_dotenv("healthcare-platform/.env")

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from financial_health_router import router
from ai_core.routers import chat, intake, recommend

app = FastAPI(title="MedNoviAI AI Service")
app.include_router(router)
app.include_router(chat.router)
app.include_router(intake.router)
app.include_router(recommend.router)


@app.get("/")
def home():
    return JSONResponse({
        "service": "MedNoviAI AI Service",
        "message": "Financial Health Score API is mounted.",
        "route": "/api/ai/financial-health/{user_id}",
    })


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return JSONResponse(status_code=204, content=None)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
