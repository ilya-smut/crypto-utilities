from enum import Enum

class UtilityCodes(Enum):
    MOD = 1
    GCD = 2
    EXTEU = 3
    MODINV = 4
    FASTPOV = 5

class SavedValues:
    def __init__(self):
        self.stored_values = dict() # storing as strings for HTML use

    def add_value(self, name: str, value: str|int):
        if len(name) < 1:
            return 1
        if type(value) is str:
            try:
                try_inting = int(value)
                self.stored_values[name] = value
                return 0
            except ValueError:
                return 1
        elif type(value) is int:
            self.stored_values[name] = str(value)
            return 0
        return 1
    
    def get_value_str(self, name: str):
        return self.stored_values.get(name, None)

    def get_value_int(self, name: str):
        value = self.stored_values.get(name, None)
        if value:
            return int(value)
        
    def list_saved_names(self):
        return list(self.stored_values.keys)
    
    def get_saved_pairs(self):
        return self.stored_values
    
    def remove_saved(self, name):
        if name in self.stored_values:
            del self.stored_values[name]


class ResponseData:
    def __init__(self):
        self.data = dict()
    
    def add_global(self, appendix: dict, subkey=""):
        if subkey:
            if subkey in self.data:
                self.data = self.data[subkey] | appendix
            else:
                self.data[subkey] = appendix
        else:
            self.data = self.data | appendix
        return self

    def add_result(self, appendix: dict):
        if "results" not in self.data:
            self.data["results"] = dict()
        self.data["results"] = self.data["results"] | appendix
        return self
    
    def add_saved_value(self, appendix: dict, replace=False):
        if "saved_values" not in self.data:
            self.data["saved_values"] = dict()
        if not replace:
            self.data["saved_values"] = self.data["saved_values"] | appendix
        else:
            self.data["saved_values"] = appendix
        return self
    
    def set_combo_op(self, op: str):
        self.data["combo_op"] = op
        return self

    
    def values(self):
        return self.data