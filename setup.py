from setuptools import find_packages, setup

setup(
    name="orchestrator",
    packages=find_packages(exclude=["orchestrator_tests"]),
    # package data paths are relative to the package key
    package_data={"orchestrator": ["analytics/**/*"]},
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-airbyte",
        "boto3",
        "dagster-dbt",
        "pandas",
        "numpy",
        "scipy",
        "dbt-core",
        "dbt-snowflake",
        # packaging v22 has build compatibility issues with dbt as of 2022-12-07
        "packaging<22.0",
        "streamlit",
        "snowflake",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest", "snowflake-snowpark-python[localtest]"]},
)
