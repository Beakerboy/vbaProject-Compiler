import datetime

def test_datetime():
    input = 0x01D92433C2B823C0
    date = filetime2datetime(input)
    assert date.ctime() == "Mon Jan  9 14:07:51 2023"

def filetime2datetime(filetime):
    """
    convert FILETIME (64 bits int) to Python datetime.datetime
    """
    _FILETIME_null_date = datetime.datetime(1601, 1, 1, 0, 0, 0)
    return _FILETIME_null_date + datetime.timedelta(microseconds=filetime//10)
