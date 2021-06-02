from setuptools import setup

with open("README.md") as f:
    long_desc = f.read()

setup(
    name='MathLang-Core',
    version='2021.0',
    author='GreaterGoodCorp',
    author_email='binhnt.mdev@gmail.com',
    license='MIT License',
    description='MathLang is a specially designed programming language for maths.',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Education",
        "Topic :: Utilities",
    ],
    url='https://github.com/GreaterGoodCorp/MathLang',
    project_urls={
        "Bug Tracker": "https://github.com/GreaterGoodCorp/MathLang/issues",
    },
    packages=['MathLang', 'MathLang.Core'],
    package_dir={'': 'src'},
    install_requires=[
        "rply~=0.7.7",
        "sympy~=1.8",
        "dill~=0.3.3",
    ],
    python_requires=">=3.6",
)
