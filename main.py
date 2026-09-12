from fastapi import FastAPI
from fastapi.responses import JSONResponse
from financial_health_router import router
from src.errors import register_exception_handlers
from src.financial_assistant.spending_pattern_router import router as spending_router

app = FastAPI(title="MedNoviAI AI Service")
register_exception_handlers(app)
app.include_router(router)
app.include_router(spending_router)


@app.get("/")
def home():
    return JSONResponse({
        "service": "MedNoviAI AI Service",
        "message": "Financial Health Score API is mounted.",
        "route": "/api/ai/financial-health/{user_id}",
    })


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    from fastapi import Response
    return Response(status_code=204)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
