APP_NAME='ws'
from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='django-%s' % APP_NAME,
      version=version,
      description="WS BPMS",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Ales Zabala Alava (Shagi)',
      author_email='shagi@gisa-elkartea.org',
      url='http://lagunak.gisa-elkartea.org/projects/wsbpms',
      license='GPL',
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
