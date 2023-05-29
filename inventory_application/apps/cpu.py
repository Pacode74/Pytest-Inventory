from inventory_application.apps.resources import Resources
from collections import namedtuple


class CPU(Resources):
    def __init__(self, name, manufacturer):
        super().__init__(name, manufacturer)
        self._cores = None
        self._socket = None
        self._power_watts = None

    @property
    def cores(self):
        return self._cores

    @cores.setter
    def cores(self, value):
        self._validate_int(value)
        setattr(self, "_cores", value)

    @property
    def socket(self):
        return self._socket

    @socket.setter
    def socket(self, value):
        self._validate_str(value)
        setattr(self, "_socket", value)

    @property
    def power_watts(self):
        return self._power_watts

    @power_watts.setter
    def power_watts(self, value):
        self._validate_int(value)
        setattr(self, "_power_watts", value)

    def _nt_cpu(self):
        n = namedtuple(f"{str(type(self).__name__)}", "core socket power_watts")
        return n(self.cores, self.socket, self.power_watts)

    def __repr__(self):
        Combined = namedtuple(
            f"{str(type(self).__name__)}",
            self._nt_resource()._fields + self._nt_cpu()._fields,
        )
        combined_tuple = Combined(*self._nt_resource(), *self._nt_cpu())
        return str(combined_tuple)

    #     def __repr__(self):
    #         return super().__repr__() + f', cores={self.cores}, socket={self.socket}, power_watts={self.power_watts}'
