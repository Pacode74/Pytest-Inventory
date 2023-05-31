from inventory_application.apps.storage import Storage
from collections import namedtuple
import re


class HDD(Storage):
    def __init__(self, name, manufacturer):
        super().__init__(name, manufacturer)
        self._size = None
        self._rpm = None

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._validate_str(value)
        pattern = r"^(2\.5\"|3\.5\")$"
        match = re.match(pattern, value)
        if not match:
            raise ValueError('value can be either 2.5" of 3.5" .')
        else:
            setattr(self, "_size", value)

    @property
    def rpm(self):
        return self._rpm

    @rpm.setter
    def rpm(self, value):
        self._validate_int(value)
        if not 5_400 <= value <= 10_000:
            raise ValueError("value can only be between 5,400 and 10,000.")
        else:
            setattr(self, "_rpm", value)

    #     def __repr__(self):
    #         return super().__repr__() + f', size={self.size}, rpm={self.rpm}'

    def _nt_hdd(self):
        n = namedtuple(f"{str(type(self).__name__)}", "size rpm")
        return n(self.size, self.rpm)

    def __repr__(self):
        Combined = namedtuple(
            f"{str(type(self).__name__)}",
            self._nt_resource()._fields
            + self._nt_storage()._fields
            + self._nt_hdd()._fields,
        )
        combined_tuple = Combined(
            *self._nt_resource(), *self._nt_storage(), *self._nt_hdd()
        )
        return str(combined_tuple)
