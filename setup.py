from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        'sentence_embedding',
        ['sentence_embedding.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++',
    ),
]

setup(
    name='sentence_embedding',
    ext_modules=ext_modules,
    zip_safe=False,
)
