class Resources:
    def __init__(self, name, manufacturer, quantity):
        self._validate_str(name)
        self._validate_str(manufacturer)
        self._validate_int(quantity)
        self._inventory = []
        self._name = name
        self._manufacturer = manufacturer
        self._quantity = quantity
        self.purchased(self._name, self._manufacturer, self._quantity)

    def _validate_str(self, value):
        if value is None or len(str(value).strip()) == 0:
            raise ValueError(f"{value} cannot be empty.")
        if not isinstance(value, str):
            raise TypeError(f"Unsupported type for value, {value} must be a string.")
        else:
            return value

    def _validate_int(self, value):
        if value is None or len(str(value).strip()) == 0:
            raise ValueError(f"{value} cannot be empty.")
        if not isinstance(value, int):
            raise TypeError(f"Unsupported type for value, {value} must be a integer.")
        if value <= 0:
            raise ValueError(f"{value} must be greater than zero.")
        else:
            return value

    def purchased(self, name, manufacturer, quantity):
        """Add an item to the inventory or update its quantity if it already exists."""
        name = self._validate_str(name)
        manufacturer = self._validate_str(manufacturer)
        quantity = self._validate_int(quantity)
        for d in self._inventory:
            if d["name"] == name:
                d["total"] += quantity
                break
        else:
            self._inventory.append(
                {
                    "name": name,
                    "manufacturer": manufacturer,
                    "total": quantity,
                    "allocated": 0,
                    "remaining": 0,
                }
            )

    def claim(self, name, quantity):
        """Method to take n resources from the pool (as long as inventory is available)"""
        self._validate_str(name)
        self._validate_int(quantity)
        for d in self._inventory:
            if d["name"] == name:
                if d["total"] != 0 and d["allocated"] <= d["total"]:
                    d["allocated"] += quantity
                    d["remaining"] = d["total"] - d["allocated"]

    def freeup(self, name, quantity):
        """Method to return n resources to the pool (e.g. disassembled some builds)"""
        self._validate_str(name)
        self._validate_int(quantity)
        for d in self._inventory:
            if d["name"] == name:
                if d["total"] != 0 and d["allocated"] != 0:
                    d["allocated"] -= quantity
                    d["remaining"] = d["total"] - d["allocated"]

    def died(self, name, quantity):
        """Method to return and permanently remove inventory from the pool
        (e.g. they broke something) - as long as total available allows it"""
        self._validate_str(name)
        self._validate_int(quantity)
        for d in self._inventory:
            if d["name"] == name:
                if d["total"] != 0 and d["allocated"] != 0:
                    if d["total"] == quantity:
                        self._inventory.remove(d)
                    else:
                        d["total"] -= quantity
                        d["allocated"] -= quantity
                        d["remaining"] = d["total"] - d["allocated"]
                    break

    def search_name(self, name):
        self._validate_str(name)
        for d in self._inventory:
            if d["name"] == name:
                return d
        return None

    def total(self, name):
        """Inventory total (how many are in the inventory pool)."""
        self._validate_str(name)
        for d in self._inventory:
            if d["name"] == name:
                return d["total"]

    def allocated(self, name):
        """Number allocated (how many are already in use)."""
        self._validate_str(name)
        for d in self._inventory:
            if d["name"] == name:
                return d["allocated"]

    @property
    def category(self):
        """Computed property that returns a lower case version of the class name"""
        return type(self).__name__.lower()

    def __str__(self):
        return f"{[d['name'] for d in self._inventory]}"

    def __repr__(self):
        return f"{self._inventory}"
