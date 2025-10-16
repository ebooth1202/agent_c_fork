from ts_tool import api


def read_plsql_and_summarize():
    """
    Read C:\agent_workspace\medpro\source_files\PM_Extract.txt as PL/SQL
    and get summary information using ts_tool API
    """
    file_path = r"C:\agent_workspace\medpro\source_files\PM_Extract.txt"

    try:
        # Read the PL/SQL file
        with open(file_path, 'r', encoding='utf-8') as file:
            plsql_content = file.read()

        print(f"Successfully read {len(plsql_content)} characters from {file_path}")

        # Use ts_tool API to get summary of the PL/SQL content
        print("=" * 60)
        print("CODE SUMMARY")
        print("=" * 60)
        summary = api.get_code_summary(plsql_content, language="plsql", filename="PM_Extract.txt", format="markdown")
        print(summary)

        # Use explore_code to get complete structure
        print("\n" + "=" * 60)
        print("COMPLETE CODE EXPLORATION")
        print("=" * 60)
        exploration = api.explore_code(plsql_content, language="plsql", filename="PM_Extract.txt", format="markdown")
        print(exploration)

        # Get module-level documentation
        print("\n" + "=" * 60)
        print("MODULE DOCUMENTATION")
        print("=" * 60)
        module_docs = api.get_documentation(plsql_content, entity_type="module", entity_name="", language="plsql", filename="PM_Extract.txt")
        if module_docs:
            print(module_docs)
        else:
            print("No module-level documentation found.")

        return {
            'summary': summary,
            'exploration': exploration,
            'module_documentation': module_docs
        }

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return None


if __name__ == "__main__":
    # Run the function when script is executed directly
    read_plsql_and_summarize()
