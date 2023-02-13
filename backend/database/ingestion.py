from os import environ
from typing import Union

import requests


def fetch_measurements() -> Union[list[dict], None]:
    """get measurements data from url in environnement variables
    returns the raw json from measurement service
    """
    url = environ["MEASUREMENTS_DATA_URL"]
    try:
        server_response = requests.get(url)
        if server_response.status_code == 200:
            return server_response.json()
    except:
        raise ConnectionError(f"could not find data from {url}")


def parse_measurements(measurements: Union[list[dict], None]) -> list[dict]:
    """measurements type is a dict with list at 'measurements' key.
    this list dicts with all data inside.
    returns: a list of fields to import into the table."""
    return [
        {
            "id": measure,
            "precip": dict_to_iterate[measure]["precip"],
            "temp": dict_to_iterate[measure]["temp"],
            "hum": dict_to_iterate[measure]["hum"],
        }
        for dict_to_iterate in measurements
        for measure in dict_to_iterate
    ]
