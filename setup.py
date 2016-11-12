from setuptools import setup

setup(name="cans",
      version="0.1",
      description="Reaction-diffusion model for QFA",
      long_description=readme(),
      url="https://github.com/boo62/cans.git",
      author="Daniel Boocock",
      author_email="daniel.boocock@protonmail.ch",
      license="",
      packages=["cans"],
      # package_dir={"cans"},
      # py_modules=["cans.plate", "cans.model",
      #             "cans.fitter", "cans.plotter"],
      scripts=[],
      install_requires=[],
      test_suite="tests",
      tests_require=["pytest"],
      zip_safe=False)
