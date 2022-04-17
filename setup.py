from distutils.core import setup
from setuptools import find_packages

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='compuglobal',
    packages=find_packages(exclude=['docs', 'tests', 'examples']),
    version='0.2.6',
    description='Python wrapper for the CGHMC API (Frinkiac, Morbotron,' +
                ' Master Of All Science and more!)',
    long_description=long_description,
    author='MitchellAW',
    author_email='mitchwoollatt@gmail.com',
    license='MIT',
    url='https://github.com/MitchellAW/CompuGlobal',
    keywords=['frinkiac', 'morbotron', 'master-of-all-science',
              'good-god-lemon', 'capital-beat-us', 'the-simpsons',
              'futurama', 'rick-and-morty', '30 rock', 'west wing', 'api'],
    scripts=[],
    classifiers=['Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.9',
                 'Programming Language :: Python :: 3.10'],
    install_requires=['requests>=2.20.0', 'aiohttp>=3.6.0,<4']
)
