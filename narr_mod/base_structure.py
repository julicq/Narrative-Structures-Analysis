# narr_mod/base_structure.py

class BaseStructure:
    def get_prompt(self, formatted_structure):
        raise NotImplementedError("Subclasses must implement get_prompt method")

    def analyze(self, formatted_structure):
        raise NotImplementedError("Subclasses must implement analyze method")