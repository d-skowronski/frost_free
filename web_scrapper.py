from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
BASE_URL = 'https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne'


def get_file(url_ending, encoding, needs_unzipping=False):
    '''
    Get file from a URL.
    If needs_unzipping, decoded data will unzipped and file returned

    Returned file-like object will be decoded according do provided encoding
    '''
    raw_data = urlopen(f'{BASE_URL}{url_ending}')

    if needs_unzipping:
        data = text_file_from_zip(raw_data.read())
    else:
        data = raw_data

    return data.read().decode(encoding=encoding)


def text_file_from_zip(byte_sequence, file_number=0):
    '''
    Parse byte squence to zip file and return a file like object
    '''
    zip = ZipFile(BytesIO(byte_sequence))
    file = zip.open(zip.namelist()[file_number])

    return file
