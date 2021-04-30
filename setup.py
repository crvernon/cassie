from setuptools import setup, find_packages

setup(
    name='cassie',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/crvernon/cassie.git',
    license='MIT',
    author='Chris R. Vernon',
    author_email='chris.vernon@pnnl.gov',
    description='Configuration builders scripts for the Cassandra coupler',
    python_requires='>=3.6',
    include_package_data=True
)
