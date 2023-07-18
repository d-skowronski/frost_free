from dataclasses import dataclass
from datetime import datetime


@dataclass
class MinMaxValidator:
    value: int | float
    min: int | float | None
    max: int | float | None

    def validate(self) -> int | float:
        if self.min and self.value < self.min:
            raise ValueError(f'Value too low! needs to be in range {self.min} to {self.max}')
        elif self.max and self.value > self.max:
            raise ValueError(f'Value too high! needs to be in range {self.min} to {self.max}')

        return self.value


def datetime_from_datapoint(
        datapoint: dict,
        field_names: list[str] = {
            'year': 'Rok',
            'month': 'Miesiąc',
            'day': 'Dzień',
            'hour': 'Godzina',
        }
) -> datetime:
    '''
    Create datetime object from datapoint. Maximum resolution is one hour.
    You can pass different field names if needed.
    '''

    return datetime(
        year=int(datapoint[field_names['year']]),
        month=int(datapoint[field_names['month']]),
        day=int(datapoint[field_names['day']]),
        hour=int(datapoint[field_names['hour']]),
    )
