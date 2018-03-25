# pylint: disable=W0621

import pytest
import deedee


@pytest.fixture
def context():
    return deedee.Context()


def test_example1(context):
    @deedee.resolve
    def example(param1, param2, param3=context.example):
        return (param1, param2, param3)

    context.register("example", "foobar")
    assert example("a", "b") == ("a", "b", "foobar")
    assert example(param1="a", param2="b") == ("a", "b", "foobar")
    assert example(param2="b", param1="a") == ("a", "b", "foobar")


def test_example1_override(context):
    @deedee.resolve
    def example(param1, param2, param3=context.example):
        return (param1, param2, param3)

    context.register("example", "foobar")
    assert example("a", "b", "c") == ("a", "b", "c")
    assert example("a", "b", param3="c") == ("a", "b", "c")
    assert example(param3="c", param1="a", param2="b") == ("a", "b", "c")


def test_example_kwargs(context):
    @deedee.resolve
    def example_kwargs(param1, param2, *, param3=context.example_kwargs):
        return (param1, param2, param3)

    context.register("example_kwargs", "foobar")
    assert example_kwargs("a", "b") == ("a", "b", "foobar")


def test_example_multiple(context):
    @deedee.resolve
    def example_multiple(param1=context.p1, param2=context.p2, param3=context.p3):
        return (param1, param2, param3)
    context.register("p1", "v1")
    context.register("p2", "v2")
    context.register("p3", "v3")

    assert example_multiple() == ("v1", "v2", "v3")
    assert example_multiple(1) == (1, "v2", "v3")
    assert example_multiple(1, 2) == (1, 2, "v3")
    assert example_multiple(1, 2, 3) == (1, 2, 3)


def test_example_mutable(context):
    @deedee.resolve
    def example_mutable(param1=context.p1):
        return param1

    v1 = [1]
    context.register("p1", v1)

    v1.append(5)

    assert example_mutable() == [1, 5]
    assert example_mutable() is v1
