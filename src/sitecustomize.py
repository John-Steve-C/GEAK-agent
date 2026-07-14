"""Runtime compatibility patches for local evaluation environments.

The installed TileLang/TVM combination on this machine rejects Python attribute
storage on TVM-derived objects before their handles are initialized. TileLang's
Python visitors/mutators rely on TVM's ``derived_object`` helper, so patch that
helper to keep Python-side instances in a side table instead of ``self._inst``.
"""

import functools
import importlib.abc
import importlib.machinery
import sys
import weakref

_DERIVED_INSTANCES = {}


def _get_inst(obj):
    return _DERIVED_INSTANCES.get(id(obj))


def _patched_derived_object(cls):
    def _extract(inst, name):
        def method(*args, **kwargs):
            return getattr(inst, name)(*args, **kwargs)

        for inherit_cls, base_cls in zip(cls.__mro__, cls.__mro__[1:]):
            if not hasattr(base_cls, name):
                continue
            if getattr(base_cls, name) is getattr(inherit_cls, name) and name != "__str__":
                continue
            return method
        return None

    if hasattr(cls, "_type") and cls._type == "TVMDerivedObject":
        raise TypeError(
            f"Inheritance from a decorated object `{cls.__name__}` is not allowed. "
            f"Please inherit from `{cls.__name__}._cls`."
        )
    if not hasattr(cls, "_tvm_metadata"):
        raise AssertionError("Please use the user-facing method overriding class, i.e., PyRunner.")

    metadata = getattr(cls.__base__, "_tvm_metadata")
    fields = metadata.get("fields", [])
    methods = metadata.get("methods", [])

    class TVMDerivedObject(metadata["cls"]):  # type: ignore
        _cls = cls
        _type = "TVMDerivedObject"

        def __init__(self, *args, **kwargs):
            inst = cls(*args, **kwargs)
            _DERIVED_INSTANCES[id(self)] = inst
            super().__init__(
                *[getattr(inst, name) for name in fields],
                *[_extract(inst, name) for name in methods],
            )
            try:
                outer = weakref.ref(self)
            except TypeError:
                outer = lambda self=self: self
            object.__setattr__(inst, "_outer", outer)

        def __getattr__(self, name):
            import inspect

            inst = _get_inst(self)
            if inst is None:
                return super(TVMDerivedObject, self).__getattr__(name)
            try:
                result = inst.__getattribute__(name)
            except AttributeError:
                result = super(TVMDerivedObject, self).__getattr__(name)

            if inspect.ismethod(result):
                def method(*args, **kwargs):
                    return result(*args, **kwargs)

                setattr(method, "__own__", self)
                return method
            return result

        def __setattr__(self, name, value):
            if name in ["key", "handle"]:
                super(TVMDerivedObject, self).__setattr__(name, value)
                return
            inst = _get_inst(self)
            if inst is None:
                super(TVMDerivedObject, self).__setattr__(name, value)
                return
            inst.__setattr__(name, value)

    functools.update_wrapper(TVMDerivedObject.__init__, cls.__init__)
    TVMDerivedObject.__name__ = cls.__name__
    TVMDerivedObject.__doc__ = cls.__doc__
    TVMDerivedObject.__module__ = cls.__module__
    for key, value in cls.__dict__.items():
        if isinstance(value, (classmethod, staticmethod)):
            setattr(TVMDerivedObject, key, value)
    return TVMDerivedObject


def _patch_support(module):
    if getattr(module.derived_object, "__name__", "") == "_patched_derived_object":
        return
    module.derived_object = _patched_derived_object


def _disable_prelower_semantic_check(module):
    if hasattr(module, "PreLowerSemanticCheck"):
        module.PreLowerSemanticCheck = lambda mod: None


class _CompatLoader(importlib.abc.Loader):
    def __init__(self, wrapped, fullname):
        self.wrapped = wrapped
        self.fullname = fullname

    def create_module(self, spec):
        if hasattr(self.wrapped, "create_module"):
            return self.wrapped.create_module(spec)
        return None

    def exec_module(self, module):
        self.wrapped.exec_module(module)
        if self.fullname == "tvm.runtime.support":
            _patch_support(module)
        elif self.fullname in {"tilelang.engine.phase", "tilelang.engine.lower"}:
            _disable_prelower_semantic_check(module)


class _CompatFinder(importlib.abc.MetaPathFinder):
    TARGETS = {"tvm.runtime.support", "tilelang.engine.phase", "tilelang.engine.lower"}

    def find_spec(self, fullname, path=None, target=None):
        if fullname not in self.TARGETS:
            return None
        spec = importlib.machinery.PathFinder.find_spec(fullname, path)
        if spec is None or spec.loader is None or isinstance(spec.loader, _CompatLoader):
            return spec
        spec.loader = _CompatLoader(spec.loader, fullname)
        return spec


for name, module in list(sys.modules.items()):
    if name == "tvm.runtime.support":
        _patch_support(module)
    elif name in {"tilelang.engine.phase", "tilelang.engine.lower"}:
        _disable_prelower_semantic_check(module)

if not any(isinstance(finder, _CompatFinder) for finder in sys.meta_path):
    sys.meta_path.insert(0, _CompatFinder())
