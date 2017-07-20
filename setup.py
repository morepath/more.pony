
import io
from setuptools import setup, find_packages

long_description = (
    io.open('README.rst', encoding='utf-8').read()
    + '\n\n' +
    io.open('CHANGES.rst', encoding='utf-8').read())

setup(name='more.pony',
      version='0.2',
      description="Pony ORM integration in Morepath",
      long_description=long_description,
      author="Henri Hulski",
      author_email="henri.hulski@gazeta.pl",
      keywords='morepath Pony ORM PonyORM',
      license="BSD",
      url="https://github.com/morepath/more.pony",
      namespace_packages=['more'],
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
      ],
      install_requires=[
          'morepath >= 0.18',
          'pony >= 0.7.2'
      ],
      extras_require=dict(
          test=[
              'pytest >= 2.9.1',
              'pytest-remove-stale-bytecode',
              'webtest'
          ],
          coverage=[
              'pytest-cov',
          ],
          pep8=[
              'flake8',
              'pep8-naming',
          ],
      ))
