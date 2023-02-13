from datetime import datetime

from database.db import Base, session
from database.ingestion import fetch_measurements, parse_measurements
from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy_serializer import SerializerMixin


class Measurements(Base, SerializerMixin):
    """Measurements data from sensor"""

    __tablename__ = "measurements"
    pk = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String)
    date = Column(DateTime)
    precip = Column(Float)
    temp = Column(Float)
    hum = Column(Float)

    @classmethod
    def ingest(cls) -> dict:
        """data integration from measurement service
        returns: status dict to display
        """
        json_measurements = fetch_measurements()
        data_to_import = parse_measurements(json_measurements)

        status = {
            "state": "full ingestion",
            "messages": [],
            "measurements imported": 0,
        }

        for data in data_to_import:
            try:
                measurement = Measurements(
                    id=data["id"],
                    date=datetime.now().isoformat(),
                    precip=data["precip"],
                    temp=data["temp"],
                    hum=data["hum"],
                )
                session.add(measurement)
                session.commit()
                status["measurements imported"] += 1
            except Exception as exception:
                status["state"] = "partial ingestion"
                status["messages"].append(str(exception))

        if status["measurements imported"] == 0:
            status["state"] = ["ingestion null"]

        return status
