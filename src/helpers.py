from dataclasses import dataclass


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
