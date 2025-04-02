from binascii import crc32
from typing import BinaryIO


class Signature:
    BYTES_LEN = 8

    def __init__(self, signature_bytes: bytes) -> None:
        if not isinstance(signature_bytes, bytes) or len(signature_bytes) != 8:
            raise Exception()

        self.__bytes = signature_bytes

    def get_bytes(self) -> bytes:
        return self.__bytes

    def __repr__(self) -> str:
        return "Signature[{}]".format(self.__bytes)

class Chunk:
    def __init__(self, chunk_bytes: bytes) -> None:
        if not isinstance(chunk_bytes, bytes) or len(chunk_bytes) < 12:
            raise Exception()

        if crc32(chunk_bytes[4:-4]).to_bytes(4, "big") != chunk_bytes[-4:]:
            raise Exception()

        self.__bytes = chunk_bytes

    def get_length(self) -> int:
        return int.from_bytes(self.__bytes[:4], "big")

    def get_type(self) -> str:
        return self.__bytes[4:8].decode('ascii')

    def get_data(self) -> bytes:
        return self.__bytes[8:-4]

    def get_crc(self) -> bytes:
        return self.__bytes[-4:]

    def get_bytes(self):
        return self.__bytes

    def __repr__(self) -> str:
        return "Chunk[length={}, type={}, data={}, crc={}]".format(self.get_length(), self.get_type(), self.get_data(), self.get_crc())

def dump_signature(io: BinaryIO) -> Signature:
    return Signature(io.read(8))

def dump_chunk(io: BinaryIO) -> Chunk:
    length_bytes = io.read(4)
    length = int.from_bytes(length_bytes, "big")
    return Chunk(length_bytes + io.read(8 + length))

def dump_png(filepath: str) -> None:
    with open(filepath, 'rb') as f:
        signature = dump_signature(f)
        print(signature)

        while True:
            chunck = dump_chunk(f)
            print(chunck)
            if chunck.get_type() == 'IEND':
                break
