from setuptools import setup, find_packages
import unittest

with open("README.md", "r") as fh:
    long_description = fh.read()


def main(version: str = "0.0.1"):
    setup(name='pyprofiling',
          version=version,
          description='Profiling a program for visualization in chrome://tracing/',
          long_description=long_description,
          long_description_content_type="text/markdown",
          url='https://github.com/JulianSobott/pyprofiling',
          author='Julian Sobott',
          author_email='julian.sobott@gmail.com',
          license='Apache',
          packages=find_packages(),
          include_package_data=True,
          keywords='profiling threads timing',
          project_urls={
              "Bug Tracker": "https://github.com/JulianSobott/pyprofiling/issues",
              "Source Code": "https://github.com/JulianSobott/pyprofiling",
          },
          classifiers=[
              "Programming Language :: Python :: 3.7",
              "License :: OSI Approved :: Apache Software License",
              "Operating System :: OS Independent",
              "Topic :: Software Development :: Libraries",
          ],
          zip_safe=False,
          )


if __name__ == '__main__':
    main()
