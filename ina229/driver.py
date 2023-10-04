from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from enum import IntEnum
from typing import ClassVar
from warnings import warn

from periphery import GPIO, SPI


@dataclass
class INA229:
    """A Python driver for Texas Instruments INA229 85-V, 20-Bit,
    Ultra-Precise Power/Energy/Charge Monitor With SPI Interface
    Expander with Serial Interface
    """

    class Address(IntEnum):
        CONFIG: int = 0x00
        ADC_CONFIG: int = 0x01
        SHUNT_CAL: int = 0x02
        SHUNT_TEMPCO: int = 0x03
        VSHUNT: int = 0x04
        VBUS: int = 0x05
        DIETEMP: int = 0x06
        CURRENT: int = 0x07
        POWER: int = 0x08
        ENERGY: int = 0x09
        CHARGE: int = 0x0A
        DIAG_ALRT: int = 0x0B
        SOVL: int = 0x0C
        SUVL: int = 0x0D
        BOVL: int = 0x0E
        BUVL: int = 0x0F
        TEMP_LIMIT: int = 0x10
        PWR_LIMIT: int = 0x11
        MANUFACTURING_ID: int = 0x3E
        DEVICE_ID: int = 0x3F

    @dataclass
    class Operation(ABC):
        READ_OR_WRITE_BIT: ClassVar[int]
        address: int
        register_address: int

        @property
        def control_byte(self) -> int:
            return (
                (self.address << INA229.ADDRESS_OFFSET)
                | (self.READ_OR_WRITE_BIT << INA229.READ_OR_WRITE_BIT_OFFSET)
            )

        @property
        @abstractmethod
        def data_bytes(self) -> list[int]:
            pass

        @property
        def transmitted_data(self) -> list[int]:
            return [self.control_byte, *self.data_bytes]

        @abstractmethod
        def parse(self, received_data: list[int]) -> int | None:
            pass

    @dataclass
    class Read(Operation):
        READ_OR_WRITE_BIT: ClassVar[int] = 1
        data_byte_count: int

        @property
        def data_bytes(self) -> list[int]:
            return (
                [(1 << INA229.SPI_WORD_BIT_COUNT) - 1] * self.data_byte_count
            )

        def parse(self, received_data: list[int]) -> int:
            parsed_data = 0

            for datum in received_data[-self.data_byte_count:]:
                parsed_data <<= INA229.SPI_WORD_BIT_COUNT
                parsed_data |= datum

            return parsed_data

    @dataclass
    class Write(Operation):
        READ_OR_WRITE_BIT: ClassVar[int] = 0
        data_bytes: list[int]

        def parse(self, received_data: list[int]) -> None:
            return None

    SPI_MODES: ClassVar[tuple[int, int]] = 0b00, 0b11
    """The supported spi modes."""
    MAX_SPI_MAX_SPEED: ClassVar[float] = 10e6
    """The supported maximum spi maximum speed."""
    SPI_BIT_ORDER: ClassVar[str] = 'msb'
    """The supported spi bit order."""
    SPI_WORD_BIT_COUNT: ClassVar[int] = 8
    """The supported spi number of bits per word."""
    ADDRESS_OFFSET: ClassVar[int] = 2
    """The address offset."""
    READ_OR_WRITE_BIT_OFFSET: ClassVar[int] = 0
    """The fixed-bits offset."""
    alert_gpio: GPIO
    """The alert GPIO."""
    spi: SPI
    """The SPI."""
    callback: Callable[[], None]
    """The callback function."""

    def __post_init__(self) -> None:
        if self.spi.mode not in self.SPI_MODES:
            raise ValueError('unsupported spi mode')
        elif self.spi.max_speed > self.MAX_SPI_MAX_SPEED:
            raise ValueError('unsupported spi maximum speed')
        elif self.spi.bit_order != self.SPI_BIT_ORDER:
            raise ValueError('unsupported spi bit order')
        elif self.spi.bits_per_word != self.SPI_WORD_BIT_COUNT:
            raise ValueError('unsupported spi number of bits per word')

        if self.spi.extra_flags:
            warn(f'unknown spi extra flags {self.spi.extra_flags}')

    def operate(self, *operations: Operation) -> list[int | None]:
        transmitted_data = []

        for operation in operations:
            transmitted_data.extend(operation.transmitted_data)

        received_data = self.spi.transfer(transmitted_data)

        assert isinstance(received_data, list)

        parsed_data = []
        begin = 0

        for operation in operations:
            end = begin + len(operation.transmitted_data)

            parsed_data.append(operation.parse(received_data[begin:end]))

            begin = end

        return parsed_data
