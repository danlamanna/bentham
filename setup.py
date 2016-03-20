from setuptools import setup

setup(
    name="bentham",
    author="Dan LaManna, Chris Kotfila",
    author_email="me@danlamanna.com, kotfic@gmail.com",
    license="",
    description="",
    version="0.1.0",
    packages=['bentham',
              'bentham.clients',
              'bentham.trackers'],
    install_requires=[
        'Click',
    ],
    entry_points='''
    [console_scripts]
    bentham=bentham.cli:cli
    ''',
)
