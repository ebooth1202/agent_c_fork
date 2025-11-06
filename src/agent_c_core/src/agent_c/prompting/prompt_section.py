import inspect
from functools import wraps
from string import Template

from typing import Callable, Any, Dict, List, TYPE_CHECKING, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from agent_c.util import to_snake_case
from agent_c.util.logging_utils import LoggingManager

if TYPE_CHECKING:
    from agent_c.models.chat_history import ChatSession


def property_bag_item(func: Callable) -> Callable:
    """
    Decorator to mark a method as a dynamic property for a PromptSection.
    The method marked with this decorator will be included in the dynamic properties.

    Args:
        func (Callable): The method to be marked as a dynamic property.

    Returns:
        Callable: The wrapped method with an additional attribute to indicate it's a property bag item.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    wrapper.is_property_bag_item = True
    return wrapper


class PromptSection(BaseModel):
    """
    A class representing a section of a prompt with dynamic properties.

    Attributes:
        name (str): The name of the section.
        template (str): The template string for the section.
        render_section_header (bool): Flag to determine if a header should be rendered for the section.
        required (bool): Flag to determine if the section is required.
    """
    section_type: str = Field(None, description="The type of the prompt section, used for registration and identification.")
    model_config = ConfigDict(arbitrary_types_allowed=True, protected_namespaces=())
    name: str
    template: str
    render_section_header: bool = True
    required: bool = False

    def __init__(self, **data: Any):
        """
        Initialize the PromptSection with the provided data.

        Args:
            **data: Arbitrary keyword arguments to initialize the section.
        """
        super().__init__(**data)
        self._logger = LoggingManager(self.__class__.__name__).get_logger()

    @model_validator(mode='after')
    def validate_section_type(self):
        if self.section_type is None:
            self.section_type  = to_snake_case(self.__class__.__name__.removesuffix('Section'))
        return self


    @classmethod
    def get_dynamic_property_names(cls) -> List[str]:
        """
        Retrieves the names of all dynamic properties defined in the PromptSection.

        Returns:
            List[str]: A list of dynamic property names.
        """
        dynamic_prop_names: List[str] = []
        for attr_name in dir(cls):
            # Skip internal or special attributes
            if attr_name.startswith('_'):
                continue

            attr = getattr(cls, attr_name)
            if callable(attr) and getattr(attr, 'is_property_bag_item', False):
                dynamic_prop_names.append(attr_name)
        return dynamic_prop_names

    async def get_dynamic_properties(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieves the dynamic properties of the PromptSection.

        Args:
            data: Dict[str, Any]: The data dictionary to pass to attributes that accept it

        Returns:
            Dict[str, Any]: A dictionary of dynamic property names and their values.
        """
        dynamic_props: Dict[str, Any] = {}
        for attr_name in dir(self):
            # Skip internal or special attributes
            if attr_name.startswith('_'):
                continue

            attr = getattr(self, attr_name)
            if callable(attr) and getattr(attr, 'is_property_bag_item', False):
                try:
                    sig = inspect.signature(attr)
                    # If it has exactly one parameter (excluding 'self'), pass data
                    param_count = len(sig.parameters)
                    if param_count == 0:
                        dynamic_props[attr_name] = await attr()
                    elif param_count == 1:
                        dynamic_props[attr_name] = await attr(data)
                    else:
                        self._logger.exception(f"Dynamic property '{attr_name}' has too many parameters: {param_count}")
                except Exception as e:
                    self._logger.exception(f"Error getting dynamic property '{attr_name}': {e}")
        return dynamic_props

    async def render(self, data: Dict[str, Any]) -> Optional[str]:
        template: Template = Template(self.template)
        result = template.substitute(data)
        return result

    def __init_subclass__(cls, **kwargs):
        """Automatically register subclasses"""
        super().__init_subclass__(**kwargs)
        if cls.__name__.startswith('Base'):
            return

        from agent_c.util.registries.section import SectionRegistry
        SectionRegistry.register_section_class(cls)