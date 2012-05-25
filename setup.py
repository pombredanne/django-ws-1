###############################################################################
#  Copyright 2011,2012 GISA Elkartea.                                         #
#                                                                             #
#  This file is part of django-ws.                                            #
#                                                                             #
#  django-ws is free software: you can redistribute it and/or modify it       #
#  under the terms of the GNU Affero General Public License as published      #
#  by the Free Software Foundation, either version 3 of the License, or       #
#  (at your option) any later version.                                        #
#                                                                             #
#  django-ws is distributed in the hope that it will be useful, but WITHOUT   #
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or      #
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public       #
#  License for more details.                                                  #
#                                                                             #
#  You should have received a copy of the GNU Affero General Public License   #
#  along with django-ws. If not, see <http://www.gnu.org/licenses/>.          #
###############################################################################

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
      package_data = {
          'templates': ['*'],
          'static': ['*'],
          },
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'django_extjs4',
          'django-celery',
          'django-guardian',
          'django-jsonfield',
          'pexpect',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
