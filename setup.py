import io
from setuptools import setup, find_packages
long_description = (
    io.open('README.rst', encoding='utf-8').read()
    + '\n' +
    io.open('CHANGES.rst', encoding='utf-8').read()
    + '\n' +
    io.open('CREDITS.rst', encoding='utf-8').read()
)

setup(
    name='cartridge_braintree',
    version='1.0b1',
    description="Braintree Payments processing for Mezzanine/Cartridge",
    long_description=long_description,
    maintainer="Henri Hulski",
    maintainer_email="henri@openhomeo.info",
    license="MIT",
    url="https://github.com/henri-hulski/cartridge_braintree",
    packages=find_packages(),
    install_requires=[
        'braintree',
    ],
    extras_require=dict(
        countries_utf8_sorting=['pyuca'],
    ),
)
