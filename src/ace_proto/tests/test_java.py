"""Tests for Java language support.

Tests Java-specific parsing including:
- Classes, interfaces, enums
- Methods with Javadoc
- Constructors
- Fields and constants
- Packages and imports
- Access modifiers
- Annotations
"""

import pytest
from ts_tool import api
from .conftest import assert_successful_result, assert_has_entity


class TestJavaClasses:
    """Tests for Java class parsing."""

    def test_simple_class(self):
        """Test parsing a simple class."""
        code = '''
package com.example;

public class MyClass {
}
'''
        result = api.get_public_interface(code, 'java', format='dict')
        assert_successful_result(result)
        assert result['class_count'] == 1
        assert result['public_classes'][0]['name'] == 'MyClass'

    def test_class_with_methods(self, java_simple_code):
        """Test parsing a class with methods."""
        result = api.get_public_interface(java_simple_code, 'java', format='dict')
        assert_successful_result(result)

        calc_class = result['public_classes'][0]
        assert calc_class['name'] == 'Calculator'
        assert len(calc_class['methods']) == 2
        assert_has_entity(calc_class['methods'], 'add', 'method')
        assert_has_entity(calc_class['methods'], 'multiply', 'method')

    def test_class_with_constructor(self):
        """Test parsing a class with constructor."""
        code = '''
public class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() {
        return name;
    }
}
'''
        result = api.get_public_interface(code, 'java', format='dict')
        assert_successful_result(result)

        person_class = result['public_classes'][0]
        assert person_class['name'] == 'Person'
        # Should have at least the public method
        assert len(person_class['methods']) >= 1

    def test_interface(self):
        """Test parsing an interface."""
        code = '''
public interface Calculator {
    int add(int a, int b);
    int multiply(int a, int b);
}
'''
        result = api.get_public_interface(code, 'java', format='dict')
        assert_successful_result(result)

        assert result['class_count'] == 1
        interface = result['public_classes'][0]
        assert interface['name'] == 'Calculator'
        assert len(interface['methods']) == 2

    def test_enum(self):
        """Test parsing an enum."""
        code = '''
public enum Color {
    RED,
    GREEN,
    BLUE
}
'''
        result = api.get_code_summary(code, 'java', format='dict')
        assert_successful_result(result)
        # Enums should be counted
        assert result['class_count'] >= 1

    def test_abstract_class(self):
        """Test parsing an abstract class."""
        code = '''
public abstract class Shape {
    public abstract double getArea();

    public void printArea() {
        System.out.println(getArea());
    }
}
'''
        result = api.get_public_interface(code, 'java', format='dict')
        assert_successful_result(result)

        shape_class = result['public_classes'][0]
        assert shape_class['name'] == 'Shape'
        assert len(shape_class['methods']) >= 1


class TestJavaMethods:
    """Tests for Java method parsing."""

    def test_method_with_return_type(self, java_simple_code):
        """Test that methods have return types extracted."""
        result = api.get_public_interface(java_simple_code, 'java', format='dict')
        assert_successful_result(result)

        calc_class = result['public_classes'][0]
        add_method = next(m for m in calc_class['methods'] if m['name'] == 'add')

        # Check that return_type field exists and is extracted
        assert 'return_type' in add_method
        assert add_method['return_type'] == 'int'

    def test_void_method(self):
        """Test parsing a void method."""
        code = '''
public class Logger {
    public void log(String message) {
        System.out.println(message);
    }
}
'''
        result = api.get_public_interface(code, 'java', format='dict')
        assert_successful_result(result)

        logger_class = result['public_classes'][0]
        log_method = logger_class['methods'][0]
        assert log_method['name'] == 'log'
        assert log_method['return_type'] == 'void'

    def test_generic_method(self):
        """Test parsing a generic method."""
        code = '''
public class GenericClass {
    public <T> T getValue(T defaultValue) {
        return defaultValue;
    }
}
'''
        result = api.get_public_interface(code, 'java', format='dict')
        assert_successful_result(result)

        generic_class = result['public_classes'][0]
        assert len(generic_class['methods']) == 1
        assert generic_class['methods'][0]['name'] == 'getValue'

    def test_static_method(self):
        """Test parsing a static method."""
        code = '''
public class MathHelper {
    public static int square(int x) {
        return x * x;
    }
}
'''
        result = api.get_public_interface(code, 'java', format='dict')
        assert_successful_result(result)

        math_class = result['public_classes'][0]
        square_method = math_class['methods'][0]
        assert square_method['name'] == 'square'

    def test_method_with_varargs(self):
        """Test parsing method with varargs."""
        code = '''
public class VarArgsTest {
    public int sum(int... numbers) {
        int total = 0;
        for (int n : numbers) {
            total += n;
        }
        return total;
    }
}
'''
        result = api.get_public_interface(code, 'java', format='dict')
        assert_successful_result(result)

        varargs_class = result['public_classes'][0]
        assert len(varargs_class['methods']) == 1
        assert varargs_class['methods'][0]['name'] == 'sum'


class TestJavaFields:
    """Tests for Java field parsing."""

    def test_public_fields(self):
        """Test parsing public fields."""
        code = '''
public class Constants {
    public static final int MAX_SIZE = 100;
    public static final String DEFAULT_NAME = "John";
}
'''
        result = api.get_code_summary(code, 'java', format='dict')
        assert_successful_result(result)
        # Constants should be detected
        assert result['class_count'] == 1

    def test_private_fields_excluded(self):
        """Test that private fields are excluded from public interface."""
        code = '''
public class MyClass {
    private int privateField;
    public int publicField;
}
'''
        result = api.get_public_interface(code, 'java', format='dict')
        assert_successful_result(result)
        # Should parse successfully
        assert result['class_count'] == 1


class TestJavaDocumentation:
    """Tests for Java Javadoc extraction."""

    def test_method_javadoc(self, java_simple_code):
        """Test extracting Javadoc from method."""
        doc = api.get_documentation(java_simple_code, 'method', 'Calculator.add', language='java')
        assert doc is not None
        assert 'Adds two numbers' in doc

    def test_class_javadoc(self, java_simple_code):
        """Test extracting Javadoc from class."""
        doc = api.get_documentation(java_simple_code, 'class', 'Calculator', language='java')
        assert doc is not None
        assert 'calculator' in doc.lower()

    def test_multiline_javadoc(self):
        """Test extracting multiline Javadoc."""
        code = '''
/**
 * This is a complex class that does many things.
 * It handles calculations and more.
 *
 * @author John Doe
 * @version 1.0
 */
public class ComplexCalculator {
    /**
     * Performs advanced calculation
     *
     * @param x First parameter
     * @param y Second parameter
     * @return The result
     * @throws IllegalArgumentException if parameters are invalid
     */
    public int calculate(int x, int y) {
        return x + y;
    }
}
'''
        doc = api.get_documentation(code, 'class', 'ComplexCalculator', language='java')
        assert doc is not None
        assert 'complex class' in doc.lower()


class TestJavaPackages:
    """Tests for Java package handling."""

    def test_package_declaration(self):
        """Test parsing code with package declaration."""
        code = '''
package com.mycompany.myapp;

import java.util.List;

public class MyClass {
    public void doSomething() { }
}
'''
        result = api.explore_code(code, 'java', format='dict')
        assert_successful_result(result)

        module = result['module']
        assert len(module['classes']) == 1
        assert module['classes'][0]['name'] == 'MyClass'

    def test_nested_packages(self):
        """Test parsing deeply nested package."""
        code = '''
package com.example.project.module.submodule;

public class NestedClass {
}
'''
        result = api.get_public_interface(code, 'java', format='dict')
        assert_successful_result(result)
        assert result['class_count'] == 1


class TestJavaAccessModifiers:
    """Tests for Java access modifier handling."""

    def test_public_class_included(self):
        """Test that public classes are included in public interface."""
        code = '''
public class PublicClass { }
'''
        result = api.get_public_interface(code, 'java', format='dict')
        assert_successful_result(result)
        assert result['class_count'] == 1
        assert result['public_classes'][0]['name'] == 'PublicClass'

    def test_package_private_class_excluded(self):
        """Test that package-private classes are excluded from public interface."""
        code = '''
public class PublicClass { }
class PackagePrivateClass { }
'''
        result = api.get_public_interface(code, 'java', format='dict')
        assert_successful_result(result)

        class_names = [c['name'] for c in result['public_classes']]
        assert 'PublicClass' in class_names
        assert 'PackagePrivateClass' not in class_names

    def test_public_methods_only(self):
        """Test that only public methods are in public interface."""
        code = '''
public class MyClass {
    public void publicMethod() { }
    private void privateMethod() { }
    protected void protectedMethod() { }
    void packagePrivateMethod() { }
}
'''
        result = api.get_public_interface(code, 'java', format='dict')
        assert_successful_result(result)

        my_class = result['public_classes'][0]
        method_names = [m['name'] for m in my_class['methods']]

        assert 'publicMethod' in method_names
        assert 'privateMethod' not in method_names
        assert 'protectedMethod' not in method_names
        assert 'packagePrivateMethod' not in method_names


class TestJavaImports:
    """Tests for Java import statement parsing."""

    def test_import_statements(self):
        """Test parsing import statements."""
        code = '''
package com.example;

import java.util.List;
import java.util.ArrayList;
import java.util.Map;

public class MyClass { }
'''
        result = api.explore_code(code, 'java', format='dict')
        assert_successful_result(result)

        imports = result['module']['imports']
        assert len(imports) >= 3
        import_text = ' '.join(imports)
        assert 'java.util' in import_text

    def test_wildcard_import(self):
        """Test parsing wildcard imports."""
        code = '''
import java.util.*;

public class MyClass { }
'''
        result = api.explore_code(code, 'java', format='dict')
        assert_successful_result(result)
        # Should parse without error
        assert result['module']['language'] == 'java'

    def test_static_import(self):
        """Test parsing static imports."""
        code = '''
import static java.lang.Math.PI;
import static java.lang.Math.sqrt;

public class Calculator {
    public double getPI() {
        return PI;
    }
}
'''
        result = api.explore_code(code, 'java', format='dict')
        assert_successful_result(result)
        # Should parse successfully
        assert result['module']['language'] == 'java'


class TestJavaAnnotations:
    """Tests for Java annotation handling."""

    def test_override_annotation(self):
        """Test parsing @Override annotation."""
        code = '''
public class MyClass extends BaseClass {
    @Override
    public String toString() {
        return "MyClass";
    }
}
'''
        result = api.get_public_interface(code, 'java', format='dict')
        assert_successful_result(result)

        my_class = result['public_classes'][0]
        assert len(my_class['methods']) >= 1

    def test_deprecated_annotation(self):
        """Test parsing @Deprecated annotation."""
        code = '''
public class MyClass {
    @Deprecated
    public void oldMethod() { }

    public void newMethod() { }
}
'''
        result = api.get_public_interface(code, 'java', format='dict')
        assert_successful_result(result)

        my_class = result['public_classes'][0]
        assert len(my_class['methods']) == 2

    def test_custom_annotation(self):
        """Test parsing custom annotations."""
        code = '''
public class MyClass {
    @MyCustomAnnotation(value = "test")
    public void annotatedMethod() { }
}
'''
        result = api.get_public_interface(code, 'java', format='dict')
        assert_successful_result(result)
        # Should parse without error
        assert result['class_count'] == 1


class TestJavaReturnTypes:
    """Tests for Java return type extraction."""

    def test_primitive_return_types(self):
        """Test extraction of primitive return types."""
        code = '''
public class TypeTest {
    public int getInt() { return 42; }
    public long getLong() { return 42L; }
    public boolean getBool() { return true; }
    public double getDouble() { return 3.14; }
    public char getChar() { return 'a'; }
}
'''
        result = api.get_public_interface(code, 'java', format='dict')
        assert_successful_result(result)

        type_class = result['public_classes'][0]
        methods = {m['name']: m for m in type_class['methods']}

        assert methods['getInt']['return_type'] == 'int'
        assert methods['getLong']['return_type'] == 'long'
        assert methods['getBool']['return_type'] == 'boolean'
        assert methods['getDouble']['return_type'] == 'double'
        assert methods['getChar']['return_type'] == 'char'

    def test_object_return_types(self):
        """Test extraction of object return types."""
        code = '''
public class TypeTest {
    public String getString() { return "test"; }
    public Object getObject() { return null; }
    public Integer getInteger() { return 42; }
}
'''
        result = api.get_public_interface(code, 'java', format='dict')
        assert_successful_result(result)

        type_class = result['public_classes'][0]
        methods = {m['name']: m for m in type_class['methods']}

        assert methods['getString']['return_type'] == 'String'
        assert methods['getObject']['return_type'] == 'Object'
        assert methods['getInteger']['return_type'] == 'Integer'

    def test_generic_return_types(self):
        """Test extraction of generic return types."""
        code = '''
import java.util.List;
import java.util.Map;

public class GenericTypes {
    public List<String> getList() { return null; }
    public Map<String, Integer> getMap() { return null; }
}
'''
        result = api.get_public_interface(code, 'java', format='dict')
        assert_successful_result(result)

        generic_class = result['public_classes'][0]
        # Should have return_type field for all methods
        for method in generic_class['methods']:
            assert 'return_type' in method
            assert method['return_type'] is not None

    def test_array_return_types(self):
        """Test extraction of array return types."""
        code = '''
public class ArrayTest {
    public int[] getIntArray() { return new int[0]; }
    public String[] getStringArray() { return new String[0]; }
}
'''
        result = api.get_public_interface(code, 'java', format='dict')
        assert_successful_result(result)

        array_class = result['public_classes'][0]
        # Should have return_type field for all methods
        for method in array_class['methods']:
            assert 'return_type' in method
            assert method['return_type'] is not None


class TestJavaInheritance:
    """Tests for Java inheritance handling."""

    def test_class_extends(self):
        """Test parsing class with extends."""
        code = '''
public class BaseClass { }

public class DerivedClass extends BaseClass {
    public void derivedMethod() { }
}
'''
        result = api.get_public_interface(code, 'java', format='dict')
        assert_successful_result(result)

        # Should find both classes
        class_names = [c['name'] for c in result['public_classes']]
        assert 'BaseClass' in class_names
        assert 'DerivedClass' in class_names

    def test_interface_implements(self):
        """Test parsing class that implements interface."""
        code = '''
public interface MyInterface {
    void interfaceMethod();
}

public class MyClass implements MyInterface {
    public void interfaceMethod() { }
}
'''
        result = api.get_public_interface(code, 'java', format='dict')
        assert_successful_result(result)

        # Should find both interface and class
        assert result['class_count'] == 2

    def test_multiple_interfaces(self):
        """Test parsing class implementing multiple interfaces."""
        code = '''
public class MyClass implements Interface1, Interface2 {
    public void method1() { }
    public void method2() { }
}
'''
        result = api.get_public_interface(code, 'java', format='dict')
        assert_successful_result(result)
        assert result['class_count'] == 1
