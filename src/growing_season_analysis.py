import web_scraper
import helpers
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class DatesRange:
    start: datetime | None = None
    end: datetime | None = None

    @property
    def delta(self):
        if self.start and self.end:
            return self.end - self.start
        else:
            return timedelta(0)


def date_range_finder(year_data, lowest_temperature):
    '''
    Find longest stretch of temperatures above lowest_temperature.

    Returns dictionary with:
    - start: starting date
    - end: ending date
    - delta: timedelta between those two dates
    '''

    # Dictionary key on which analysis will be conducted
    key = 'Temperatura powietrza [°C]'

    max_range = DatesRange()
    temporary_range = DatesRange()

    prev_datapoint = None

    for datapoint in year_data:
        prev_temperature = float(prev_datapoint[key]) if prev_datapoint else lowest_temperature
        temperature = float(datapoint[key])

        if temperature > lowest_temperature and prev_temperature <= lowest_temperature:
            temporary_range.start = datetime(
                int(datapoint['Rok']),
                int(datapoint['Miesiąc']),
                int(datapoint['Dzień']),
                int(datapoint['Godzina']),
            )
        elif float(temperature) <= lowest_temperature and prev_temperature > lowest_temperature:
            temporary_range.end = datetime(
                int(prev_datapoint['Rok']),
                int(prev_datapoint['Miesiąc']),
                int(prev_datapoint['Dzień']),
                int(prev_datapoint['Godzina']),
            )

            if temporary_range.delta > max_range.delta:
                max_range = temporary_range
                temporary_range = DatesRange()

        prev_datapoint = datapoint

    return max_range


if __name__ == '__main__':
    # Configuration

    years = helpers.get_years_range(year_start=2019, year_end=2022)
    station_name = 'KRAKÓW-BALICE'
    lowest_temperature = 2

    # Getting static information
    station_code = web_scraper.get_weather_station_code(
        'KRAKÓW-BALICE',
        web_scraper.get_file('/wykaz_stacji.csv', encoding='iso8859_2')
    )
    schema = web_scraper.parse_schema(
        web_scraper.get_file('/terminowe/synop/s_t_format.txt', encoding="cp1250")
    )

    # Output
    print(f"Season with temperature above {lowest_temperature} celsius around {station_name}\n", 50*"-")

    for year in years:
        year_data = web_scraper.get_file(
            f'/terminowe/synop/{year}/{year}_{station_code}_s.zip',
            encoding='iso8859_2',
            needs_unzipping=True
        )

        mapped_year_data = web_scraper.apply_schema_to_weather_data(year_data, schema)

        date_range = date_range_finder(mapped_year_data, lowest_temperature)
        representation = f"{year}:\
 {date_range.start.strftime('%B %d').rjust(14)}\
 - {date_range.end.strftime('%d %B').ljust(14)}\
({date_range.delta.days} days)"

        print(representation)
