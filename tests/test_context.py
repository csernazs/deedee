
import pytest
import deedee


def test_lazyvalue():
    lv = deedee.LazyValue()
    lv.value = 1234
    assert lv.resolve() == lv.value


def test_contextvalue():
    registry = {"foo": "bar"}
    cv = deedee.ContextValue(registry, "foo")
    assert cv.resolve() == "bar"


def test_contextvalue_non_existing_key():
    cv = deedee.ContextValue({}, "non_existing")
    with pytest.raises(deedee.ResolveError):
        cv.resolve()


def test_context_happy_path():
    context = deedee.Context()
    context_value = context.foobar

    context.register("foobar", "baz")
    with pytest.raises(deedee.AlreadyRegistered):
        context.register("foobar", "zzz")

    assert context_value.resolve() == "baz"
    assert context.get_unresolved_keys() == set()
    assert context.is_all_resolved() is True


def test_context_resolve_error():
    context = deedee.Context()
    extra_context_value = context.not_defined

    assert context.get_unresolved_keys() == {"not_defined"}
    with pytest.raises(deedee.ResolveError):
        extra_context_value.resolve()

    assert context.is_all_resolved() is False
