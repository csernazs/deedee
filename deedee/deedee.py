
import functools
import inspect
from abc import ABC, abstractmethod


class Unset:
    def __repr__(self):
        return "<unset>"


class ResolveError(Exception):
    pass


class AlreadyRegistered(Exception):
    pass


class LazyValue(ABC):
    @abstractmethod
    def resolve(self):
        pass


class ContextValue(LazyValue):
    def __init__(self, registry, key):
        super().__init__()
        self._registry = registry
        self._key = key

    def resolve(self):
        try:
            value = self._registry[self._key]
        except KeyError:
            raise ResolveError("Key {!r} is undefined".format(self._key)) from None
        return value

    def __repr__(self):
        return "<ContextValue for {!r}>".format(self._key)


class Context:
    def __init__(self, registry=None):
        if registry is None:
            registry = {}
        self.registry = registry
        self.keys_taken = {}

    def __getattr__(self, key):
        if key in self.keys_taken:
            retval = self.keys_taken[key]
        else:
            retval = self.keys_taken[key] = ContextValue(self.registry, key)

        return retval

    def register(self, key, value, *, force=False):
        if key in self.registry and not force:
            raise AlreadyRegistered("Key already registered: {!r}".format(key))
        self.registry[key] = value

    def get_unresolved_keys(self):
        return set(self.keys_taken.keys()) - set(self.registry.keys())

    def is_all_resolved(self):
        return not bool(self.get_unresolved_keys())


def resolve(func):
    signature = inspect.signature(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        new_parameters = []
        for parameter in signature.parameters.values():
            if isinstance(parameter.default, LazyValue):
                new_parameters.append(parameter.replace(default=parameter.default.resolve()))
            else:
                new_parameters.append(parameter)

        new_signature = signature.replace(parameters=new_parameters)
        bound_args = new_signature.bind(*args, **kwargs)
        bound_args.apply_defaults()
        return func(*bound_args.args, **bound_args.kwargs)
    return wrapper


UNSET = Unset()
context = Context()
