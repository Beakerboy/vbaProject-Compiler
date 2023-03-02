import uuid
test_cache():
    prefix = "3C 00 FF FF 00 00"
    guid1 = uuid.UUID("C8AE1FC3015E4219A2B65CBF0A6FA82A")
    guid2 = uuid.UUID("FCFB3D2AA0FA1068A73808002B3371B5")
    middle = "00" * 16 + 1.to_bytes(4, "little).hex()
    guid3 = uuid.UUID("892FE18148AA45178E8A2134D23D9DD3")

    part1 = prefix + guid1 + guid2 + middle + guid3
    part2 = guid3 + guid1
