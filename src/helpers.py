from datetime import date


def integer_input(prompt):
    '''
    Wrapper for input() that validates only integers
    '''
    while True:
        try:
            data = input(prompt)
            if data.isnumeric():
                return int(data)
            else:
                raise TypeError('Please provide this in numeric form')
        except TypeError as e:
            print(f'{str(e)}\n')


def get_years_range(year_start, year_end):
    '''
    This function provides extra validation.
    Scraping weather data works for years 2001 - current year.

    Returns range object: year_start to year_end (both inclusive).
    '''
    MIN_YEAR = 2001
    MAX_YEAR = date.today().year - 1

    if year_start < MIN_YEAR:
        raise ValueError(f'Earliest starting year can be {MIN_YEAR}')
    elif year_end > MAX_YEAR:
        raise ValueError('You can only check previous years')

    return range(year_start, year_end+1)


def get_years_range_user_input():
    '''
    Wrapper around get_years_range that allows for direct input
    of years from console.
    '''
    years = None

    while years is None:
        try:
            year_start = integer_input('Starting year: ')
            year_end = integer_input('Ending year: ')
            years = get_years_range(year_start=year_start, year_end=year_end)
        except ValueError as e:
            print(f'\n{str(e)}\nTry again\n')

    return years
