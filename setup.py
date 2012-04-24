APP_NAME='ws'
from setuptools import setup, find_packages
import sys, os

version = '0.1'

classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Other Environment',
    'Framework :: Django',
    'Programming Language :: Python',
    'License :: OSI Approved :: GNU Affero General Public License v3',
]

long_description = file('README.rst').read()

setup(name='django-%s' % APP_NAME,
      version=version,
      description="WS BPMS",
      long_description=long_description,
      classifiers=classifiers, # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='GISA Elkartea',
      author_email='kontaktua@gisa-elkartea.org',
      url='http://lagunak.gisa-elkartea.org/projects/django-ws',
      license='AGPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      package_dir={
          APP_NAME: APP_NAME,
      },
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
