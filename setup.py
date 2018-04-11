from setuptools import setup

setup(
    Name='JAAC',
    version='0.1',
    author='Marcus Vechiato',
    description='Just another AWS cli',
    license='GPVv3+',
    packages=['jaac'],
    url='https://github.com/vechiato/jaac',
    install_requires=[
        'click',
        'boto3',
        'sqlite3',
        'pandas',
        'zipfile'
    ],
    entry_points='''
        [console_scripts]
        jaac=jaac.jaac:cli
    ''',
)
