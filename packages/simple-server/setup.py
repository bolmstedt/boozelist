import setuptools

setuptools.setup(
    name='simple-server',
    version='0.1',
    packages=setuptools.find_packages(),
    description='Simple HTTP server with router.',
    dependency_links=['file:/../thread-runner'],
 )
