from setuptools import setup, find_packages

setup(
    name="snakegame",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pygame",
    ],
    entry_points={
        'console_scripts': [
            'snakegame=snakegame.game:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple Snake game implemented in Python using Pygame",
    keywords="game, snake, pygame",
    python_requires=">=3.6",
)
