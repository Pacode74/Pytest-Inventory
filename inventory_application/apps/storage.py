from inventory_application.apps.resources import Resources
from collections import namedtuple


class Storage(Resources):
    def __init__(self, name, manufacturer):
        super().__init__(name, manufacturer)
        self._capacity_GB = None

    @property
    def capacity_GB(self):
        return self._capacity_GB

    @capacity_GB.setter
    def capacity_GB(self, value):
        self._validate_int(value)
        setattr(self, "_capacity_GB", value)

    #     def __repr__(self):
    #         return super().__repr__() + f', capacity_GB={self.capacity_GB}'

    def _nt_storage(self):
        n = namedtuple(f"{str(type(self).__name__)}", "capacity_GB")
        return n(self.capacity_GB)

    def __repr__(self):
        Combined = namedtuple(
            f"{str(type(self).__name__)}",
            self._nt_resource()._fields + self._nt_storage()._fields,
        )
        combined_tuple = Combined(*self._nt_resource(), *self._nt_storage())
        return str(combined_tuple)
