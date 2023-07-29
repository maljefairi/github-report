from setuptools import setup, find_packages

setup(
    name="ZZrepo_scanner",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'python-dotenv>=0.19.1,<1',
        'openai>=0.27.0,<1',
        'backoff>=1.11.1,<2'
    ],
)
