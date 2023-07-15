from io import BytesIO
from zipfile import ZipFile, ZipExtFile
from urllib.request import urlopen
from re import finditer, MULTILINE
from typing import Optional
from collections.abc import Callable, Iterable
import csv

BASE_URL = 'https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne'


def get_default_station_list() -> list:
    unparsed_weather_stations = get_file('/wykaz_stacji.csv', encoding='iso8859_2')
    weather_stations = csv.reader(
        unparsed_weather_stations.splitlines(),
        skipinitialspace=True,
        quotechar='"'
    )

    return list(weather_stations)


def get_default_schema() -> list:
    schema = parse_schema(
        get_file('/terminowe/synop/s_t_format.txt', encoding="cp1250")
    )
    return schema


def get_default_weather_data(year: int, station_code: int, schema: list) -> str:
    weather_data = get_file(
        f'/terminowe/synop/{year}/{year}_{station_code}_s.zip',
        encoding='iso8859_2',
        needs_unzipping=True
    ).splitlines()

    return apply_schema_to_weather_data(weather_data, schema)


def weather_data_fetcher(
        *,
        year: Optional[int] = None,
        station_code: Optional[int] = None
        ) -> Callable[[int], list[dict]]:
    '''
    If called with year, returns a function that can be called with station_code to retrive weather data

    If called with station_code, returns a function that can be called with year to retrive weather data
    '''
    if not ((year is None) ^ (station_code is None)):
        raise TypeError(
            'year and station_code are mutualy exclusive. Choose one and call returned object with another.'
        )
    schema = get_default_schema()

    if year:
        def fetch_weather_by_station(station_code: int) -> list[dict]:
            return get_default_weather_data(year, station_code, schema)

        return fetch_weather_by_station

    elif station_code:
        def fetch_weather_by_year(year: int) -> list[dict]:
            return get_default_weather_data(year, station_code, schema)

        return fetch_weather_by_year


def get_file(url_ending: str, encoding: str, needs_unzipping: bool = False) -> str:
    '''
    Get file from a URL.
    If needs_unzipping, decoded data will unzipped and file returned

    Returned file-like object will be decoded according do provided encoding
    '''
    raw_data = urlopen(f'{BASE_URL}{url_ending}')

    if needs_unzipping:
        data = text_file_from_zip(raw_data.read())
    else:
        data = raw_data

    return data.read().decode(encoding=encoding)


def text_file_from_zip(byte_sequence: bytes, file_number: int = 0) -> ZipExtFile:
    '''
    Parse byte squence to zip file and return a file like object
    '''
    zip = ZipFile(BytesIO(byte_sequence))
    file = zip.open(zip.namelist()[file_number])
    return file


def get_weather_station_code(
        weather_station_name: str,
        weather_stations: Optional[Iterable[Iterable[str]]] = None) -> int:
    '''
    Retrive station code based on a name. If weather_stations is not provided, a default list
    of weather stations will be fetched
    '''
    # Weather stations CSV file schema:
    # long_code, name, code
    # "354180135","HEL","  135"
    if weather_stations is None:
        weather_stations = get_default_station_list()

    # It seems that only stations with code this long have complete weather data
    STATION_CODE_LENGTH = 3

    for station in weather_stations:
        if station[1] == weather_station_name:
            if len(station[2].lstrip()) == STATION_CODE_LENGTH:
                return int(station[2])
            else:
                raise ValueError(f"Station {weather_station_name} exists, but no weather data is available")

    raise ValueError(f"Station {weather_station_name} does not exist")


def parse_schema(unparsed_schema: str) -> list:
    '''
    Return list of fields from text
    Text must follow:

    Field1                                    something
    Field2                                    something
    Field3                                    something

    Anything else will be discarded
    This example would return: [Field1, Field2, Field3]
    '''

    schema = []
    matches = finditer(r"([A-Z].+?)\s{3,}", unparsed_schema, MULTILINE)
    for match in matches:
        schema.append(match.group(1))

    return schema


def apply_schema_to_weather_data(weather_data: Iterable[str], schema: Iterable) -> list[dict[str, str]]:
    '''
    Uses csv.DictReader to match weather_data with schema. Each element in weather data should be valid CSV.

    Return list of dictionaries where each element is datapoint, and specific data can be retrived with key
    from schema.
    '''
    data = csv.DictReader(
        weather_data, delimiter=',', fieldnames=schema
    )

    return list(data)
