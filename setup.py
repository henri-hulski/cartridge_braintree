import io
from setuptools import setup, find_packages
long_description = (
    io.open('README.rst', encoding='utf-8').read() +
    '\n' +
    io.open('CHANGES.rst', encoding='utf-8').read() +
    '\n' +
    io.open('CREDITS.rst', encoding='utf-8').read()
)

setup(
    name='cartridge_braintree',
    version='1.0b2',
    description="Braintree Payments processing for Mezzanine/Cartridge",
    long_description=long_description,
    maintainer="Henri Hulski",
    maintainer_email="henri@openhomeo.info",
    license="BSD",
    url="https://github.com/henri-hulski/cartridge_braintree",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    keywords='django mezzanine cartridge payment',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'braintree',
    ],
    extras_require=dict(
        countries_utf8_sorting=['pyuca'],
    ),
)
