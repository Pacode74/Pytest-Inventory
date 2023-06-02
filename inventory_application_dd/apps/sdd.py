from inventory_application_store_multiple_items.apps.storage import Storage


class SDD(Storage):
    def interface(self, name, interface):
        """Interface setter"""
        self._validate_str(name)
        self._validate_str(interface)
        for d in self._inventory:
            if d['name'] == name:
                d['interface'] = interface