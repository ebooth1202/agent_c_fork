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
    # Test 0: Full folder gathering with DEFAULT brand
    print("\n=== Test 0: Default brand (modern blue/gray) ===")
    result = await tester.run_tool_test(
        tool_name='generate_md_viewer',
        tool_params={
            "workspace_start": "//md_tool/tests/fixtures/test_markdown/",
            "output_filename": "test_default_brand.html",
            "title": "Default Brand Test",
            "brand": "default"
        }
    )
    content = tester.extract_content_from_results(result)
    if content:
        print("✓ Default brand:", content[:100])

    # Test 0b: Full folder gathering with CENTRIC brand
    print("\n=== Test 0b: Centric brand (purple/orange) ===")
    result0b = await tester.run_tool_test(
        tool_name='generate_md_viewer',
        tool_params={
            "workspace_start": "//md_tool/tests/fixtures/test_markdown/",
            "output_filename": "test_centric_brand.html",
            "title": "Centric Brand Test",
            "brand": "centric"
        }
    )
    content0b = tester.extract_content_from_results(result0b)
    if content0b:
        print("✓ Centric brand:", content0b[:100])

    # Test 1: Backward compatible - relative paths with workspace
    print("\n=== Test 1: Relative paths with workspace (backward compatible) ===")
    result1 = await tester.run_tool_test(
        tool_name='generate_custom_md_viewer',
        tool_params={
            "workspace": "md_tool/tests/fixtures/test_markdown",
            "output_filename": "//md_tool/tests/output/test_custom_relative.html",
            "custom_structure": """{
                "items": [
                    {
                        "type": "folder",
                        "name": "📋 Document Overview",
                        "children": [
                            {
                                "type": "file",
                                "name": "Multi-Function Document",
                                "path": "test_overview.md"
                            }
                        ]
                    }
                ]
            }""",
            "title": "Test 1: Relative Paths",
        }
    )
    content1 = tester.extract_content_from_results(result1)
    if content1:
        print("✓ Test 1 passed:", content1[:100])

    # Test 2: Fully qualified paths only (no workspace)
    print("\n=== Test 2: Fully qualified UNC paths (no workspace) ===")
    result2 = await tester.run_tool_test(
        tool_name='generate_custom_md_viewer',
        tool_params={
            # No workspace parameter!
            "output_filename": "//md_tool/tests/output/test_custom_qualified.html",
            "custom_structure": """{
                "items": [
                    {
                        "type": "folder",
                        "name": "🏦 Fully Qualified Paths",
                        "children": [
                            {
                                "type": "file",
                                "name": "Project Guide",
                                "path": "//md_tool/tests/fixtures/test_markdown/dir1/02_project-guide.md"
                            },
                            {
                                "type": "file",
                                "name": "Custom Index",
                                "path": "//md_tool/tests/fixtures/test_markdown/dir2/01 index.md"
                            }
                        ]
                    }
                ]
            }""",
            "title": "Test 2: Fully Qualified Paths",
        }
    )
    content2 = tester.extract_content_from_results(result2)
    if content2:
        print("✓ Test 2 passed:", content2[:100])

    # Test 3: Hybrid - mix of fully qualified and relative paths
    print("\n=== Test 3: Hybrid (mix of both path types) ===")
    result3 = await tester.run_tool_test(
        tool_name='generate_custom_md_viewer',
        tool_params={
            "workspace": "md_tool/tests/fixtures/test_markdown",  # For relative paths
            "output_filename": "//md_tool/tests/output/test_custom_hybrid.html",
            "custom_structure": """{
                "items": [
                    {
                        "type": "folder",
                        "name": "📋 Document Overview",
                        "children": [
                            {
                                "type": "file",
                                "name": "Overview (relative)",
                                "path": "test_overview.md"
                            }
                        ]
                    },
                    {
                        "type": "folder",
                        "name": "🏦 Miscellaneous",
                        "children": [
                            {
                                "type": "file",
                                "name": "Project Guide (fully qualified)",
                                "path": "//md_tool/tests/fixtures/test_markdown/dir1/02_project-guide.md"
                            },
                            {
                                "type": "file",
                                "name": "Index (relative)",
                                "path": "dir2/01 index.md"
                            },
                            {
                                "type": "file",
                                "name": "FAQ (fully qualified)",
                                "path": "//md_tool/tests/fixtures/test_markdown/dir2/04 faq.md"
                            }
                        ]
                    }
                ]
            }""",
            "title": "Test 3: Hybrid Paths",
        }
    )
    content3 = tester.extract_content_from_results(result3)
    if content3:
        print("✓ Test 3 passed:", content3[:100])

if __name__ == "__main__":
    asyncio.run(run_example())
