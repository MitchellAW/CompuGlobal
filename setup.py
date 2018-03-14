from distutils.core import setup
from setuptools import find_packages

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='compuglobal',
    packages=find_packages(exclude=['docs', 'doc', 'testing', 'examples']),
    version='0.1.7',
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
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6'],
    install_requires=['requests==2.18.4']
)
