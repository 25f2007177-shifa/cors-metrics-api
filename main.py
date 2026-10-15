import time
import uuid

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware

EMAIL = "25f2007177@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-jziksm.example.com"

app = FastAPI()

# Permit only the assigned frontend origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# This middleware adds headers to normal responses and CORS preflight responses.
@app.middleware("http")
async def add_request_headers(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = max(0.0, time.perf_counter() - start)

    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{elapsed:.6f}"
    return response


@app.get("/stats")
async def stats(values: str = Query(...)):
    try:
        numbers = [int(value.strip()) for value in values.split(",")]
        if not numbers or any(value.strip() == "" for value in values.split(",")):
            raise ValueError
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="values must be comma-separated integers",
        )

    total = sum(numbers)

    return {
        "email": EMAIL,
        "count": len(numbers),
        "sum": total,
        "min": min(numbers),
        "max": max(numbers),
        "mean": total / len(numbers),
    }
