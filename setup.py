# Update the code and upload the package to pypi
# 1. python ./setup.py bdist_wheel --universal
# 2. twine upload dist/xxx.whl

from setuptools import setup, find_packages

setup(
    name="openmldb_lab",
    version="0.1.2",
    author="tobe",
    author_email="tobeg3oogle@gmail.com",
    url="https://github.com/tobegit3hub/openmldb_lab",
    description="OpenMLDB Lab",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    # TODO: Change to requirements.txt
    install_requires=[
        'flask', 'flask-cors', 'openmldb>=0.4.1'
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "openmldb_lab=openmldb_server.server:main"
        ],
    })
