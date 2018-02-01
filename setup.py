from setuptools import setup, find_packages
from rgc.version import __version__

setup(
  name             = 'rgc',
  version          = __version__,
  description      = 'Cleanup old tags from docker-registry provided with GitLab',
  url              = 'https://github.com/mvisonneau/docker-registry-gitlab-cleanup',
  author           = 'Maxime VISONNEAU',
  author_email     = 'maxime.visonneau@gmail.com',
  license          = 'AGPL-3.0',
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
