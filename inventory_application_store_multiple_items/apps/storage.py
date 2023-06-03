from inventory_application_store_multiple_items.apps.resources import Resources


class Storage(Resources):
    def capacity_GB(self, name, capacity_GB):
        """Inventory capacity setter"""
        self._validate_str(name)
        self._validate_int(capacity_GB)
        for d in self._inventory:
            if d["name"] == name:
                d["capacity_GB"] = capacity_GB
