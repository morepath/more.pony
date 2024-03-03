from setuptools import setup, find_packages

long_description = (
    open("README.rst", encoding="utf-8").read()
    + "\n\n"
    + open("CHANGES.rst", encoding="utf-8").read()
)

setup(
    name="more.pony",
    version="0.4",
    description="Pony ORM integration in Morepath",
    long_description=long_description,
    author="Henri Hulski",
    author_email="henri.hulski@gazeta.pl",
    keywords="morepath Pony ORM PonyORM",
    license="BSD",
    url="https://github.com/morepath/more.pony",
    namespace_packages=["more"],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    install_requires=["morepath >= 0.19", "pony >= 0.7.17"],
    extras_require=dict(
        test=[
            "pytest >= 2.9.1",
            "pytest-remove-stale-bytecode",
            "webtest",
            "pygments",
        ],
        coverage=["pytest-cov"],
        lint=["flake8", "black"],
    ),
)
