import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='thread-runner',
    version='0.1',
    author='Marcus Bolmstedt',
    author_email='marcus@bolmstedt.com',
    url='https://github.com/bolmstedt/boozelist/tree/master/packages/thread-runner',
    packages=setuptools.find_packages(),
    description='Runs services in threads.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
 )
