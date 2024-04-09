from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name = 'arms_control_package',
    version = '0.1',
    packages = find_packages(),
    install_requires = requirements,
    author = 'Ethan Masters',
    author_email='ethansmasters@outlook.com',
    description = 'Setup.py file for downloading and installing required modules and dependencies needed to run the project',
)
