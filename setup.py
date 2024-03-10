from setuptools import setup, find_packages

setup(
    name="emsurveil",
    version="0.0.1",
    author="Eric Monlye",
    author_email="536682885@qq.com",
    url='https://github.com/Eicmlye/emsurveil', # project main page
    description="A Python implementation of Camera Placement Plan Evaluation System for Early Warning in Laboratories",
    long_description=open('README.md').read(),
    long_description_content_type="markdown",
    license="MIT Licence",

    python_requires=">=3.10, <3.11",
    install_requires=[
      "geatpy==2.7",
      "tqdm>=4.66.2",
    ],
    packages=find_packages(),

    platforms="any",
)
