from datetime import datetime, timedelta
from typing import Union

import numpy
from controlers.enums import LabelField, SpanValues
from database.db import session
from database.model import Measurements


def reframe_since_date_with_span(before: str, span: SpanValues) -> datetime:
    """reframe dates in function of the span param if egal day or hour"""
    date_frame = timedelta(days=0)
    date_before = datetime.fromisoformat(before)

    if span == SpanValues.DAY:
        date_frame = timedelta(days=1)

    if span == SpanValues.HOUR:
        date_frame = timedelta(hours=1)

    return date_before - date_frame


def get_measurement_query(
    datalogger: str, since: str, before: str, span: SpanValues
) -> tuple[list, datetime | str, str]:
    """make queryset with the right time frame from api filters
    params: api filters
    returns: queryset, since, before
    """
    reframed_since = since

    if span == SpanValues.DAY or span == SpanValues.HOUR:
        reframed_since = reframe_since_date_with_span(before, span)

    if span == SpanValues.MAX:
        reframed_since = ""

    if reframed_since == "":
        queryset = (
            session.query(Measurements)
            .filter(Measurements.id == datalogger)
            .filter(Measurements.date <= before)
        )
    else:
        queryset = (
            session.query(Measurements)
            .filter(Measurements.id == datalogger)
            .filter(Measurements.date <= before)
            .filter(Measurements.date >= reframed_since)
        )
    formated_queryset = [row.to_dict() for row in queryset]
    return formated_queryset, reframed_since, before


def get_summary_controler(
    serialized_queryset: list[dict],
    reframed_since: Union[str, datetime],
    reframed_before: str,
) -> list[dict]:
    """serialized formated measurements for summary url response
    params:
    serialized queryset
    reframed since and before date in function of API parameters
    returns:
    response of agregated data : DataRecordAggregateResponse schema
    """

    temp_array = numpy.array([], dtype=float)
    hum_array = numpy.array([], dtype=float)
    precip_array = numpy.array([], dtype=float)

    for row in serialized_queryset:
        temp_array = numpy.append(temp_array, row[LabelField.TEMP])
        hum_array = numpy.append(hum_array, row[LabelField.HUM])
        precip_array = numpy.append(precip_array, row[LabelField.PRECIP])

    time_slot = f"{reframed_before},{reframed_since}"

    return [
        {
            "label": LabelField.TEMP,
            "time_slot": time_slot,
            "value": {
                "min": numpy.min(temp_array),
                "max": numpy.max(temp_array),
                "avg": numpy.average(temp_array),
            },
        },
        {
            "label": LabelField.HUM,
            "time_slot": time_slot,
            "value": {
                "min": numpy.min(hum_array),
                "max": numpy.max(hum_array),
                "avg": numpy.average(hum_array),
            },
        },
        {
            "label": LabelField.PRECIP,
            "time_slot": time_slot,
            "value": numpy.sum(precip_array),
        },
    ]


def get_raw_data_controler(
    serialized_queryset: list[dict],
) -> list[dict]:
    """
    serialized formated measurements for data url response
    returns formated data from db
    """

    response = []

    for row in serialized_queryset:
        response.append(
            [
                {
                    "label": LabelField.TEMP,
                    "measured_at": row["date"],
                    "value": row["temp"],
                },
                {
                    "label": LabelField.HUM,
                    "measured_at": row["date"],
                    "value": row["hum"],
                },
                {
                    "label": LabelField.PRECIP,
                    "measured_at": row["date"],
                    "value": row["precip"],
                },
            ]
        )

    return response
