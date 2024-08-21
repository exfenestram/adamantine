from setuptools import setup, find_packages

setup(
    name='adamantine',
    version='0.2',
    packages=find_packages(include=['adamantine', 'adamantine.*']),
    license='MIT',
    description='A library for Immutable/Functional programming in Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=['pyrsistent'],

    url='https://github.com/exfenestram/adamantine',
    author='Ray Richardson')

