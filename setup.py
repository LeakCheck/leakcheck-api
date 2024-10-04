import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="leakcheck",
    version="2.0.0",
    py_modules = ('leakcheck',),
    scripts=['leakcheck'],
    author="LeakCheck",
    author_email="the@leakcheck.net",
    description="Python wrapper for LeakCheck API & also a CLI tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LeakCheck/leakcheck-api",
    install_requires=[
          'requests',
          'pysocks',
          'tabulate'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
