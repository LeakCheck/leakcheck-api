import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="leakcheck",
    version="0.1.3",
    py_modules = ('leakcheck',),
    author="LeakCheck",
    author_email="the@leakcheck.net",
    description="LeakCheck API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LeakCheck/leakcheck-api",
    install_requires=[
          'requests',
          'pysocks'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)