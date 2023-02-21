import create_cache
import pytest


data_for_test = [((0xB81C, "{00020819-0000-0000-C000-000000000046}"),
                  (0x0800, 0x0333)),
                 ((0x9B9A, "{00020820-0000-0000-C000-000000000046}"),
                  (0x0C00, 0x0333))]

@pytest.mark.parametrize("input, expected", data_for_test)
def test_create_cache(input, expected):
    # Read the data from the demo file and decompress it.
    f = open('tests/blank/vbaProject.bin', 'rb')
    offset = expected[0]
    length = expected[1]
    f.seek(offset)
    file_data = f.read(length)

    cookie = input[0]
    guid = input[1]
    cache = create_cache.create_cache(cookie, guid)
    assert cache == file_data
