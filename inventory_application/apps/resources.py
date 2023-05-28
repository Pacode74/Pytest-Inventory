# resources
from collections import namedtuple


class Resources:
    def __init__(self, name, manufacturer):
        self.name = name
        self.manufacturer = manufacturer
        self._total = 0
        self._allocated = 0

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._validate_str(value)
        self._name = value

    @property
    def manufacturer(self):
        return self._manufacturer

    @manufacturer.setter
    def manufacturer(self, value):
        self._validate_str(value)
        self._manufacturer = value

    def purchase(self, n):
        """method to add inventory to the pool (e.g. they purchased a new CPU)"""
        self._validate_int(n)
        self._total += n

    def claim(self, n):
        """method to take n resources from the pool (as long as inventory is available)"""
        self._validate_int(n)
        if n > self._total:
            raise ValueError("The claimed number cannot be greater than total number.")
        else:
            self._allocated += n

    def freeup(self, n):
        """method to return n resources to the pool (e.g. disassembled some builds)"""
        self._validate_int(n)
        if n > self._allocated:
            raise ValueError("Freeup number cannot be greater than allocated number.")
        else:
            self._allocated -= n

    def died(self, n):
        """method to return and permanently remove inventory from the pool (e.g. they broke something)
        - as long as total available allows it"""
        self._validate_int(n)
        if self.allocated < n:
            raise ValueError("The died number is greater than allocated number.")
        else:
            self._allocated -= n
            self._total -= n

    @property
    def total(self):
        """inventory total (how many are in the inventory pool)."""
        return self._total

    @property
    def allocated(self):
        """number allocated (how many are already in use)."""
        return self._allocated

    @property
    def remaining(self):
        """computed property that calculates the number of remaining items in the inventory."""
        self._remaining = self._total - self._allocated
        return self._remaining

    @property
    def category(self):
        """Computed property that returns a lower case version of the class name"""
        return type(self).__name__.lower()

    def _validate_int(self, value):
        """validator for the integer"""
        if value is None or len(str(value).strip()) == 0:
            raise ValueError("value cannot be empty.")
        if not isinstance(value, int):
            raise TypeError("Unsupported type for value, value must be a integer.")
        if value <= 0:
            raise ValueError("Value must be greater than zero.")
        else:
            return value

    def _validate_str(self, value):
        """validator for the string"""
        if value is None or len(str(value).strip()) == 0:
            raise ValueError("value cannot be empty.")
        if not isinstance(value, str):
            raise TypeError("Unsupported type for value, value must be a string.")
        else:
            return value

    def __str__(self):
        return f"{type(self).__name__}(name='{self._name}', manufacturer='{self._manufacturer}')"

    def _nt_resource(self):
        n = namedtuple(
            f"{str(type(self).__name__)}",
            "category name manufacturer total allocated remaining",
        )
        return n(
            self.category,
            self.name,
            self.manufacturer,
            self.total,
            self.allocated,
            self.remaining,
        )

    def __repr__(self):
        return str(self._nt_resource())

    # def __str__(self):
    #     return self.name
    #
    # def __repr__(self):
    #     return f"category={self.category}, name={self.name}, manufacturer={self.manufacturer}, total={self.total}, " \
    #            f"allocated={self.allocated}, remaining={self.remaining}"
