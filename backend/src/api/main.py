from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import (
    snapshots,
    kpis,
    churn,
    clv,
    segmentation,
    retention,
)

app = FastAPI(title="Customer Intelligence Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(snapshots.router)
app.include_router(kpis.router)
app.include_router(churn.router)
app.include_router(clv.router)
app.include_router(segmentation.router)
app.include_router(retention.router)