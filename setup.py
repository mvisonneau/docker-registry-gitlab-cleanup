from setuptools import setup, find_packages
from rgc.version import __version__

setup(
  name             = 'rgc',
  version          = __version__,
  description      = 'Cleanup old tags from docker-registry provided with GitLab',
  url              = 'http://github.com/mvisonneau/registry-gitlab-cleaner',
  author           = 'Maxime VISONNEAU',
  author_email     = 'maxime.visonneau@gmail.com',
  license          = 'Apache 2.0',
  packages         = find_packages( exclude=[ 'docs', 'tests*' ] ),
  install_requires = [
    'www_authenticate',
    'requests',
    'python-gitlab'
  ],
  entry_points     = {
    'console_scripts': [
      'rgc=rgc.cli:main'
    ],
  }
)