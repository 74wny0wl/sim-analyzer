import sim
from sim import directory, bytes_vector


def get_iccid(sim_dump_directory_path: str, iccid_file_name='2FE2') -> str:
    iccid_file_path = directory.find_file(sim_dump_directory_path, file_name=iccid_file_name)
    with open(iccid_file_path, 'rb') as iccid_file:
        iccid_bulk_data = iccid_file.read()

    _iccid = ""
    for i in range(10):
        iccid_byte = "{:02x}".format(sim.bytes_vector.mirror(iccid_bulk_data[i]))
        _iccid += iccid_byte

    return _iccid
