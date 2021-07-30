from setuptools import setup, find_packages

setup(
    name="flexlmtools",
    version="0.1.0",
    install_requires=[],
    extras_require={
        "develop": ["pytest"]
    },
    author="Sho Hirose",
    author_email="sho.hirose@gmail.com",
    description="Package for Flexlm License Manager",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Unlicense",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6'
)