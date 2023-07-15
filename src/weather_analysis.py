from datetime import date
import helpers


def get_years_range(year_start: int, year_end: int) -> range:
    '''
    Validates if years are in correct range.

    Returns range object: year_start to year_end (both inclusive).

    Scraping weather data works for years 2001 to current year - 1.
    '''
    MIN_YEAR = 2001
    MAX_YEAR = date.today().year - 1

    starting_year = helpers.MinMaxValidator(year_start, MIN_YEAR, MAX_YEAR).validate()
    ending_year = helpers.MinMaxValidator(year_end, MIN_YEAR, MAX_YEAR).validate()

    return range(starting_year, ending_year+1)


def get_years_range_user_input() -> range:
    '''
    Wrapper around get_years_range that allows for direct input
    of years from console.
    '''
    years = None

    while years is None:
        try:
            year_start = int(input('Starting year: '))
            year_end = int(input('Ending year: '))
            years = get_years_range(year_start=year_start, year_end=year_end)
        except ValueError as e:
            print(f'\n{str(e)}\nTry again\n')

    return years
