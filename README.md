# frost free season
A script for looking up the last and first frost dates for a given weather station.

I wanted to look in the past and determine the length of the growing season in previous years. However, most information on previous weather is not free. Having tried to look for a reputable API, I stumbled upon an official government institution in Poland that handles weather.

The API of "Instytut Meteorologii i Gospodarki Wodnej" was limited. I decided to compile data from their sets of CSV files to come up with an answer.
There is a chance that this script can stop working in the future if url's or layout of data were to change.

# modules
### web_scraper
Web scraper that can be used for various weather analysis tasks.

After providing the weather station name and a year, the module can return the data for each hour in a year with all the available fields. Fields: https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/terminowe/synop/s_t_format.txt

The data is returned as a list of dictionaries. Each list element represents an hour in a year.

##### example:
    def example():
      year = 2021

      # Get weather station code, given a name
      station_code = get_weather_station_code(
          'KRAKÓW-BALICE',
          get_file('/wykaz_stacji.csv', encoding='iso8859_2')
      )

      # Get list of fields in weather data
      schema = parse_schema(
          get_file('/terminowe/synop/s_t_format.txt', encoding="cp1250")
      )

      # Get weather data
      weather_data = get_file(
          f'/terminowe/synop/{year}/{year}_{station_code}_s.zip',
          encoding='iso8859_2',
          needs_unzipping=True
      )

      # Combine weather data with field names to create list of dictionaries
      data = apply_schema_to_weather_data(weather_data, schema)]
      
      return data[25]['Temperatura powietrza [°C]']


Field 'Temperatura powietrza [°C]' is air temperature.
Index 25 references 26th hour of a year - 2st January 2021, 1:00 am

### growing_season_analysis
Module conducts analysis to determine longest stretch in a year with temperatures above provided one.
You can check for many years at the same time. Returned data can be displayed in a console.

##### example return:
    Season with temperature above 2 celsius around KRAKÓW-BALICE
    --------------------------------------------------
    2010:       April 24 - 01 October     (160 days)
    2011:         May 07 - 09 October     (154 days)
    2012:         May 18 - 21 September   (125 days)
    2013:       April 16 - 28 September   (164 days)
    2014:         May 06 - 06 October     (152 days)
