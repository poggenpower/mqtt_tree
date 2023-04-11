import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mqtt_client",
    version="0.2.2",
    author="Thomas Laubrock",
    author_email="mqtt_tree@schmu.net",
    description="Wrapper around paho mqtt client. Optional dispay a UI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/poggenpower/mqtt_tree",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/poggenpower/mqtt_tree/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    packages=["mqtt_client"],
    install_requires=["paho-mqtt>=1.5.1"],
    tests_require=["pytest"],
    entry_points={"console_scripts": ["mqtt_tree=mqtt_client.mqtt_tree:main"]},
)
