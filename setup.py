from setuptools import setup, find_packages


setup(name="lembas",
      version="0.1.0",
      author="shonenada",
      author_email="shonenada@gmail.com",
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      description="simple K-V server",
      url="https://github.com/shonenada/Lembas",
      install_requires=[
        "Flask==0.12.1",
        "python-envcfg==0.2.0",
      ],
)

