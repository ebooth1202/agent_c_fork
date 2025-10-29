# Unified Web Search Tools - Primary interface for all web search functionality
from .tool import WebSearchTools

# Legacy individual tools - DEPRECATED
# These tools are deprecated and will be removed in a future version.
# Use WebSearchTools instead for all web search functionality.

# Tools used by engine adapters (required for unified system)
from .google_serp import GoogleSerpTools  # Used by GoogleSerpEngine
from .hacker_news import HackerNewsTools  # Used by HackerNewsEngine
from .news_api import NewsApiTools  # Used by NewsApiEngine
from .tavily_research import TavilyResearchTools  # Used by TavilyEngine
from .wikipedia.tool import WikipediaTools  # Used by WikipediaEngine



# Export main interface
__all__ = ['WebSearchTools']

# Backward compatibility exports (deprecated)
__all__.extend([
    'GoogleSerpTools', 'HackerNewsTools', 'NewsApiTools', 
    'TavilyResearchTools', 'WikipediaTools',
    'GoogleTrendsTools', 'SeekingAlphaTools'
])
