import re
from inventory_application_store_multiple_items.apps.storage import Storage


class HDD(Storage):
    def size(self, name, size):
        """Inventory size setter"""
        import re

        self._validate_str(name)
        if size is None or len(str(size).strip()) == 0:
            raise ValueError(f"{size} cannot be empty.")
        if not isinstance(size, str):
            raise TypeError(f"Unsupported type for value, {size} must be a string.")
        pattern = r"^(2\.5\"|3\.5\")$"
        match = re.match(pattern, size)
        if not match:
            raise ValueError(f'{size} can be either 2.5" of 3.5" .')
        else:
            for d in self._inventory:
                if d["name"] == name:
                    d["size"] = size

    def rpm(self, name, rpm):
        "rpm setter"
        self._validate_str(name)
        if rpm is None or len(str(rpm).strip()) == 0:
            raise ValueError(f"{rpm} cannot be empty.")
        if not isinstance(rpm, int):
            raise TypeError(f"Unsupported type for value, {rpm} must be a integer.")
        if not 5_400 <= rpm <= 10_000:
            raise ValueError(f"{rpm} can only be between 5,400 and 10,000.")
        else:
            for d in self._inventory:
                if d["name"] == name:
                    d["rpm"] = rpm
