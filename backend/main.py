from datetime import datetime

from config.settings import settings
from controlers.controlers import (
    get_measurement_query,
    get_raw_data_controler,
    get_summary_controler,
)
from controlers.enums import SpanValues
from database.db import database, session
from database.model import Measurements
from fastapi import FastAPI

app = FastAPI(settings=settings)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    session.close()
    await database.disconnect()


@app.get("/api/ingest")
async def ingest():
    status = Measurements.ingest()
    return {"ingestion status": status}


@app.get("/api/summary")
async def summary(
    datalogger: str,
    since: str = "",
    before: str = datetime.now().isoformat(),
    span: SpanValues = SpanValues.RAW,
):
    """Array of records matching the input criteria."""
    formated_queryset, reframed_since, reframed_before = get_measurement_query(
        datalogger, since, before, span
    )

    if len(formated_queryset) == 0:
        return []

    return get_summary_controler(formated_queryset, reframed_since, reframed_before)


@app.get("/api/data")
async def data(
    datalogger: str,
    since: str = "",
    before: str = datetime.now().isoformat(),
):
    """Array of records matching the input criteria. DataRecordResponse schema"""
    formated_queryset, reframed_since, reframed_before = get_measurement_query(
        datalogger, since, before, span=SpanValues.RAW
    )

    if len(formated_queryset) == 0:
        return []

    return get_raw_data_controler(formated_queryset)
