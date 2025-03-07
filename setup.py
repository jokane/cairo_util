from setuptools import setup, find_packages

version_filename = os.path.join(os.path.split(__file__)[0], "cairo_util/version.py")
with open(version_filename) as version_file:
    exec(compile(version_file.read(), version_filename, "exec"))

setup(
    name='cairo_util',
    version=version_from_git(),
    author="Jason O'Kane",
    author_email='jokane@tamu.edu',
    description='Some convenience tools for PyCairo.',
    packages=find_packages(),    
    install_requires=['pycairo']
)
