from setuptools import setup, find_packages

setup(
    name='weather-sdk',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'weather-sdk=weather_sdk.sdk:main',
        ],
    },
)
ы