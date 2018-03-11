from distutils.core import setup
from setuptools import find_packages

setup(
    name='compuglobal',
    packages=find_packages(exclude=['docs', 'doc', 'testing']),
    version='0.1.3',
    description='Unofficial python wrapper for the CGHMC API (Frinkiac, ' +
                'Morbotron, Master Of All Science and more!)',
    author='MitchellAW',
    author_email='mitchwoollatt@gmail.com',
    url='https://github.com/MitchellAW/CompuGlobal',
    # Where to dowload your package
    download_url='https://github.com/MitchellAW/CompuGlobal/' +
                 'archive/0.1.3.tar.gz',
    keywords=['frinkiac', 'morbotron', 'master-of-all-science',
              'good-god-lemon', 'capital-beat-us', 'the-simpsons',
              'futurama', 'rick-and-morty', '30 rock', 'west wing', 'api'],
    scripts=[],
    classifiers=[],
    # List of your dependencies
    install_requires=['requests==2.18.4']
)
