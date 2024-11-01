from setuptools import setup, find_packages

setup(
    name="smartusbhub",
    version="1.0.0",
    description="A library to control Smart USB Hub through serial communication",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/smartusbhub",  # 仓库链接
    packages=find_packages(),
    install_requires=[
        "pyserial"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)