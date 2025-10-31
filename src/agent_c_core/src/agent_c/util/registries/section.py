from pathlib import Path
from typing import Any, Dict, Type, TypeVar, Optional, List
from pydantic import ValidationError

from agent_c.config import locate_config_path
from agent_c.prompting.prompt_section import PromptSection
from agent_c.util.string import to_snake_case


SectionType = TypeVar('SectionType', bound=PromptSection)


class SectionRegistry:
    """Registry for models with section_type field to enable polymorphic deserialization"""
    _model_registry: Dict[str, Type[PromptSection]] = {}
    _sections: Dict[str, PromptSection] = {}

    @classmethod
    def register_section_class(cls, section_class: Type[PromptSection], section_type: str = None) -> Type[PromptSection]:
        """Register a section class with its section_type string"""
        if section_type:
            type_name = section_type
        else:
            # Try to get it from the model's field default
            if hasattr(section_class, 'model_fields') and 'section_type' in section_class.model_fields:
                field = section_class.model_fields['section_type']
                if hasattr(field, 'default') and field.default is not None:
                    type_name = field.default
                else:
                    # Fall back to computed name
                    type_name = to_snake_case(section_class.__name__.removesuffix('Section'))

            else:
                type_name = to_snake_case(section_class.__name__.removesuffix('Section'))

        cls._model_registry[type_name] = section_class
        return section_class

    @classmethod
    def register_section(cls, section_type: str, section_class) -> None:
        """Register a section instance with its section_type string"""
        cls._sections[section_type] = section_class

    @classmethod
    def register_with_section_type(cls, section_type: str):
        """Decorator for manual registration with explicit section_type"""

        def decorator(section_class: Type[PromptSection]) -> Type[PromptSection]:
            return cls.register_section_class(section_class, section_type)

        return decorator

    @classmethod
    def get_model_class(cls, section_type: str, allow_base: Optional[bool] = True) -> Type[PromptSection]:
        """Get a section class by its section_type string"""
        if section_type not in cls._model_registry:
            #if allow_base:
            #    from agent_c.models.prompts.base import BasePromptSection
            #    return BasePromptSection

            raise ValueError(f"Section type '{section_type}' is not registered")

        return cls._model_registry[section_type]

    @classmethod
    def create(cls, section_type: Optional[str] = None, data: Optional[Dict[str, Any]] = None) -> PromptSection:
        """Create a section instance from data dictionary"""
        if section_type is None and data is not None:
            section_type = data.get('section_type')

        if section_type is None:
            raise ValueError("'section_type' is required to create a section instance")

        if data is None:
            if not cls.is_section_registered(section_type):
                raise ValueError(f"No data provided and section_type '{section_type}' is not registered")

        #if section_type in cls._sections:
        #    section = cls._sections[section_type].model_copy(update=data)
        #    if section.changed_on_disk():
        #        from agent_c.config.prompt_section_loader import PromptSectionLoader
        #        return PromptSectionLoader.instance().load_section_from_file(Path(section.path_on_disk))

        if cls.is_section_model_registered(section_type):
            section_class = cls.get_model_class(section_type)
            return section_class(**data)

        # if data:
        #     if data.get('is_tool_section', False):
        #         from agent_c.models.prompts.tool import BaseToolSection
        #         return BaseToolSection(**data)
        #
        #     from agent_c.models.prompts.base import BasePromptSection
        #     return BasePromptSection(**data)

        raise ValueError(f"Section type '{section_type}' is not registered or does not have a model class, and no data provided to create an instance")

    @classmethod
    def is_section_model_registered(cls, section_type: str) -> bool:
        """Check if a section_type is registered"""
        return section_type in cls._model_registry


    @classmethod
    def is_section_registered(cls, section_type: str) -> bool:
        """Check if a section_type is registered"""
        return section_type in cls._model_registry or section_type in cls._sections

    @classmethod
    def list_types(cls) -> list[str]:
        """List all registered section types"""
        keys = list(set(list(cls._model_registry.keys()) + list(cls._sections.keys())))
        keys.sort()
        return keys

    @classmethod
    def prompt_vars(cls) -> Dict[str, List[str]]:
        """Get all registered section models"""
        result = {}
        for key, model in cls._model_registry.items():
           prop_names = model.get_dynamic_property_names()
           if len(prop_names):
               result[key] = prop_names

        return result

    @classmethod
    def export_prompt_vars(cls) -> None:
        """Export all registered section models to a JSON file"""
        import json
        from agent_c.config import locate_config_path
        cfg_path = locate_config_path()
        export_path =Path(cfg_path).joinpath("prompt_section_vars.json")
        prompt_vars = cls.prompt_vars()
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(prompt_vars, f, indent=4)