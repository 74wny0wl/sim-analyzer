def mirror(byte):
    mirrored_byte = ((byte & 0x0F) << 4) | ((byte & 0xF0) >> 4)
    return mirrored_byte


def read_vector(bulk_data):
    for byte in bulk_data:
        yield mirror(byte)


def decode_vector(bulk_data):
    decoded_vector = ["{:02x}".format(mirrored_byte) for mirrored_byte in read_vector(bulk_data)]
    return decoded_vector


def decode_vector_as_sim_string(bulk_data):
    sim_string = ''.join(decode_vector(bulk_data))
    return sim_string.rstrip('f')
