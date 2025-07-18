class AccessFlags:
    def __init__(self, raw_bytes: bytes) -> None:
        self.raw = raw_bytes

    def get_hex(self) -> str:
        return self.raw.hex().upper()

    def is_public(self) -> bool:
        return (0x0001 & self.raw) != 0

    def is_final(self) -> bool:
        return (0x0010 & self.raw) != 0

    def is_super(self) -> bool:
        return (0x0020 & self.raw) != 0

    def is_interface(self) -> bool:
        return (0x0200 & self.raw) != 0

    def is_abstract(self) -> bool:
        return (0x0400 & self.raw) != 0

    def is_synthetic(self) -> bool:
        return (0x1000 & self.raw) != 0

    def is_annotation(self) -> bool:
        return (0x2000 & self.raw) != 0

    def is_enum(self) -> bool:
        return (0x4000 & self.raw) != 0

    def is_module(self) -> bool:
        return (0x8000 & self.raw) != 0
