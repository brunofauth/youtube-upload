from setuptools import setup
from pathlib import Path


HERE = Path(__file__).parent


if __name__ == "__main__":

    data = {}
    with open(HERE / "wcd/__version__.py", "r", encoding="utf-8") as f:
        exec(f.read(), data)

    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()

    setup(
        name=data["__title__"],
        version=data["__version__"],
        license=data["__license__"],

        author=data["__author__"],
        author_email=data["__author_email__"],

        description=data["__description__"],
        long_description=long_description,
        long_description_content_type="text/markdown",

        packages=["yt_upload"],
        install_requires=["click>=8.1.2", "google-api-python-client>=2.42.0", "oauth2client>=4.1.3", "tqdm>=4.63.1"],

        entry_points={"console_scripts": ["wcd=yt_upload.cli:cli_main"]},
        # package_data={"": ["*.yml"]},

        url=data["__url__"],
        project_urls={"Bug Tracker": "https://github.com/brunofauth/youtube_upload/issues"},

        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License"
        ],
        python_requires=">=3.10"
    )


