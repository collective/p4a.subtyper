import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.3dev'

long_description = (
    read('README.txt')
    + '\n' +
    read('CHANGES.txt')
    )


setup(name='p4a.subtyper',
      version=version,
      description="Subtyping framework for Plone",
      long_description=long_description,
      classifiers=[
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Rocky Burt',
      author_email='rocky@serverzen.com',
      #url='http://www.plone4artists.org/svn/projects/p4a.subtyper/',
      url='https://svn.plone.org/svn/collective/p4a/p4a.subtyper/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['p4a'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'p4a.z2utils'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
