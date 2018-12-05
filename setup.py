import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requires = [
    'click>=7.0',
    'pygments>=2.3.0',
]
test_requires = [
    'pytest-cov',
    'pytest>=3.6.1',
    'pytest-mock>=1.10.0'
]

setuptools.setup(
    name="seed-otp",
    version="0.1.0",
    author="Brenden Matthews",
    author_email="brenden@diddyinc.com",
    description="Python-based Bitcoin seed mnemonic one-time pad tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brndnmtthws/seed-otp",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ),
    entry_points={
        'console_scripts':
        ['seed-otp=seed_otp.main:cli'],
    },
    python_requires=">=3.5",
    install_requires=requires,
    tests_require=test_requires,
    extras_require={
        'test': test_requires,
    },
)
