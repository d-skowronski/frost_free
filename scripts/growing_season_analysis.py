from collections.abc import Iterable
from datetime import datetime, timedelta
from dataclasses import dataclass
from src.helpers import datetime_from_datapoint


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

    def __str__(self) -> str:
        start = self.start.strftime('%B %d').rjust(14) if self.start else 'no date'.rjust(14)
        end = self.end.strftime('%d %B').ljust(14) if self.end else 'no date'.ljust(14)
        return f"{start} - {end} ({self.delta.days} days)"


def date_range_finder(
    year_data: Iterable[dict[str, str]],
    lowest_temperature: float | int,
    key: str = 'Temperatura powietrza [°C]'
) -> DatesRange:
    '''
    Find longest stretch of temperatures above lowest_temperature.
    Key represents dictionary key on which analysis will be conducted

    Returns object with:
    - start: starting date
    - end: ending date
    - delta: timedelta between those two dates
    '''

    max_range = DatesRange()
    temporary_range = DatesRange()

    prev_datapoint = None

    for datapoint in year_data:
        prev_temperature = float(prev_datapoint[key]) if prev_datapoint else lowest_temperature
        temperature = float(datapoint[key])

        if temperature > lowest_temperature and prev_temperature <= lowest_temperature:
            temporary_range = DatesRange()
            temporary_range.start = datetime_from_datapoint(datapoint)

        elif temperature <= lowest_temperature and prev_temperature > lowest_temperature:
            temporary_range.end = datetime_from_datapoint(prev_datapoint)

            if temporary_range.delta >= max_range.delta:
                max_range = temporary_range

        prev_datapoint = datapoint

    # Checks for edge case when datapoints end but temporary range is still open
    if temporary_range.end is None and temporary_range.start is not None:
        temporary_range.end = datetime_from_datapoint(year_data[-1])

        if temporary_range.delta >= max_range.delta:
            max_range = temporary_range

    return max_range
