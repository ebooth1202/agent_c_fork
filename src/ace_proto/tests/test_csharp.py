"""Tests for C# language support.

Tests C#-specific parsing including:
- Classes, interfaces, structs, enums
- Methods with XML documentation
- Properties and fields
- Namespaces
- Access modifiers
- Using directives
"""

import pytest
from ts_tool import api
from .conftest import assert_successful_result, assert_has_entity


class TestCSharpClasses:
    """Tests for C# class parsing."""

    def test_simple_class(self):
        """Test parsing a simple class."""
        code = '''
using System;

namespace MyApp
{
    public class MyClass
    {
    }
}
'''
        result = api.get_public_interface(code, 'c_sharp', format='dict')
        assert_successful_result(result)
        assert result['class_count'] == 1
        assert result['public_classes'][0]['name'] == 'MyClass'

    def test_class_with_methods(self, csharp_simple_code):
        """Test parsing a class with methods."""
        result = api.get_public_interface(csharp_simple_code, 'c_sharp', format='dict')
        assert_successful_result(result)

        calc_class = result['public_classes'][0]
        assert calc_class['name'] == 'Calculator'
        assert len(calc_class['methods']) == 2
        assert_has_entity(calc_class['methods'], 'Add', 'method')
        assert_has_entity(calc_class['methods'], 'Multiply', 'method')

    def test_class_with_constructor(self):
        """Test parsing a class with constructor."""
        code = '''
public class Person
{
    public Person(string name, int age)
    {
        Name = name;
        Age = age;
    }

    public string Name { get; set; }
    public int Age { get; set; }
}
'''
        result = api.get_public_interface(code, 'c_sharp', format='dict')
        assert_successful_result(result)

        person_class = result['public_classes'][0]
        assert person_class['name'] == 'Person'

    def test_interface(self):
        """Test parsing an interface."""
        code = '''
public interface ICalculator
{
    int Add(int a, int b);
    int Multiply(int a, int b);
}
'''
        result = api.get_public_interface(code, 'c_sharp', format='dict')
        assert_successful_result(result)

        assert result['class_count'] == 1
        interface = result['public_classes'][0]
        assert interface['name'] == 'ICalculator'
        assert len(interface['methods']) == 2

    def test_struct(self):
        """Test parsing a struct."""
        code = '''
public struct Point
{
    public int X { get; set; }
    public int Y { get; set; }

    public Point(int x, int y)
    {
        X = x;
        Y = y;
    }
}
'''
        result = api.get_public_interface(code, 'c_sharp', format='dict')
        assert_successful_result(result)

        assert result['class_count'] == 1
        struct = result['public_classes'][0]
        assert struct['name'] == 'Point'

    def test_enum(self):
        """Test parsing an enum."""
        code = '''
public enum Color
{
    Red,
    Green,
    Blue
}
'''
        result = api.get_code_summary(code, 'c_sharp', format='dict')
        assert_successful_result(result)
        # Enums should be counted
        assert result['class_count'] >= 1


class TestCSharpMethods:
    """Tests for C# method parsing."""

    def test_method_with_return_type(self, csharp_simple_code):
        """Test that methods have return types extracted."""
        result = api.get_public_interface(csharp_simple_code, 'c_sharp', format='dict')
        assert_successful_result(result)

        calc_class = result['public_classes'][0]
        add_method = next(m for m in calc_class['methods'] if m['name'] == 'Add')

        # Check that return_type field exists and is extracted
        assert 'return_type' in add_method
        assert add_method['return_type'] == 'int'

    def test_void_method(self):
        """Test parsing a void method."""
        code = '''
public class Logger
{
    public void Log(string message)
    {
        Console.WriteLine(message);
    }
}
'''
        result = api.get_public_interface(code, 'c_sharp', format='dict')
        assert_successful_result(result)

        logger_class = result['public_classes'][0]
        log_method = logger_class['methods'][0]
        assert log_method['name'] == 'Log'
        assert log_method['return_type'] == 'void'

    def test_generic_method(self):
        """Test parsing a generic method."""
        code = '''
public class GenericClass
{
    public T GetValue<T>(T defaultValue)
    {
        return defaultValue;
    }
}
'''
        result = api.get_public_interface(code, 'c_sharp', format='dict')
        assert_successful_result(result)

        generic_class = result['public_classes'][0]
        assert len(generic_class['methods']) == 1
        assert generic_class['methods'][0]['name'] == 'GetValue'

    def test_static_method(self):
        """Test parsing a static method."""
        code = '''
public class MathHelper
{
    public static int Square(int x)
    {
        return x * x;
    }
}
'''
        result = api.get_public_interface(code, 'c_sharp', format='dict')
        assert_successful_result(result)

        math_class = result['public_classes'][0]
        square_method = math_class['methods'][0]
        assert square_method['name'] == 'Square'


class TestCSharpProperties:
    """Tests for C# property parsing."""

    def test_auto_properties(self):
        """Test parsing auto-implemented properties."""
        code = '''
public class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    public string Email { get; private set; }
}
'''
        result = api.get_code_summary(code, 'c_sharp', format='dict')
        assert_successful_result(result)
        # Properties should be detected
        assert result['class_count'] == 1

    def test_property_with_backing_field(self):
        """Test parsing property with backing field."""
        code = '''
public class Person
{
    private string _name;

    public string Name
    {
        get { return _name; }
        set { _name = value; }
    }
}
'''
        result = api.get_code_summary(code, 'c_sharp', format='dict')
        assert_successful_result(result)
        assert result['class_count'] == 1


class TestCSharpDocumentation:
    """Tests for C# XML documentation extraction."""

    def test_method_xml_doc(self, csharp_simple_code):
        """Test extracting XML documentation from method."""
        doc = api.get_documentation(csharp_simple_code, 'method', 'Calculator.Add', language='c_sharp')
        assert doc is not None
        assert 'Adds two numbers' in doc

    def test_class_xml_doc(self, csharp_simple_code):
        """Test extracting XML documentation from class."""
        doc = api.get_documentation(csharp_simple_code, 'class', 'Calculator', language='c_sharp')
        assert doc is not None
        assert 'calculator' in doc.lower()

    def test_multiline_xml_doc(self):
        """Test extracting multiline XML documentation."""
        code = '''
/// <summary>
/// This is a complex class that does many things.
/// It handles calculations and more.
/// </summary>
/// <remarks>
/// Use this class for all your math needs.
/// </remarks>
public class ComplexCalculator
{
    /// <summary>
    /// Performs advanced calculation
    /// </summary>
    /// <param name="x">First parameter</param>
    /// <param name="y">Second parameter</param>
    /// <returns>The result</returns>
    public int Calculate(int x, int y)
    {
        return x + y;
    }
}
'''
        doc = api.get_documentation(code, 'class', 'ComplexCalculator', language='c_sharp')
        assert doc is not None
        assert 'calculations' in doc.lower()


class TestCSharpNamespaces:
    """Tests for C# namespace handling."""

    def test_single_namespace(self):
        """Test parsing code with namespace."""
        code = '''
using System;

namespace MyCompany.MyApp
{
    public class MyClass
    {
        public void DoSomething() { }
    }
}
'''
        result = api.explore_code(code, 'c_sharp', format='dict')
        assert_successful_result(result)

        module = result['module']
        assert len(module['classes']) == 1
        assert module['classes'][0]['name'] == 'MyClass'

    def test_nested_namespaces(self):
        """Test parsing nested namespaces."""
        code = '''
namespace Outer
{
    namespace Inner
    {
        public class NestedClass
        {
        }
    }
}
'''
        result = api.get_public_interface(code, 'c_sharp', format='dict')
        assert_successful_result(result)
        assert result['class_count'] == 1


class TestCSharpAccessModifiers:
    """Tests for C# access modifier handling."""

    def test_public_class_included(self):
        """Test that public classes are included in public interface."""
        code = '''
public class PublicClass { }
'''
        result = api.get_public_interface(code, 'c_sharp', format='dict')
        assert_successful_result(result)
        assert result['class_count'] == 1
        assert result['public_classes'][0]['name'] == 'PublicClass'

    def test_private_class_excluded(self):
        """Test that private top-level classes are excluded from public interface."""
        code = '''
public class PublicClass { }

class PackagePrivateClass { }
'''
        result = api.get_public_interface(code, 'c_sharp', format='dict')
        assert_successful_result(result)

        # Should find PublicClass but not PackagePrivateClass
        class_names = [c['name'] for c in result['public_classes']]
        assert 'PublicClass' in class_names
        assert 'PackagePrivateClass' not in class_names

    def test_internal_class_excluded(self):
        """Test that internal classes are excluded from public interface."""
        code = '''
public class PublicClass { }
internal class InternalClass { }
'''
        result = api.get_public_interface(code, 'c_sharp', format='dict')
        assert_successful_result(result)

        class_names = [c['name'] for c in result['public_classes']]
        assert 'PublicClass' in class_names
        assert 'InternalClass' not in class_names

    def test_public_methods_included(self):
        """Test that public methods are in public interface."""
        code = '''
public class MyClass
{
    public void PublicMethod1() { }
    public void PublicMethod2() { }
}
'''
        result = api.get_public_interface(code, 'c_sharp', format='dict')
        assert_successful_result(result)

        my_class = result['public_classes'][0]
        method_names = [m['name'] for m in my_class['methods']]

        assert 'PublicMethod1' in method_names
        assert 'PublicMethod2' in method_names


class TestCSharpImports:
    """Tests for C# using directive parsing."""

    def test_using_directives(self):
        """Test parsing using directives."""
        code = '''
using System;
using System.Collections.Generic;
using System.Linq;

public class MyClass { }
'''
        result = api.explore_code(code, 'c_sharp', format='dict')
        assert_successful_result(result)

        imports = result['module']['imports']
        assert len(imports) >= 3
        import_text = ' '.join(imports)
        assert 'System' in import_text

    def test_using_static(self):
        """Test parsing using static directives."""
        code = '''
using static System.Math;

public class Calculator
{
    public double GetPI() => PI;
}
'''
        result = api.explore_code(code, 'c_sharp', format='dict')
        assert_successful_result(result)
        # Should parse without error
        assert result['module']['language'] == 'c_sharp'


class TestCSharpReturnTypes:
    """Tests for C# return type extraction."""

    def test_primitive_return_types(self):
        """Test extraction of primitive return types."""
        code = '''
public class TypeTest
{
    public int GetInt() => 42;
    public string GetString() => "test";
    public bool GetBool() => true;
    public double GetDouble() => 3.14;
}
'''
        result = api.get_public_interface(code, 'c_sharp', format='dict')
        assert_successful_result(result)

        type_class = result['public_classes'][0]
        methods = {m['name']: m for m in type_class['methods']}

        assert methods['GetInt']['return_type'] == 'int'
        assert methods['GetString']['return_type'] == 'string'
        assert methods['GetBool']['return_type'] == 'bool'
        assert methods['GetDouble']['return_type'] == 'double'

    def test_complex_return_types(self):
        """Test extraction of complex return types."""
        code = '''
using System.Collections.Generic;

public class ComplexTypes
{
    public List<int> GetList() => new List<int>();
    public Dictionary<string, int> GetDict() => new Dictionary<string, int>();
    public int[] GetArray() => new int[0];
}
'''
        result = api.get_public_interface(code, 'c_sharp', format='dict')
        assert_successful_result(result)

        complex_class = result['public_classes'][0]
        # Should have return_type field for all methods
        for method in complex_class['methods']:
            assert 'return_type' in method
            assert method['return_type'] is not None

    def test_nullable_return_types(self):
        """Test extraction of nullable return types."""
        code = '''
public class NullableTest
{
    public int? GetNullableInt() => null;
    public string? GetNullableString() => null;
}
'''
        result = api.get_public_interface(code, 'c_sharp', format='dict')
        assert_successful_result(result)

        nullable_class = result['public_classes'][0]
        # Should extract return types for nullable types
        for method in nullable_class['methods']:
            assert 'return_type' in method
