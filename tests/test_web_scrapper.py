import pytest
from src import web_scrapper


@pytest.fixture
def valid_schema():
    return ['Station name', 'Day', 'Hour']


@pytest.fixture
def weather_data():
    return '''"Test_name","01","12"
"Test_name","02","13"
"Test_name","03","14"
'''


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
def weather_stations_csv():
    return '''"251199989","Test_name_1","94521"
"354180131","Test_name_2","  131"
"254170010","Test_name_3","1"
'''


# TESTS - get_weather_station_code
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


# TESTS - parse_schema
def test_parse_schema(schema_txt):
    schema = web_scrapper.parse_schema(schema_txt)
    assert schema == ['Wyskość próbki [cm]', 'Status pomiaru CIPR']


# TESTS - apply_schema_to_weather_data
def test_apply_schema_to_weather_data(valid_schema, weather_data):
    data = web_scrapper.apply_schema_to_weather_data(
        weather_data,
        valid_schema
    )

    assert data == [{'Station name': 'Test_name', 'Day': '01', 'Hour': '12'},
                    {'Station name': 'Test_name', 'Day': '02', 'Hour': '13'},
                    {'Station name': 'Test_name', 'Day': '03', 'Hour': '14'},
                    ]
