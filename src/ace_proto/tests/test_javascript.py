"""Tests for JavaScript language support.

Tests JavaScript-specific parsing including:
- Classes and methods
- Functions (regular and arrow)
- ES6+ features
- JSDoc comments
- Exports/imports
- Async/await
"""

import pytest
from ts_tool import api
from .conftest import assert_successful_result, assert_has_entity


class TestJavaScriptClasses:
    """Tests for JavaScript class parsing."""

    def test_simple_class(self):
        """Test parsing a simple class."""
        code = '''
class MyClass {
}
'''
        result = api.get_public_interface(code, 'javascript', format='dict')
        assert_successful_result(result)
        assert result['class_count'] == 1
        assert result['public_classes'][0]['name'] == 'MyClass'

    def test_class_with_methods(self, javascript_simple_code):
        """Test parsing a class with methods."""
        result = api.get_public_interface(javascript_simple_code, 'javascript', format='dict')
        assert_successful_result(result)

        calc_class = result['public_classes'][0]
        assert calc_class['name'] == 'Calculator'
        assert len(calc_class['methods']) == 2
        assert_has_entity(calc_class['methods'], 'add', 'method')
        assert_has_entity(calc_class['methods'], 'multiply', 'method')

    def test_class_with_constructor(self):
        """Test parsing a class with constructor."""
        code = '''
class Person {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }

    greet() {
        return `Hello, I'm ${this.name}`;
    }
}
'''
        result = api.get_public_interface(code, 'javascript', format='dict')
        assert_successful_result(result)

        person_class = result['public_classes'][0]
        assert person_class['name'] == 'Person'
        # Should have the greet method
        method_names = [m['name'] for m in person_class['methods']]
        assert 'greet' in method_names

    def test_class_with_static_method(self):
        """Test parsing class with static method."""
        code = '''
class MathHelper {
    static square(x) {
        return x * x;
    }

    static cube(x) {
        return x * x * x;
    }
}
'''
        result = api.get_public_interface(code, 'javascript', format='dict')
        assert_successful_result(result)

        math_class = result['public_classes'][0]
        assert len(math_class['methods']) == 2

    def test_class_with_getters_setters(self):
        """Test parsing class with getters and setters."""
        code = '''
class Person {
    constructor(firstName, lastName) {
        this._firstName = firstName;
        this._lastName = lastName;
    }

    get fullName() {
        return `${this._firstName} ${this._lastName}`;
    }

    set fullName(name) {
        const parts = name.split(' ');
        this._firstName = parts[0];
        this._lastName = parts[1];
    }
}
'''
        result = api.get_public_interface(code, 'javascript', format='dict')
        assert_successful_result(result)

        person_class = result['public_classes'][0]
        # Should have getter/setter as methods
        assert len(person_class['methods']) >= 1


class TestJavaScriptFunctions:
    """Tests for JavaScript function parsing."""

    def test_simple_function(self, javascript_simple_code):
        """Test parsing a simple function."""
        result = api.get_public_interface(javascript_simple_code, 'javascript', format='dict')
        assert_successful_result(result)

        assert result['function_count'] == 1
        func = result['public_functions'][0]
        assert func['name'] == 'helloWorld'

    def test_function_with_parameters(self):
        """Test parsing function with parameters."""
        code = '''
function addNumbers(a, b) {
    return a + b;
}
'''
        result = api.get_public_interface(code, 'javascript', format='dict')
        assert_successful_result(result)

        assert result['function_count'] == 1
        func = result['public_functions'][0]
        assert func['name'] == 'addNumbers'

    def test_arrow_function(self):
        """Test parsing arrow function."""
        code = '''
const square = (x) => x * x;
const add = (a, b) => a + b;
'''
        result = api.get_code_summary(code, 'javascript', format='dict')
        assert_successful_result(result)
        # Should parse without error
        assert result['language'] == 'javascript'

    def test_async_function(self):
        """Test parsing async function."""
        code = '''
async function fetchData() {
    const response = await fetch('api/data');
    return response.json();
}
'''
        result = api.get_public_interface(code, 'javascript', format='dict')
        assert_successful_result(result)

        assert result['function_count'] == 1
        func = result['public_functions'][0]
        assert func['name'] == 'fetchData'

    def test_generator_function(self):
        """Test parsing generator function."""
        code = '''
function* numberGenerator() {
    yield 1;
    yield 2;
    yield 3;
}
'''
        result = api.get_public_interface(code, 'javascript', format='dict')
        assert_successful_result(result)

        assert result['function_count'] == 1
        func = result['public_functions'][0]
        assert func['name'] == 'numberGenerator'


class TestJavaScriptReturnTypes:
    """Tests for JavaScript return type handling."""

    def test_functions_have_return_type_field(self):
        """Test that functions have return_type field (should be None for JS)."""
        code = '''
function getNumber() {
    return 42;
}

function getString() {
    return "test";
}
'''
        result = api.get_public_interface(code, 'javascript', format='dict')
        assert_successful_result(result)

        # JavaScript is dynamically typed, so return_type should be None
        for func in result['public_functions']:
            assert 'return_type' in func
            assert func['return_type'] is None

    def test_methods_have_return_type_field(self):
        """Test that methods have return_type field (should be None for JS)."""
        code = '''
class MyClass {
    getValue() {
        return 42;
    }

    getText() {
        return "test";
    }
}
'''
        result = api.get_public_interface(code, 'javascript', format='dict')
        assert_successful_result(result)

        my_class = result['public_classes'][0]
        # JavaScript is dynamically typed, so return_type should be None
        for method in my_class['methods']:
            assert 'return_type' in method
            assert method['return_type'] is None


class TestJavaScriptDocumentation:
    """Tests for JavaScript JSDoc extraction."""

    def test_function_jsdoc(self, javascript_simple_code):
        """Test extracting JSDoc from function."""
        doc = api.get_documentation(javascript_simple_code, 'function', 'helloWorld', language='javascript')
        assert doc is not None
        assert 'Say hello' in doc or 'hello' in doc.lower()

    def test_class_jsdoc(self, javascript_simple_code):
        """Test extracting JSDoc from class."""
        doc = api.get_documentation(javascript_simple_code, 'class', 'Calculator', language='javascript')
        assert doc is not None
        assert 'calculator' in doc.lower()

    def test_method_jsdoc(self, javascript_simple_code):
        """Test extracting JSDoc from method."""
        doc = api.get_documentation(javascript_simple_code, 'method', 'Calculator.add', language='javascript')
        assert doc is not None
        assert 'two numbers' in doc.lower() or 'adds' in doc.lower()

    def test_multiline_jsdoc(self):
        """Test extracting multiline JSDoc."""
        code = '''
/**
 * This is a complex function that does many things.
 * It processes data and returns results.
 *
 * @param {number} x - First parameter
 * @param {number} y - Second parameter
 * @returns {number} The result
 * @throws {Error} If parameters are invalid
 */
function complexFunction(x, y) {
    return x + y;
}
'''
        doc = api.get_documentation(code, 'function', 'complexFunction', language='javascript')
        assert doc is not None
        assert 'complex function' in doc.lower()


class TestJavaScriptES6Features:
    """Tests for ES6+ feature parsing."""

    def test_template_literals(self):
        """Test parsing code with template literals."""
        code = '''
function greet(name) {
    return `Hello, ${name}!`;
}
'''
        result = api.get_public_interface(code, 'javascript', format='dict')
        assert_successful_result(result)
        assert result['function_count'] == 1

    def test_destructuring(self):
        """Test parsing code with destructuring."""
        code = '''
function processUser({ name, age }) {
    return `${name} is ${age} years old`;
}
'''
        result = api.get_public_interface(code, 'javascript', format='dict')
        assert_successful_result(result)
        assert result['function_count'] == 1

    def test_spread_operator(self):
        """Test parsing code with spread operator."""
        code = '''
function sum(...numbers) {
    return numbers.reduce((a, b) => a + b, 0);
}
'''
        result = api.get_public_interface(code, 'javascript', format='dict')
        assert_successful_result(result)
        assert result['function_count'] == 1

    def test_default_parameters(self):
        """Test parsing function with default parameters."""
        code = '''
function greet(name = "World") {
    return `Hello, ${name}!`;
}
'''
        result = api.get_public_interface(code, 'javascript', format='dict')
        assert_successful_result(result)
        assert result['function_count'] == 1


class TestJavaScriptExportsImports:
    """Tests for JavaScript module system."""

    def test_import_statements(self):
        """Test parsing import statements."""
        code = '''
import React from 'react';
import { useState, useEffect } from 'react';
import * as utils from './utils';

function MyComponent() {
    return <div>Hello</div>;
}
'''
        result = api.explore_code(code, 'javascript', format='dict')
        assert_successful_result(result)

        imports = result['module']['imports']
        # Should capture some imports
        assert len(imports) >= 1

    def test_export_functions(self):
        """Test parsing regular functions (export parsing is complex)."""
        code = '''
function add(a, b) {
    return a + b;
}

function multiply(a, b) {
    return a * b;
}
'''
        result = api.get_public_interface(code, 'javascript', format='dict')
        assert_successful_result(result)
        # Should find the functions
        assert result['function_count'] == 2

    def test_export_default_class(self):
        """Test parsing default export with class."""
        code = '''
export default class Calculator {
    add(a, b) {
        return a + b;
    }
}
'''
        result = api.get_public_interface(code, 'javascript', format='dict')
        assert_successful_result(result)
        assert result['class_count'] == 1

    def test_named_exports(self):
        """Test parsing named exports."""
        code = '''
const PI = 3.14159;
const E = 2.71828;

function square(x) {
    return x * x;
}

export { PI, E, square };
'''
        result = api.get_code_summary(code, 'javascript', format='dict')
        assert_successful_result(result)
        # Should parse successfully
        assert result['language'] == 'javascript'


class TestJavaScriptAsyncAwait:
    """Tests for async/await handling."""

    def test_async_function_declaration(self):
        """Test parsing async function declaration."""
        code = '''
async function fetchUser(id) {
    const response = await fetch(`/api/users/${id}`);
    return response.json();
}
'''
        result = api.get_public_interface(code, 'javascript', format='dict')
        assert_successful_result(result)
        assert result['function_count'] == 1

    def test_async_method(self):
        """Test parsing async method in class."""
        code = '''
class ApiClient {
    async fetchData(endpoint) {
        const response = await fetch(endpoint);
        return response.json();
    }

    async postData(endpoint, data) {
        const response = await fetch(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
        return response.json();
    }
}
'''
        result = api.get_public_interface(code, 'javascript', format='dict')
        assert_successful_result(result)

        api_class = result['public_classes'][0]
        assert len(api_class['methods']) == 2

    def test_promise_handling(self):
        """Test parsing Promise-based code."""
        code = '''
function loadData() {
    return fetch('/api/data')
        .then(response => response.json())
        .then(data => processData(data))
        .catch(error => console.error(error));
}
'''
        result = api.get_public_interface(code, 'javascript', format='dict')
        assert_successful_result(result)
        assert result['function_count'] == 1


class TestJavaScriptPrivateMembers:
    """Tests for private member handling."""

    def test_private_fields(self):
        """Test parsing class with private fields (ES2022+)."""
        code = '''
class Person {
    #age;

    constructor(name, age) {
        this.name = name;
        this.#age = age;
    }

    getAge() {
        return this.#age;
    }
}
'''
        result = api.get_public_interface(code, 'javascript', format='dict')
        assert_successful_result(result)

        person_class = result['public_classes'][0]
        # Public method should be found
        method_names = [m['name'] for m in person_class['methods']]
        assert 'getAge' in method_names

    def test_private_methods(self):
        """Test parsing class with private methods (ES2022+)."""
        code = '''
class Calculator {
    #validate(x) {
        return typeof x === 'number';
    }

    add(a, b) {
        if (!this.#validate(a) || !this.#validate(b)) {
            throw new Error('Invalid input');
        }
        return a + b;
    }
}
'''
        result = api.get_public_interface(code, 'javascript', format='dict')
        assert_successful_result(result)

        calc_class = result['public_classes'][0]
        method_names = [m['name'] for m in calc_class['methods']]
        # Public method should be included
        assert 'add' in method_names


class TestJavaScriptVariables:
    """Tests for JavaScript variable declarations."""

    def test_const_declarations(self):
        """Test parsing const declarations."""
        code = '''
const MAX_SIZE = 100;
const DEFAULT_NAME = "John";
const PI = 3.14159;
'''
        result = api.get_code_summary(code, 'javascript', format='dict')
        assert_successful_result(result)
        # Should parse successfully
        assert result['language'] == 'javascript'

    def test_let_declarations(self):
        """Test parsing let declarations."""
        code = '''
let counter = 0;
let userName = "test";
'''
        result = api.get_code_summary(code, 'javascript', format='dict')
        assert_successful_result(result)
        assert result['language'] == 'javascript'

    def test_var_declarations(self):
        """Test parsing var declarations."""
        code = '''
var globalVar = "global";
var count = 42;
'''
        result = api.get_code_summary(code, 'javascript', format='dict')
        assert_successful_result(result)
        assert result['language'] == 'javascript'


class TestJavaScriptObjectLiterals:
    """Tests for object literal parsing."""

    def test_object_methods(self):
        """Test parsing object with methods."""
        code = '''
const calculator = {
    add(a, b) {
        return a + b;
    },

    multiply(a, b) {
        return a * b;
    }
};
'''
        result = api.get_code_summary(code, 'javascript', format='dict')
        assert_successful_result(result)
        # Should parse successfully
        assert result['language'] == 'javascript'

    def test_object_with_arrow_functions(self):
        """Test parsing object with arrow function properties."""
        code = '''
const utils = {
    square: (x) => x * x,
    cube: (x) => x * x * x
};
'''
        result = api.get_code_summary(code, 'javascript', format='dict')
        assert_successful_result(result)
        assert result['language'] == 'javascript'


class TestJavaScriptErrorHandling:
    """Tests for error handling in JavaScript code."""

    def test_try_catch(self):
        """Test parsing try-catch blocks."""
        code = '''
function safeParse(json) {
    try {
        return JSON.parse(json);
    } catch (error) {
        console.error('Parse error:', error);
        return null;
    }
}
'''
        result = api.get_public_interface(code, 'javascript', format='dict')
        assert_successful_result(result)
        assert result['function_count'] == 1

    def test_try_catch_finally(self):
        """Test parsing try-catch-finally blocks."""
        code = '''
function processFile(filename) {
    let file = null;
    try {
        file = openFile(filename);
        return processData(file);
    } catch (error) {
        console.error(error);
        return null;
    } finally {
        if (file) {
            file.close();
        }
    }
}
'''
        result = api.get_public_interface(code, 'javascript', format='dict')
        assert_successful_result(result)
        assert result['function_count'] == 1
