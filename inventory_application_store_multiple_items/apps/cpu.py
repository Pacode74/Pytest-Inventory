from inventory_application_store_multiple_items.apps.resources import Resources


class CPU(Resources):

    def core(self, name, core):
        """Inventory core setter"""
        self._validate_str(name)
        self._validate_int(core)
        for d in self._inventory:
            if d['name'] == name:
                d['core'] = core

    def socket(self, name, socket):
        """Inventory socket setter"""
        self._validate_str(name)
        self._validate_str(socket)
        for d in self._inventory:
            if d['name'] == name:
                d['socket'] = socket

    def power_watts(self, name, power_watts):
        """Inventory power_watts setter"""
        self._validate_str(name)
        self._validate_int(power_watts)
        for d in self._inventory:
            if d['name'] == name:
                d['power_watts'] = power_watts
