def create_cache(cookie, guid):
    co = cookie
    ca = (b''
          + b'\x01\x16\x03\x00\x00\xF0\x00\x00\x00\xD2\x02\x00\x00\xD4\x00\x00'
          + b'\x00\x00\x02\x00\x00\xFF\xFF\xFF\xFF\xD9\x02\x00\x00\x2D\x03\x00'
          + b'\x00\x00\x00\x00\x00\x01\x00\x00\x00\xF3\x08' + co + b'\x00\x00\xFF'
          + b'\xFF\x23\x01\x00\x00\x88\x00\x00\x00\xB6\x00\xFF\xFF\x01\x01\x00'
          + b'\x00\x00\x00\xFF\xFF\xFF\xFF\x00\x00\x00\x00\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00' * 16 * 2
          + b'\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x03\x00\x00\x00\x05'
          + b'\x00\x00\x00\x07\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x01'
          + b'\x01\x08\x00\x00\x00\xFF\xFF\xFF\xFF\x78\x00\x00\x00\x08\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF'
          + b'\x00\x00\x00\x00\x4D\x45\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00'
          + b'\x00\x00\xFF\xFF\x00\x00\x00\x00\xFF\xFF\x01\x01\x00\x00\x00\x00'
          + b'\xDF\x00\xFF\xFF\x00\x00\x00\x00\x18\x00\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF' * 16 * 7
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x28\x00\x00\x00\x02\x00'
          + b'\x53\x4C\xFF\xFF\xFF\xFF\x00\x00\x01\x00\x53\x10\xFF\xFF\xFF\xFF'
          + b'\x00\x00\x01\x00\x53\x94\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x02\x3C'
          + b'\xFF\xFF\xFF\xFF\x00\x00\xFF\xFF\x01\x01\x00\x00\x00\x00\x01\x00'
          + b'\x4E\x00\x30\x00\x7B\x00\x30\x00\x30\x00\x30\x00\x32\x00\x30\x00'
          + b'\x38\x00\x31\x00\x39\x00\x2D\x00\x30\x00\x30\x00\x30\x00\x30\x00'
          + b'\x2D\x00\x30\x00\x30\x00\x30\x00\x30\x00\x2D\x00\x43\x00\x30\x00'
          + b'\x30\x00\x30\x00\x2D\x00\x30\x00\x30\x00\x30\x00\x30\x00\x30\x00'
          + b'\x30\x00\x30\x00\x30\x00\x30\x00\x30\x00\x34\x00\x36\x00\x7D\x00'
          + b'\x00\x00\x00\x00\x00\x00\xFF\xFF\xFF\xFF\x01\x01\x40\x00\x00\x00'
          + b'\x02\x80\xFE\xFF\xFF\xFF\xFF\xFF\x20\x00\x00\x00\xFF\xFF\xFF\xFF'
          + b'\x30\x00\x00\x00\x02\x01\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x2E\x00\x43\x00'
          + b'\x1D\x00\x00\x00\x25\x00\x00\x00\xFF\xFF\xFF\xFF\x40\x00\x00\x00'
          + b'\x00\x00\xFF\xFF\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\x00\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\x00\x00'
          + b'\x00\x00\x00\x00\xFF\xFF\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00'
          + b'\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\xFF\xFF\xFF\xFF'
          + b'\xFF\xFF\x00\x00\x00\x00\x00\x00\xDF\x00\x00\x00\x00\x00\x00\x00'
          + b'\x00' * 16 * 3
          + b'\x00\x00\x00\x00\x00\xFE\xCA\x01\x00\x00\x00\xFF\xFF\xFF\xFF\x01'
          + b'\x01\x08\x00\x00\x00\xFF\xFF\xFF\xFF\x78\x00\x00\x00\xFF\xFF\xFF'
          + b'\xFF\x00\x00')
    return ca
