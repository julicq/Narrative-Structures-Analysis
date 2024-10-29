# narr_mod/base_structure.py

from abc import ABC, abstractmethod
from typing import Any

class BaseStructure(ABC):
    @abstractmethod
    def get_prompt(self, formatted_structure: dict[str, Any]) -> str:
        """Generate prompt for the structure analysis.
        
        Args:
            formatted_structure: Dictionary containing the structure data
            
        Returns:
            str: Generated prompt for analysis
        """
        pass

    @abstractmethod
    def analyze(self, formatted_structure: dict[str, Any]) -> dict[str, Any]:
        """Analyze the given structure.
        
        Args:
            formatted_structure: Dictionary containing the structure data
            
        Returns:
            dict: Analysis results
        """
        pass
