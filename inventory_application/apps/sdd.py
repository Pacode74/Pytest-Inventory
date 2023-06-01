from inventory_application.apps.storage import Storage
from collections import namedtuple


class SDD(Storage):
    def __init__(self, name, manufacturer):
        super().__init__(name, manufacturer)
        self._interface = None

    @property
    def interface(self):
        return self._interface

    @interface.setter
    def interface(self, value):
        self._validate_str(value)
        setattr(self, "_interface", value)

    #     def __repr__(self):
    #         return super().__repr__() + f', interface={self.interface}'

    def _nt_sdd(self):
        n = namedtuple(f"{str(type(self).__name__)}", "interface")
        return n(self.interface)

    def __repr__(self):
        Combined = namedtuple(
            f"{str(type(self).__name__)}",
            self._nt_resource()._fields
            + self._nt_storage()._fields
            + self._nt_sdd()._fields,
        )
        combined_tuple = Combined(
            *self._nt_resource(), *self._nt_storage(), *self._nt_sdd()
        )
        return str(combined_tuple)
