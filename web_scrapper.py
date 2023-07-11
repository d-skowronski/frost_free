from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import csv

BASE_URL = 'https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne'


def get_file(url_ending, encoding, needs_unzipping=False):
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


def text_file_from_zip(byte_sequence, file_number=0):
    '''
    Parse byte squence to zip file and return a file like object
    '''
    zip = ZipFile(BytesIO(byte_sequence))
    file = zip.open(zip.namelist()[file_number])

    return file


def get_weather_station_code(weather_station_name, unparsed_weather_stations):
    # Weather stations CSV file schema:
    # long_code, name, code
    # "354180135","HEL","  135"
    weather_stations = csv.reader(
        unparsed_weather_stations.splitlines(),
        skipinitialspace=True,
        quotechar='"'
    )

    # It seems that only stations with code this long have complete weather data
    STATION_CODE_LENGTH = 3

    for station in weather_stations:
        if station[1] == weather_station_name:
            if len(station[2].lstrip()) == STATION_CODE_LENGTH:
                return int(station[2])
            else:
                raise ValueError(f"Station {weather_station_name} exists, but no weather data is available")

    raise ValueError(f"Station {weather_station_name} does not exist")


