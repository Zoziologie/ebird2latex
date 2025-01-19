from setuptools import setup

setup(
    name="e2L",
    version="0.2.0",
    license="MIT",
    author="Raphaël Nussbaumer",
    author_email="rafnuss@gmail.com",
    description="Generate custom PDF checklists with eBird occurrence data.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Zoziologie/ebird2latex",
    download_url="https://github.com/Zoziologie/ebird2latex/archive/refs/tags/v0.0.3.tar.gz",
    py_modules=["e2L"],
    install_requires=["requests", "lxml"],
    keywords=["python", "eBird", "LaTeX"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
    ],
)
