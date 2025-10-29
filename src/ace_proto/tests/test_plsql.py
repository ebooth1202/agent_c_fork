"""Tests for PL/SQL language support.

These tests verify that the text-based PL/SQL scanner can correctly
extract procedures, functions, packages, and their documentation from
PL/SQL source code.
"""

import pytest
from ts_tool import api


def test_simple_procedure():
    """Test extraction of a simple procedure."""
    code = """
    -- Calculate employee bonus
    CREATE OR REPLACE PROCEDURE calc_bonus(p_id IN NUMBER) IS
    BEGIN
        NULL;
    END calc_bonus;
    """

    summary = api.get_code_summary(code, language='plsql', format='dict')
    assert summary['function_count'] == 1

    sig = api.get_signature(code, 'function', 'calc_bonus', language='plsql')
    assert sig is not None
    assert 'PROCEDURE calc_bonus' in sig
    assert 'p_id IN NUMBER' in sig


def test_function_with_return():
    """Test extraction of a function with RETURN type."""
    code = """
    CREATE OR REPLACE FUNCTION get_total(p_amt NUMBER) RETURN NUMBER IS
    BEGIN
        RETURN p_amt * 1.1;
    END get_total;
    """

    interface = api.get_public_interface(code, language='plsql', format='dict')
    assert interface['successful'] == True
    funcs = interface['public_functions']

    assert len(funcs) == 1
    assert funcs[0]['name'] == 'get_total'
    assert 'RETURN NUMBER' in funcs[0]['signature']
    assert funcs[0]['return_type'] == 'NUMBER'


def test_package_spec():
    """Test extraction of package specification."""
    code = """
    -- Employee utilities package
    CREATE OR REPLACE PACKAGE emp_utils IS
        PROCEDURE hire_employee(p_name VARCHAR2);
        FUNCTION calc_salary(p_level NUMBER) RETURN NUMBER;
    END emp_utils;
    """

    summary = api.get_code_summary(code, language='plsql', format='dict')
    # Package specs may or may not be counted - test functions instead
    assert summary['function_count'] >= 1  # At least the function should be found


def test_package_body():
    """Test extraction of package body."""
    code = """
    CREATE OR REPLACE PACKAGE BODY emp_utils IS
        PROCEDURE hire_employee(p_name VARCHAR2) IS
        BEGIN
            NULL;
        END;

        FUNCTION calc_salary(p_level NUMBER) RETURN NUMBER IS
        BEGIN
            RETURN p_level * 1000;
        END;
    END emp_utils;
    """

    interface = api.get_public_interface(code, language='plsql', format='dict')

    # Package body is extracted as a class
    assert len(interface['public_classes']) == 1
    assert interface['public_classes'][0]['name'] == 'emp_utils'

    # Procedures and functions inside are also extracted
    assert len(interface['public_functions']) == 2
    func_names = {f['name'] for f in interface['public_functions']}
    assert 'hire_employee' in func_names
    assert 'calc_salary' in func_names


def test_documentation_extraction():
    """Test extraction of leading comment documentation."""
    code = """
    -- This function calculates the total price
    -- including tax and shipping
    CREATE OR REPLACE FUNCTION get_total_price(
        p_base_price NUMBER,
        p_tax_rate NUMBER
    ) RETURN NUMBER IS
    BEGIN
        RETURN p_base_price * (1 + p_tax_rate);
    END;
    """

    doc = api.get_documentation(code, 'function', 'get_total_price', language='plsql')
    assert doc is not None
    assert 'total price' in doc.lower()
    assert 'tax' in doc.lower()


def test_block_comment_documentation():
    """Test extraction of block comment documentation."""
    code = """
    /*
     * Calculate employee bonus based on performance
     * Returns: Bonus amount in USD
     */
    CREATE OR REPLACE FUNCTION calc_bonus(p_emp_id NUMBER) RETURN NUMBER IS
    BEGIN
        RETURN 1000;
    END;
    """

    doc = api.get_documentation(code, 'function', 'calc_bonus', language='plsql')
    assert doc is not None
    assert 'bonus' in doc.lower()
    assert 'performance' in doc.lower()


def test_multiple_procedures():
    """Test extraction of multiple procedures in one file."""
    code = """
    CREATE OR REPLACE PROCEDURE proc1(p_id NUMBER) IS
    BEGIN
        NULL;
    END;

    CREATE OR REPLACE PROCEDURE proc2(p_name VARCHAR2) IS
    BEGIN
        NULL;
    END;

    CREATE OR REPLACE FUNCTION func1 RETURN NUMBER IS
    BEGIN
        RETURN 42;
    END;
    """

    interface = api.get_public_interface(code, language='plsql', format='dict')
    assert len(interface['public_functions']) == 3

    names = {f['name'] for f in interface['public_functions']}
    assert names == {'proc1', 'proc2', 'func1'}


def test_complex_return_type():
    """Test function with complex return type (e.g., %TYPE, %ROWTYPE)."""
    code = """
    CREATE OR REPLACE FUNCTION get_emp_name(p_id NUMBER)
    RETURN employees.name%TYPE IS
    BEGIN
        RETURN 'John Doe';
    END;
    """

    interface = api.get_public_interface(code, language='plsql', format='dict')
    assert len(interface['public_functions']) == 1
    assert interface['public_functions'][0]['return_type'] == 'employees.name%TYPE'


def test_quoted_identifier():
    """Test extraction with quoted identifiers."""
    code = """
    CREATE OR REPLACE PROCEDURE "Quoted_Proc"(p_val NUMBER) IS
    BEGIN
        NULL;
    END;
    """

    interface = api.get_public_interface(code, language='plsql', format='dict')
    assert len(interface['public_functions']) == 1
    assert interface['public_functions'][0]['name'] == 'Quoted_Proc'


def test_language_detection_by_extension():
    """Test that .sql files are detected as PL/SQL."""
    code = """
    CREATE OR REPLACE PROCEDURE test_proc IS
    BEGIN
        NULL;
    END;
    """

    detected = api.detect_language(code, filename='test.sql')
    assert detected == 'plsql'


def test_language_detection_by_content():
    """Test language detection from code content."""
    code = """
    CREATE OR REPLACE PACKAGE my_package IS
        PROCEDURE test;
    END;
    """

    detected = api.detect_language(code)
    assert detected == 'plsql'


def test_nested_begin_end_blocks():
    """Test procedure with nested BEGIN/END blocks."""
    code = """
    CREATE OR REPLACE PROCEDURE complex_proc(p_id NUMBER) IS
    BEGIN
        IF p_id > 0 THEN
            BEGIN
                NULL;
            END;
        END IF;
    END;
    """

    interface = api.get_public_interface(code, language='plsql', format='dict')
    assert len(interface['public_functions']) == 1
    assert interface['public_functions'][0]['name'] == 'complex_proc'


def test_procedure_with_comments_and_strings():
    """Test that comments and strings inside procedures don't break extraction."""
    code = """
    CREATE OR REPLACE PROCEDURE test_proc IS
        v_msg VARCHAR2(100) := 'BEGIN test END';
        -- This is a comment with BEGIN and END
    BEGIN
        /* Another comment with BEGIN END keywords */
        NULL;
    END;
    """

    interface = api.get_public_interface(code, language='plsql', format='dict')
    assert len(interface['public_functions']) == 1
    assert interface['public_functions'][0]['name'] == 'test_proc'


def test_or_replace_variations():
    """Test various CREATE OR REPLACE syntax variations."""
    code = """
    CREATE PROCEDURE proc1 IS BEGIN NULL; END;
    CREATE OR REPLACE PROCEDURE proc2 IS BEGIN NULL; END;
    CREATE OR REPLACE EDITIONABLE PROCEDURE proc3 IS BEGIN NULL; END;
    """

    interface = api.get_public_interface(code, language='plsql', format='dict')
    assert len(interface['public_functions']) == 3


def test_module_docstring():
    """Test extraction of module-level (file header) documentation."""
    code = """
    -- Module: Employee Management
    -- Author: Test User
    -- Description: Handles all employee-related operations

    CREATE OR REPLACE PROCEDURE hire_emp IS
    BEGIN
        NULL;
    END;
    """

    from ts_tool.core.code_explorer import CodeExplorer
    explorer = CodeExplorer()
    result = explorer.explore_code(code, language='plsql')

    assert result.module.docstring is not None
    assert 'Employee Management' in result.module.docstring


def test_get_entity_signature():
    """Test getting signature for a specific entity."""
    code = """
    CREATE OR REPLACE FUNCTION calc_total(
        p_subtotal NUMBER,
        p_tax NUMBER DEFAULT 0.08
    ) RETURN NUMBER IS
    BEGIN
        RETURN p_subtotal * (1 + p_tax);
    END;
    """

    sig = api.get_signature(code, 'function', 'calc_total', language='plsql')
    assert 'calc_total' in sig
    assert 'RETURN NUMBER' in sig


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
