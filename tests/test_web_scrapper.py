import pytest
from src import web_scrapper


@pytest.fixture
def weather_stations_csv():
    return '''"251199989","Test_name_1","94521"
"354180131","Test_name_2","  131"
"254170010","Test_name_3","1"
'''


def test_get_weather_station_code_correct(weather_stations_csv):
    code = web_scrapper.get_weather_station_code("Test_name_2", weather_stations_csv)
    assert code == 131


def test_get_weather_station_code_too_long_code(weather_stations_csv):
    with pytest.raises(ValueError):
        web_scrapper.get_weather_station_code("Test_name_1", weather_stations_csv)


def test_get_weather_station_code_too_short_code(weather_stations_csv):
    with pytest.raises(ValueError):
        web_scrapper.get_weather_station_code("Test_name_3", weather_stations_csv)


def test_get_weather_station_code_fake_name(weather_stations_csv):
    with pytest.raises(ValueError):
        web_scrapper.get_weather_station_code("Test_name_fake", weather_stations_csv)
