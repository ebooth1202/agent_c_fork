"""Pytest configuration and shared fixtures for ts_tool tests."""

import pytest
from ts_tool import api


# Helper functions (available automatically in all test files)

def assert_successful_result(result):
    """Assert that a result dictionary indicates success."""
    assert result['successful'] is True, f"Operation failed: {result.get('error_message')}"
    assert result.get('error_message') is None


def assert_has_entity(entities, name, entity_type='any'):
    """Assert that an entity with the given name exists in the list."""
    names = [e['name'] for e in entities] if isinstance(entities, list) else entities
    assert name in names, f"{entity_type.capitalize()} '{name}' not found. Available: {names}"


# Sample code fixtures for different languages

@pytest.fixture
def python_simple_code():
    """Simple Python code for testing."""
    return """
def hello_world():
    '''Say hello to the world.'''
    print("Hello, World!")

class Calculator:
    '''A simple calculator class.'''

    def add(self, a, b):
        '''Add two numbers.'''
        return a + b

    def multiply(self, a, b):
        '''Multiply two numbers.'''
        return a * b
"""


@pytest.fixture
def csharp_simple_code():
    """Simple C# code for testing."""
    return """
using System;

namespace MyApp
{
    /// <summary>
    /// A simple calculator class
    /// </summary>
    public class Calculator
    {
        /// <summary>
        /// Adds two numbers
        /// </summary>
        public int Add(int a, int b)
        {
            return a + b;
        }

        /// <summary>
        /// Multiplies two numbers
        /// </summary>
        public int Multiply(int a, int b)
        {
            return a * b;
        }
    }
}
"""


@pytest.fixture
def java_simple_code():
    """Simple Java code for testing."""
    return """
package com.example;

import java.util.List;

/**
 * A simple calculator class
 */
public class Calculator {

    /**
     * Adds two numbers
     * @param a First number
     * @param b Second number
     * @return The sum
     */
    public int add(int a, int b) {
        return a + b;
    }

    /**
     * Multiplies two numbers
     * @param a First number
     * @param b Second number
     * @return The product
     */
    public int multiply(int a, int b) {
        return a * b;
    }
}
"""


@pytest.fixture
def javascript_simple_code():
    """Simple JavaScript code for testing."""
    return """
/**
 * A simple calculator class
 */
class Calculator {
    /**
     * Adds two numbers
     */
    add(a, b) {
        return a + b;
    }

    /**
     * Multiplies two numbers
     */
    multiply(a, b) {
        return a * b;
    }
}

/**
 * Say hello to the world
 */
function helloWorld() {
    console.log("Hello, World!");
}
"""


@pytest.fixture
def plsql_simple_code():
    """Simple PL/SQL code for testing."""
    return """
-- Calculate employee bonus
CREATE OR REPLACE PROCEDURE calc_bonus(p_id IN NUMBER, p_bonus OUT NUMBER) IS
BEGIN
    SELECT salary * 0.1 INTO p_bonus
    FROM employees
    WHERE employee_id = p_id;
END calc_bonus;

-- Get employee name
CREATE OR REPLACE FUNCTION get_emp_name(p_id IN NUMBER) RETURN VARCHAR2 IS
    v_name VARCHAR2(100);
BEGIN
    SELECT first_name || ' ' || last_name INTO v_name
    FROM employees
    WHERE employee_id = p_id;
    RETURN v_name;
END get_emp_name;
"""
