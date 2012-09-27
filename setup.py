from setuptools import setup, find_packages
import sys, os

version = '0.2'

setup(name='pyramid_saaudittrail',
      version=version,
      description="Automatically audit db changes for pyramid and sqlalchemy",
      long_description=open('README.rst').read(),
      classifiers=[
            'Framework :: Pyramid'],
      keywords='',
      author='Nathan Van Gheem',
      author_email='vangheem@gmail.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
            'zope.sqlalchemy',
            'JSON-Datetime'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
