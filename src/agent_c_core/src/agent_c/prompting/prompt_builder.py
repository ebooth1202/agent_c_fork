import re
from typing import List, Dict, Any, Set, Optional, TYPE_CHECKING
from agent_c.prompting.prompt_section import PromptSection
from agent_c.util.logging_utils import LoggingManager

if TYPE_CHECKING:
    from agent_c.models.chat_history import ChatSession


class PromptBuilder:
    """
    A class to build a prompt by rendering sections with provided data.

    Attributes:
        sections (List[PromptSection]): A list of PromptSection objects that define the structure of the prompt.
    """

    def __init__(self, notifier,  block_loader, sections: List[PromptSection], tool_sections: List[PromptSection]=None) -> None:
        """
        Initialize the PromptBuilder with a list of sections.

        Args:
            sections (List[PromptSection]): A list of PromptSection objects.
        """
        self.notifier = notifier
        self.block_loader = block_loader
        self.sections: List[PromptSection] = sections
        self.tool_sections: List[PromptSection] = tool_sections or []
        self.logger = LoggingManager(self.__class__.__name__).get_logger()

    @staticmethod
    def _get_template_variables(template: str) -> Set[str]:
        """
        Extract the template variables from a string template.

        Supports:
        - {var}   - standard format string
        - $var    - template string variable
        - ${var}  - template string variable with braces

        Excludes escaped versions:
        - $$var and $${var} (double dollar is an escape)

        Args:
            template (str): The string template to extract variables from.

        Returns:
            Set[str]: A set of variable names found in the template.
        """
        # Combined pattern with three alternatives:
        # 1. ${var} - not preceded by $
        # 2. $var - not preceded by $, valid Python identifier
        # 3. {var} - standard format string
        pattern = r'(?<!\$)\$\{([^}]+)\}|(?<!\$)\$([a-zA-Z_][a-zA-Z0-9_]*)|\{([^}]+)\}'

        matches = re.findall(pattern, template)

        # Flatten tuples (each match has 3 groups, only one is non-empty)and filter out empty strings
        return {group for match in matches for group in match if group}

    async def _render_section(self, section: PromptSection, data: Dict[str, Any]) -> str:
        """
        Render a single prompt section with the provided data.

        Args:
            section (PromptSection): The prompt section to render.
            data (Dict[str, Any]): A dictionary containing the data to render the section with.

        Returns:
            str: The rendered section as a string.

        Raises:
            KeyError: If a required key is missing from the data dictionary.
            Exception: If an unexpected error occurs during rendering.
        """
        try:
            rendered_section: str = await section.render(data)
            template_vars = [v for v in self._get_template_variables(section.template) if v.startswith("block")]
            if len(template_vars):
                return await self._render_section(section, data)
            return rendered_section
        except KeyError as e:
            missing_key = str(e).strip("'")
            message = f"Error rendering section '{section.section_type}': Missing key '{missing_key}'. It will be replaced with it's own name."
            await self.notifier.send_system_message(message, "warning")
            data[missing_key] = missing_key
            return await self._render_section(section, data)

    async def render(self, data: Dict[str, Any], tool_sections: Optional[List[PromptSection]] = None) -> str:
        """
        Render the prompt sections with the provided data.

        Args:
            data (Dict[str, Any]): A dictionary containing the data to render the sections with.
            tool_sections (Optional[List[PromptSection]]): A list of prompt sections to use in the rendering process
                                                           instead of the active tool sections from the toolchest
        Returns:
            str: The rendered prompt as a string.

        Raises:
            KeyError: If a required key is missing from the data dictionary.
            Exception: If an unexpected error occurs during rendering.
        """
        rendered_sections: List[str] = []
        if tool_sections is None:
            tool_sections = self.tool_sections

        section_lists = [self.sections, tool_sections]
        section_list_titles= ["Core Operating Guidelines", "Tool Operation Guidelines / Output"]
        chat_session: 'ChatSession' = data.get("chat_session")
        chat_meta = chat_session.metadata
        all_sections = self.sections + tool_sections

        for section in all_sections:
            try:
                dyn_data = await section.get_dynamic_properties(data)
                data = data | dyn_data
                data = await self.load_blocks_for_template(section.template, data )
            except Exception as e:
                self.logger.exception(f"Error loading blocks for section '{section.section_type}': {e}")
                if section.required:
                    await self.notifier.send_system_message(f"Error loading blocks for section '{section.section_type}': {e}.  Interaction aborted", "error")
                    raise

                await self.notifier.send_system_message(f"Error loading blocks for section '{section.section_type}': {e}", "warning")

        for section in all_sections:
            try:
                if section.section_type in chat_meta.get("prompt_section_blocks", ''):
                    data[f"blocks_{section.section_type}_section"] = section.render(data)
            except Exception as e:
                self.logger.exception(f"Error preparing block for section '{section.section_type}': {e}")
                if section.required:
                    await self.notifier.send_system_message(f"Error preparing block for section '{section.section_type}': {e}.  Interaction aborted", "error")
                    raise

                await self.notifier.send_system_message(f"Error preparing block for section '{section.section_type}': {e}", "warning")

        for index, section_list in enumerate(section_lists):
            if len(section_list) == 0:
                continue

            rendered_sections.append(f"# {section_list_titles[index]}\n\n")

            header_prefix = "#" * (index + 1)

            for section in section_list:
                try:
                    if section.section_type in chat_meta.get("prompt_section_blocks", '') or section.section_type in chat_meta.get("skip_prompt_sections", ''):
                        continue

                    rendered_section: Optional[str] = await section.render(data)
                    if rendered_section is not None:
                        rendered_section += "\n\n"
                        if section.render_section_header:
                            rendered_section = f"{header_prefix} {section.name}\n{rendered_section}"

                        rendered_sections.append(rendered_section)
                except Exception as e:
                    self.logger.exception(f"Error rendering section '{section.name}': {e}")
                    if section.required:
                        await self.notifier.send_system_message(f"Error rendering section '{section.name}': {e}.  Interaction aborted", "error")
                        raise

                    await self.notifier.send_system_message(f"Error rendering section '{section.name}': {e}", "warning")

        result = "\n".join(rendered_sections)
        return result

    async def load_blocks_for_template(self, template: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Load blocks for the given template using the block loader.

        Args:
            template (str): The template string to load blocks for.
        """
        template_vars = self._get_template_variables(template)
        for var in template_vars:
            if var.startswith("block_") or var.startswith("blocks_") and var not in data:
                val = await self.block_loader.get_block(var)

                if val is not None:
                    data[var] = val
                    sub_vars = self._get_template_variables(data[var])
                    if len(sub_vars):
                        data = await self.load_blocks_for_template(data[var], data)
                else:
                    data[var] = f"MISSING INSTRUCTION BLOCK `{var}`"
                    await self.notifier.send_system_message(f"Warning! The block '{var}' could not be found.", "warning")

        return data
