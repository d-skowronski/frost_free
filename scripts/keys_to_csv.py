from src.helpers import datetime_from_datapoint
from csv import writer
from collections.abc import Iterable


def keys_to_csv(
        weather_data: Iterable[dict[str, str]],
        keys: Iterable[str] = ['Temperatura powietrza [°C]']
) -> None:
    '''
    Generate new CSV file.

    Format will be:

    datetime of datapoint, key1, key2...

    If no keys are provided only one key - temperature will be used
    '''
    with open('weather_data.csv', 'w') as file:
        csv_writer = writer(file)

        for datapoint in weather_data:
            fields = [float(datapoint[key]) for key in keys]
            csv_writer.writerow([datetime_from_datapoint(datapoint).isoformat(), *fields])
