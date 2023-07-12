from datetime import date


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
