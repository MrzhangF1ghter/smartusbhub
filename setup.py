from setuptools import setup, find_packages

setup(
    name="smartusbhub",
    version="1.0.0",
    description="A library to control Smart USB Hub through serial communication",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="jasonzhang",
    author_email="zhangtec@foxmail.com",
    url="https://github.com/MrzhangF1ghter/smartusbhub",
    packages=find_packages(),
    package_dir={'custom_modules': 'serial'},  # patch for Windows 10
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)