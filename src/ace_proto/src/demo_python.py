from ts_tool import api

file_path = r"C:\Users\justj\PycharmProjects\agent_c_framework\src\agent_c_tools\src\agent_c_tools\tools\workspace\tool.py"

with open(file_path, 'r', encoding='utf-8') as file:
    code = file.read()

language='python'

print(f"Summary{'='* 40}")
summary = api.get_code_summary(code, language=language, filename=file_path, format="markdown")
print(summary)
#
print(f"Code Context{'='* 40}")
public_interface = api.get_code_context(code, language=language, filename=file_path, format="markdown", style="standard")
print(public_interface)
#
print(f"Public Interface{'='* 40}")
public_interface = api.get_public_interface(code, language=language, filename=file_path, format="markdown")
print(public_interface)

#
print(f"Explore{'='* 40}")
exploration = api.explore_code(code, language=language, filename=file_path, format="markdown", style="standard")
print(exploration)

print(f"Get Entity{'='* 40}")
result = api.get_entity(code, entity_type='method', entity_name='WorkspaceTools.find_workspace_by_name', filename=file_path, format="markdown", detail_level="full")
print(result)


signature = api.get_signature(code, entity_type="method", entity_name='WorkspaceTools.find_workspace_by_name', filename=file_path)
print(signature)

docs = api.get_documentation(code, entity_type="method", entity_name='WorkspaceTools.find_workspace_by_name', filename=file_path)
print(docs)

sc = api.get_source_code(code, entity_type="method", entity_name='WorkspaceTools.find_workspace_by_name', filename=file_path)
print(sc)




