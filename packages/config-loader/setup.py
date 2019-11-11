import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='config-loader',
    version='0.1',
    author='Marcus Bolmstedt',
    author_email='marcus@bolmstedt.com',
    url='https://github.com/bolmstedt/boozelist/tree/master/packages/config-loader',
    packages=setuptools.find_packages(),
    description='Loads configuration data',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
 )
