import asyncio
import logging
from agent_c_tools.tools.tool_debugger.debug_tool import ToolDebugger

async def run_example():
    """Simple example of how to use the ToolDebugger"""
    # Create the tool tester
    tester = ToolDebugger(log_level=logging.INFO)

    # Setup a weather tool as a simple example
    # tool_opts is how you pass in required keys to, without loading .env
    # tool_opts={'FLASHDOCS_API_KEY': api_key}
    await tester.setup_tool(tool_import_path='agent_c_tools.MarkdownToHtmlReportTools',
                            tool_opts={})

    # Get tool info
    # tester.print_tool_info()

    # Get the correct tool names
    # tool_names = tester.get_available_tool_names()
    # print(f"\nAvailable tool names: {tool_names}")

    # Initialize workspace if needed


    # Run a tool call, pass in parameters.  Format of the tool name is <toolset_name>_<function_name>

    result = await tester.run_tool_test(
        tool_name='generate_md_viewer',
        tool_params={"workspace_start": "//md_tool/test_markdown/",
                     "output_filename": "test_all.html",
                     "title": "Gathering all files test", }
    )

    content = tester.extract_content_from_results(result)
    if content:
        print("Raw content:", content)

    # result = await tester.run_tool_test(
    #     tool_name='generate_custom_md_viewer',
    #     tool_params={
    #         "workspace": "md_tool",
    #         "file_path": "/test_markdown",
    #         "output_filename": "test_custom.html",
    #         "custom_structure": """{
    #             "items": [
    #                 {
    #                     "type": "folder",
    #                     "name": "📋 Document Overview",
    #                     "children": [
    #                         {
    #                             "type": "file",
    #                             "name": "Multi-Function Document",
    #                             "path": "test_overview.md"
    #                         }
    #                     ]
    #                 },
    #                 {
    #                     "type": "folder",
    #                     "name": "🏦 Miscellaneous",
    #                     "children": [
    #                         {
    #                             "type": "folder",
    #                             "name": "custom dir 1",
    #                             "children": [
    #                                 {
    #                                     "type": "file",
    #                                     "name": "Project Guide",
    #                                     "path": "/dir1/02_project-guide.md"
    #                                 }
    #                             ]
    #                         },
    #                         {
    #                             "type": "folder",
    #                             "name": "CUSTOM dir 2a",
    #                             "children": [
    #                                 {
    #                                     "type": "file",
    #                                     "name": "Custom Index",
    #                                     "path": "dir2/01 index.md"
    #                                 },
    #                                 {
    #                                     "type": "file",
    #                                     "name": "Custom FAQ",
    #                                     "path": "dir2/04 faq.md"
    #                                 }
    #                             ]
    #                         }
    #                     ]
    #                 }
    #             ]
    #         }""",
    #         "title": "Custom Markdown Test",
    #
    #     }
    # )
    # content = tester.extract_content_from_results(result)
    # if content:
    #     print("Raw content:", content)

if __name__ == "__main__":
    asyncio.run(run_example())
