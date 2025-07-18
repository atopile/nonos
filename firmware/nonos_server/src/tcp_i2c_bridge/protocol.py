"""Network protocol definitions for TCP-I2C bridge."""

import struct
from dataclasses import dataclass
from enum import IntEnum
from typing import Self

# Documentation: https://wiki.analog.com/resources/tools-software/sigmastudio/usingsigmastudio/tcpipchannels
# alternative: https://github.com/aventuri/sigma_tcp


class Command(IntEnum):
    """Protocol command types."""

    READ_REQUEST = 0x0A
    WRITE_REQUEST = 0x09
    READ_RESPONSE = 0x0B


class DecodeException(Exception):
    """Exception raised when decoding fails."""

    pass


class DecodeExceptionInvalidHeaderCommand(DecodeException):
    """Exception raised when decoding fails because of invalid header command."""

    def __init__(self, message: str, command: int):
        super().__init__(message)
        self.command = command


class DecodeExceptionInvalidData(DecodeException):
    """Exception raised when decoding fails because of invalid data."""

    def __init__(self, message: str, data: bytes):
        super().__init__(message)
        self.data = data


class DecodeExceptionInvalidDataPayload(DecodeExceptionInvalidData):
    """Exception raised when decoding fails because of invalid data."""

    def __init__(self, message: str, data: bytes, payload: bytes):
        super().__init__(message, data)
        self.payload = payload


class DecodeExceptionInsufficientData(DecodeException):
    """Exception raised when decoding fails because of insufficient data."""

    pass


@dataclass
class Header:
    Control: Command  # 1 byte
    """
    This is the control bit that is used to indicate that it is a write packet. Its value is 0x09
    """

    SIZE = 1

    def pack(self) -> bytes:
        """Pack into bytes."""
        return struct.pack(">B", self.Control)

    @classmethod
    def unpack(cls, data: bytes) -> "Header":
        """Unpack from bytes."""
        if len(data) < cls.SIZE:
            raise DecodeExceptionInsufficientData(
                f"Insufficient data for header: {len(data)} < 1"
            )

        try:
            return cls(Control=Command(data[0]))
        except Exception as e:
            raise DecodeExceptionInvalidHeaderCommand(
                f"Failed to unpack header: {e}", data[0]
            ) from e

    def get_request(
        self, data: bytes
    ) -> "tuple[Read.Request, bytes] | tuple[Write.Request, bytes]":
        """Get request based on command."""
        if self.Control == Command.READ_REQUEST:
            return Read.Request.unpack(data)
        elif self.Control == Command.WRITE_REQUEST:
            return Write.Request.unpack(data)
        raise DecodeException(f"Unknown command: {self.Control}")


@dataclass
class Write:
    @dataclass
    class Request:
        Header = Header(Control=Command.WRITE_REQUEST)

        Block_safeload_write: int  # 1 byte
        """
        This field indicates whether the write packet is a block write or a safeload write
        """
        Channel_number: int  # 1 byte
        """
        This indicates the channel number
        """
        Total_length: int  # 4 bytes
        """
        This indicates the total length of the write packet
        """
        Chip_address: int  # 1 byte
        """
        IC address
        """
        Data_length: int  # 4 bytes
        """
        This is the length of the data
        """
        Address: int  # 2 bytes
        """
        Register address
        """
        Data: bytes  # n bytes
        """
        This is the data to be written
        """

        SIZE = Header.SIZE + 1 + 1 + 4 + 1 + 4 + 2

        @classmethod
        def unpack(cls, data: bytes) -> tuple[Self, bytes]:
            if len(data) < cls.SIZE:
                raise DecodeExceptionInsufficientData(
                    f"Insufficient data for write request: {len(data)} < {cls.SIZE}"
                )

            header = Header.unpack(data[: Header.SIZE])
            assert header.Control == Command.WRITE_REQUEST

            total_length = struct.unpack(
                ">I", data[header.SIZE + 2 : header.SIZE + 2 + 4]
            )[0]
            packet_data = data[header.SIZE : total_length]
            data = data[total_length:]

            request = cls(
                Block_safeload_write=packet_data[0],
                Channel_number=packet_data[1],
                Total_length=total_length,
                Chip_address=packet_data[6],
                Data_length=struct.unpack(">I", packet_data[7:11])[0],
                Address=struct.unpack(">H", packet_data[11:13])[0],
                Data=packet_data[13:],
            )

            if len(request.Data) < request.Data_length:
                raise DecodeExceptionInsufficientData(
                    f"Data length mismatch: {len(request.Data)} != {request.Data_length}"
                )
            elif len(request.Data) > request.Data_length:
                raise DecodeExceptionInvalidDataPayload(
                    f"Data length mismatch: {len(request.Data)} != {request.Data_length}",
                    data=packet_data,
                    payload=request.Data,
                )

            return request, data


@dataclass
class Read:
    @dataclass
    class Request:
        Header = Header(Control=Command.READ_REQUEST)

        Total_length: int  # 4 bytes
        """
        This indicates the total length of the write packet
        """
        Chip_address: int  # 1 byte
        """
        IC address
        """
        Data_length: int  # 4 bytes
        """
        This is the length of the data
        """
        Address: int  # 2 bytes
        """
        Register address
        """
        Reserved: int  # 2 bytes
        """
        This is the reserved field
        """

        SIZE = Header.SIZE + 4 + 1 + 4 + 2 + 2

        @classmethod
        def unpack(cls, data: bytes) -> tuple[Self, bytes]:
            if len(data) < cls.SIZE:
                raise DecodeExceptionInsufficientData(
                    f"Insufficient data for read request: {len(data)} < {cls.SIZE}"
                )

            header = Header.unpack(data[: Header.SIZE])
            assert header.Control == Command.READ_REQUEST
            payload = data[Header.SIZE :]

            request = cls(
                Total_length=struct.unpack(">I", payload[:4])[0],
                Chip_address=payload[4],
                Data_length=struct.unpack(">I", payload[5:9])[0],
                Address=struct.unpack(">H", payload[9:11])[0],
                Reserved=payload[11],
            )

            assert request.Total_length == cls.SIZE

            return request, data[cls.SIZE :]

        def create_response(
            self, error: bool = False, data: bytes = b""
        ) -> "Read.Response":
            return Read.Response.create(
                chip_address=self.Chip_address,
                address=self.Address,
                error=error,
                data=data,
            )

    @dataclass(kw_only=True)
    class Response:
        Header = Header(Control=Command.READ_RESPONSE)

        Total_length: int  # 4 bytes
        """
        This indicates the total length of the write packet
        """
        Chip_address: int  # 1 byte
        """
        IC address
        """
        Data_length: int  # 4 bytes
        """
        This is the length of the data
        """
        Address: int  # 2 bytes
        """
        Register address
        """
        Status: int  # 1 byte
        """
        This byte indicates whether the read operation was a success or failure. It should be populated with a 0 for success and 1 for failure
        """
        Reserved: int = 0  # 1 byte
        """
        This is the reserved field
        """
        Data: bytes  # n bytes
        """
        This is the data read from the IC
        """

        @classmethod
        def create(
            cls,
            *,
            chip_address: int = 0x0,
            address: int,
            error: bool = False,
            data: bytes,
        ) -> Self:
            return cls(
                Total_length=(1 + 4 + 1 + 4 + 2 + 1 + 1) + len(data),
                Chip_address=chip_address,
                Data_length=len(data),
                Address=address,
                Status=1 if error else 0,
                Data=data,
            )

        def pack(self) -> bytes:
            """Pack into bytes."""
            FORMAT = ">I B I H B B"
            out = (
                self.Header.pack()
                + struct.pack(
                    FORMAT,
                    self.Total_length,
                    self.Chip_address,
                    self.Data_length,
                    self.Address,
                    self.Status,
                    self.Reserved,
                )
                + self.Data
            )
            assert len(out) == self.Total_length
            return out


if __name__ == "__main__":
    data = "0A0000000E0100000002F6E200000A"
    # 0A0000000E0100000002F6E200000A

    # 0A Control = read
    # 0000000E total length = 14
    # 01 Chip address = 1
    # 00000002 Data length = 2
    # F6E2 Address = 63106
    # 0000 Reserved = 0

    data_hex = bytes.fromhex(data)
    header = Header.unpack(data_hex)
    print(header)

    request, remaining_buffer = header.get_request(data_hex)
    print(request)
    print(remaining_buffer)
