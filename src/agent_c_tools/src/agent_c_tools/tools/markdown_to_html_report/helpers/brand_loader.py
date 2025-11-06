"""
Brand Configuration Loader

This module handles loading brand configurations from JSON files and applying
them to HTML templates via CSS variables and content injection.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Optional, Any

logger = logging.getLogger(__name__)


class BrandConfig:
    """Represents a brand configuration."""

    def __init__(self, config_data: Dict[str, Any]):
        """
        Initialize brand config from dictionary.

        Args:
            config_data: Parsed JSON brand configuration
        """
        self.name = config_data.get('name', 'Default')
        self.description = config_data.get('description', '')
        self.colors = config_data.get('colors', {})
        self.logo = config_data.get('logo', {})
        self.typography = config_data.get('typography', {})
        self.spacing = config_data.get('spacing', {})
        self.mermaid = config_data.get('mermaid', {})

    def get_css_variables(self) -> str:
        """
        Generate CSS custom properties from brand config.

        Returns:
            CSS string with :root variable definitions
        """
        css_vars = [":root {"]

        # Colors
        for key, value in self.colors.items():
            css_var_name = f"--brand-{key.replace('_', '-')}"
            css_vars.append(f"    {css_var_name}: {value};")

        # Typography
        if self.typography:
            if 'font_family' in self.typography:
                css_vars.append(f"    --brand-font-family: {self.typography['font_family']};")
            if 'headings_font' in self.typography:
                css_vars.append(f"    --brand-headings-font: {self.typography['headings_font']};")
            if 'code_font' in self.typography:
                css_vars.append(f"    --brand-code-font: {self.typography['code_font']};")
            if 'base_size' in self.typography:
                css_vars.append(f"    --brand-base-size: {self.typography['base_size']};")
            if 'heading_weight' in self.typography:
                css_vars.append(f"    --brand-heading-weight: {self.typography['heading_weight']};")
            if 'line_height' in self.typography:
                css_vars.append(f"    --brand-line-height: {self.typography['line_height']};")

        # Spacing
        if self.spacing:
            for key, value in self.spacing.items():
                css_var_name = f"--brand-{key.replace('_', '-')}"
                css_vars.append(f"    {css_var_name}: {value};")

        css_vars.append("}")

        return "\n".join(css_vars)

    def get_logo_html(self) -> str:
        """
        Generate HTML for logo based on configuration.

        Returns:
            HTML string for logo
        """
        logo_type = self.logo.get('type', 'text')

        if logo_type == 'svg' and 'svg_content' in self.logo:
            width = self.logo.get('width', '120px')
            height = self.logo.get('height', '120px')
            return f'<div class="sidebar-logo" style="width: {width}; height: {height}; margin: 0 auto 16px auto;">{self.logo["svg_content"]}</div>'

        elif logo_type == 'text' and 'text' in self.logo:
            font_size = self.logo.get('font_size', '24px')
            color = self.logo.get('color', 'var(--brand-primary)')
            return f'<div class="sidebar-logo-text" style="font-size: {font_size}; color: {color}; font-weight: 600; text-align: center; margin-bottom: 16px;">{self.logo["text"]}</div>'

        elif logo_type == 'image' and 'url' in self.logo:
            width = self.logo.get('width', '120px')
            height = self.logo.get('height', 'auto')
            alt = self.logo.get('alt', self.name)
            return f'<div class="sidebar-logo" style="margin: 0 auto 16px auto;"><img src="{self.logo["url"]}" alt="{alt}" style="width: {width}; height: {height}; display: block; margin: 0 auto;"/></div>'

        # Fallback to text name
        return f'<div class="sidebar-logo-text" style="font-size: 20px; font-weight: 600; text-align: center; margin-bottom: 16px;">{self.name}</div>'

    def get_mermaid_init_js(self) -> str:
        """
        Generate Mermaid initialization JavaScript with brand theme.

        Returns:
            JavaScript string to initialize Mermaid with brand colors
        """
        # Default Mermaid config
        if not self.mermaid:
            return 'mermaid.initialize({startOnLoad: false, theme: "default", securityLevel: "loose", logLevel: 5});'

        # Build config object from brand
        theme = self.mermaid.get('theme', 'base')
        theme_vars = self.mermaid.get('themeVariables', {})

        # Build JavaScript object notation
        js_lines = ["mermaid.initialize({"]
        js_lines.append("    startOnLoad: false,")
        js_lines.append('    securityLevel: "loose",')
        js_lines.append("    logLevel: 5,")
        js_lines.append(f'    theme: "{theme}",')

        if theme_vars:
            js_lines.append("    themeVariables: {")

            # Convert Python dict to JavaScript object
            for i, (key, value) in enumerate(theme_vars.items()):
                comma = "," if i < len(theme_vars) - 1 else ""

                # Handle different value types
                if isinstance(value, str):
                    # Escape single quotes in the value and use double quotes for JS string
                    escaped_value = value.replace('"', '\\"')
                    js_lines.append(f'        {key}: "{escaped_value}"{comma}')
                elif isinstance(value, bool):
                    js_value = "true" if value else "false"
                    js_lines.append(f"        {key}: {js_value}{comma}")
                elif isinstance(value, (int, float)):
                    js_lines.append(f"        {key}: {value}{comma}")
                else:
                    # Default to string representation
                    escaped_value = str(value).replace('"', '\\"')
                    js_lines.append(f'        {key}: "{escaped_value}"{comma}')

            js_lines.append("    }")

        js_lines.append("});")

        return "\n".join(js_lines)


class BrandLoader:
    """Loads and applies brand configurations to templates."""

    def __init__(self, templates_dir: Path):
        """
        Initialize brand loader.

        Args:
            templates_dir: Path to templates directory containing brands/ folder
        """
        self.templates_dir = Path(templates_dir)
        self.brands_dir = self.templates_dir / "brands"
        self._brand_cache: Dict[str, BrandConfig] = {}

    def load_brand(self, brand_name: str = "default") -> Optional[BrandConfig]:
        """
        Load a brand configuration by name.

        Args:
            brand_name: Name of brand config (without .json extension)

        Returns:
            BrandConfig instance or None if not found
        """
        # Check cache first
        if brand_name in self._brand_cache:
            return self._brand_cache[brand_name]

        # Load from file
        brand_file = self.brands_dir / f"{brand_name}.json"

        if not brand_file.exists():
            logger.warning(f"Brand config '{brand_name}' not found at {brand_file}")
            # Try to load default as fallback
            if brand_name != "default":
                logger.info("Falling back to 'default' brand")
                return self.load_brand("default")
            return None

        try:
            with open(brand_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)

            brand_config = BrandConfig(config_data)
            self._brand_cache[brand_name] = brand_config

            logger.info(f"Loaded brand config: {brand_config.name}")
            return brand_config

        except Exception as e:
            logger.error(f"Error loading brand config '{brand_name}': {e}")
            return None

    def apply_brand_to_template(
        self,
        template_html: str,
        brand_name: str = "default"
    ) -> str:
        """
        Apply brand configuration to template HTML.

        Args:
            template_html: Template HTML content
            brand_name: Name of brand to apply

        Returns:
            HTML with brand CSS variables and logo injected
        """
        brand = self.load_brand(brand_name)

        if not brand:
            logger.warning(f"Could not load brand '{brand_name}', using template as-is")
            return template_html

        # Inject CSS variables
        css_vars = brand.get_css_variables()
        if "/* $BRAND_CSS_VARS */" in template_html:
            template_html = template_html.replace("/* $BRAND_CSS_VARS */", css_vars)
        else:
            # Try to inject after <style> tag
            if "<style>" in template_html:
                template_html = template_html.replace(
                    "<style>",
                    f"<style>\n{css_vars}\n"
                )

        # Inject logo
        logo_html = brand.get_logo_html()
        if "<!-- $BRAND_LOGO -->" in template_html:
            template_html = template_html.replace("<!-- $BRAND_LOGO -->", logo_html)

        # Inject Mermaid theme initialization
        mermaid_init_js = brand.get_mermaid_init_js()
        if "/* $MERMAID_THEME_INIT */" in template_html:
            template_html = template_html.replace("/* $MERMAID_THEME_INIT */", mermaid_init_js)

        logger.debug(f"Applied brand '{brand_name}' to template")
        return template_html

    def list_available_brands(self) -> list:
        """
        List all available brand configurations.

        Returns:
            List of brand names (without .json extension)
        """
        if not self.brands_dir.exists():
            return []

        return [
            f.stem for f in self.brands_dir.glob("*.json")
        ]


def load_and_apply_brand(
    template_html: str,
    templates_dir: Path,
    brand_name: str = "default"
) -> str:
    """
    Convenience function to load and apply brand in one step.

    Args:
        template_html: Template HTML content
        templates_dir: Path to templates directory
        brand_name: Name of brand to apply

    Returns:
        HTML with brand applied
    """
    loader = BrandLoader(templates_dir)
    return loader.apply_brand_to_template(template_html, brand_name)
