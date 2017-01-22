from setuptools import setup

def readme():
    with open('README.rst', 'r') as f:
        return f.read()

setup(
    name="cans",
    version="0.1",
    description="Reaction-diffusion model for QFA",
    long_description=readme(),
    url="https://github.com/boo62/cans.git",
    author="Daniel Boocock",
    author_email="daniel.boocock@protonmail.ch",
    license="",
    packages=["cans", "models"],
    # scripts=[],
    # install_requires=[],
    # test_suite="tests",
    # zip_safe=False,
    setup_requires=["pytest-runner",],
    tests_require=["pytest",],
)
