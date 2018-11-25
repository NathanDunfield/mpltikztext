from setuptools import setup

setup(
    name = 'mpltikztext',
    version = '0.1',
    author = 'Nathan Dunfield',
    author_email = 'nathan@dunfield.info',
    description = 'Saving Matplotlib figures with the text turned into a TikZ overlay.',
    license = 'GPLv2+',
    keywords = 'plotting',
    packages=['mpltikztext'],
    package_dir = {'mpltikztext':'src'},
    zip_safe = False,
    install_requires = ['matplotlib>=1.5']
)
