from scripts import keys_to_csv, growing_season_analysis  # noqa: F401
from src import web_scraper, input_helpers  # noqa: F401


if __name__ == '__main__':
    # example station name, full list at
    # https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/wykaz_stacji.csv
    station_name = 'KRAKÓW-BALICE'

    station_code = web_scraper.get_weather_station_code(station_name)
    fetch_data = web_scraper.weather_data_fetcher(station_code=station_code)

    # EXAMPLE 1 - generate csv file of selected keys
    # keys_to_csv.keys_to_csv(fetch_data(2006))

    # EXAMPLE 2 - determine longest stretch of dates with temperatures above 2 deg Celsius
    # lowest_temperature = 2

    # print(f"Season with temperature above {lowest_temperature} celsius around {station_name}\n", 50*"-")
    # for year in input_helpers.get_years_range(2001, 2022):
    #     data = fetch_data(year)
    #     result = growing_season_analysis.date_range_finder(data, lowest_temperature)

    #     print(f'{year}: {result}')
