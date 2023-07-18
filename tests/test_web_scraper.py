import pytest
from src import web_scraper


@pytest.fixture
def valid_schema():
    return ['Station name', 'Day', 'Hour']


@pytest.fixture
def weather_data_after_splitlines():
    return ['Test_name,01,12',
            'Test_name,02,13',
            'Test_name,03,14']


@pytest.fixture
def schema_txt():
    return '''Wyskość próbki [cm]                                     5                                    5
Status pomiaru CIPR                                      1

Status "8" brak pomiaru  r
Status "9" brak zjawiska

Dla pola "Wysokość pokrywy śnieżnej" (PKSN) stosuje się wartości kodowane:
997 - mniejsza od 0.5 cm   r
998 - nieciągła    12
999 - niemożliwa do pomiaru
'''


@pytest.fixture
def weather_stations_list():
    return [["251199989", "Test_name_1", "94521"],
            ["354180131", "Test_name_2", "  131"],
            ["254170010", "Test_name_3", "1"]]


# TESTS - get_weather_station_code
def test_get_weather_station_code_correct(weather_stations_list):
    code = web_scraper.get_weather_station_code("Test_name_2", weather_stations_list)
    assert code == 131


def test_get_weather_station_code_too_long_code(weather_stations_list):
    with pytest.raises(ValueError):
        web_scraper.get_weather_station_code("Test_name_1", weather_stations_list)


def test_get_weather_station_code_too_short_code(weather_stations_list):
    with pytest.raises(ValueError):
        web_scraper.get_weather_station_code("Test_name_3", weather_stations_list)


def test_get_weather_station_code_fake_name(weather_stations_list):
    with pytest.raises(ValueError):
        web_scraper.get_weather_station_code("Test_name_fake", weather_stations_list)


# TESTS - parse_schema
def test_parse_schema(schema_txt):
    schema = web_scraper.parse_schema(schema_txt)
    assert schema == ['Wyskość próbki [cm]', 'Status pomiaru CIPR']


# TESTS - apply_schema_to_weather_data
def test_apply_schema_to_weather_data(weather_data_after_splitlines, valid_schema):
    data = web_scraper.apply_schema_to_weather_data(
        weather_data_after_splitlines,
        valid_schema
    )
    print(data)
    assert data == [{'Station name': 'Test_name', 'Day': '01', 'Hour': '12'},
                    {'Station name': 'Test_name', 'Day': '02', 'Hour': '13'},
                    {'Station name': 'Test_name', 'Day': '03', 'Hour': '14'},
                    ]


# TESTS weather_data_fetcher
def test_weather_data_fetcher_by_year():
    fetch_weather = web_scraper.weather_data_fetcher(year=2022)
    result = fetch_weather(station_code=566)

    assert isinstance(result, list)


def test_weather_data_fetcher_by_station():
    fetch_weather = web_scraper.weather_data_fetcher(station_code=566)
    result = fetch_weather(year=2022)

    assert isinstance(result, list)


def test_weather_data_fetcher_invalid_args():
    with pytest.raises(TypeError):
        web_scraper.weather_data_fetcher(station_code=566, year=2022)

    with pytest.raises(TypeError):
        web_scraper.weather_data_fetcher()

