from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in karkhana_supplier_discovery/__init__.py
from karkhana_supplier_discovery import __version__ as version

setup(
	name="karkhana_supplier_discovery",
	version=version,
	description="Supplier Discovery",
	author="karkhana.io",
	author_email="weadmin@karkhana.io",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
