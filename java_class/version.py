class Version:
    def __init__(self, raw_bytes: bytes) -> None:
        self.raw = raw_bytes

        self.__minor_version : int = None
        self.__major_version : int = None

    def get_minor_version(self) -> int:
        if self.__minor_version is None:
            self.__minor_version = int.from_bytes(self.raw[:2], byteorder="big", signed=False)

        return self.__minor_version

    def get_major_version(self) -> int:
        if self.__major_version is None:
            self.__major_version = int.from_bytes(self.raw[2:], byteorder="big", signed=False)

        return self.__major_version