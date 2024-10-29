# app/schemas.py

from pydantic import BaseModel, Field, computed_field
from narr_mod import StructureType, AnalysisResult

class AnalysisRequest(BaseModel):
    """Запрос на анализ текста"""
    text: str = Field(
        ..., 
        min_length=1, 
        max_length=10000,
        description="Text to analyze"
    )
    structure_type: StructureType = Field(
        default=StructureType.AUTO_DETECT,
        description="Type of narrative structure to analyze"
    )

    @computed_field
    @property
    def structure_name(self) -> str:
        """Человекочитаемое название выбранной структуры"""
        return StructureType.get_display_name(self.structure_type)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "Once upon a time...",
                    "structure_type": "three_act"
                }
            ]
        }
    }

class ErrorResponse(BaseModel):
    """Ответ с ошибкой"""
    error: str = Field(
        ..., 
        min_length=1,
        description="Error message"
    )
    code: int = Field(
        ..., 
        ge=400, 
        le=599,
        description="HTTP error code"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "Text is too long",
                    "code": 400
                }
            ]
        }
    }

class StructureInfo(BaseModel):
    """Информация о доступной структуре анализа"""
    id: StructureType = Field(..., description="Structure type identifier")
    name: str = Field(..., description="Human-readable structure name")
    description: str = Field(..., description="Structure description")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "three_act",
                    "name": "Three-Act Structure",
                    "description": "Classical three-act structure: Setup, Confrontation, Resolution"
                }
            ]
        }
    }

class AvailableStructures(BaseModel):
    """Список доступных структур анализа"""
    structures: list[StructureInfo] = Field(
        ...,
        description="List of available narrative structures"
    )
