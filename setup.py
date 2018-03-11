from distutils.core import setup
from setuptools import find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='compuglobal',
    packages=find_packages(exclude=['docs', 'doc', 'testing']),
    version='0.1.4',
    description='Unofficial python wrapper for the CGHMC API (Frinkiac, ' +
                'Morbotron, Master Of All Science and more!)',
    long_description=long_description,
    author='MitchellAW',
    author_email='mitchwoollatt@gmail.com',
    url='https://github.com/MitchellAW/CompuGlobal',
    keywords=['frinkiac', 'morbotron', 'master-of-all-science',
              'good-god-lemon', 'capital-beat-us', 'the-simpsons',
              'futurama', 'rick-and-morty', '30 rock', 'west wing', 'api'],
    scripts=[],
    classifiers=[],
    install_requires=['requests==2.18.4']
)
