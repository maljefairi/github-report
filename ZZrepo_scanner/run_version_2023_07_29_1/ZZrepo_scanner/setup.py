from setuptools import setup, find_packages

setup(
    name="ZZrepo_scanner",
    version="0.1",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        'python-dotenv~=0.19.1',
        'openai~=0.27.0',
        'backoff~=1.11.1'
    ],
    python_requires='>=3.6, <4',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)