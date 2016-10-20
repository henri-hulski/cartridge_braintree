import io
import sys
from setuptools import setup, find_packages
from shutil import rmtree

if sys.argv[:2] == ["setup.py", "bdist_wheel"]:
    # Remove previous build dir when creating a wheel build,
    # since if files have been removed from the project,
    # they'll still be cached in the build dir and end up
    # as part of the build, which is really neat!
    try:
        rmtree("build")
    except:
        pass


long_description = (
    io.open('README.rst', encoding='utf-8').read() +
    '\n\n' +
    io.open('CHANGES.rst', encoding='utf-8').read()
)

setup(
    name='cartridge_braintree',
    version='1.1.0',
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
        "Framework :: Django :: 1.8",
        "Framework :: Django :: 1.9",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
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
        'cartridge >= 0.11',
    ],
    extras_require=dict(
        countries_utf8_sorting=['pyuca'],
    ),
)
