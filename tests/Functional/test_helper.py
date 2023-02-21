import create_cache


def test_create_cache():
    # Read the data from the demo file and decompress it.
    f = open('tests/blank/vbaProject.bin', 'rb')
    offset = 0x0800
    length = 0x0333
    f.seek(offset)
    expected = f.read(length)

    cookie = 0xB81C
    guid = "{00020819-0000-0000-C000-000000000046}"
    cache = create_cache.create_cache(cookie, guid)
    assert cache == expected
