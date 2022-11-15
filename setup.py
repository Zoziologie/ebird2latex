from setuptools import setup

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="e2L",
    version='0.1.0',
    license='MIT',
    author="Raphaël Nussbaumer",
    author_email="<rafnuss@gmail.com>",
    description='Generate custom PDF checklists with eBird occurrence data.',
    long_description='eBirdToLaTex Checklist Generator is a Python module which generates a customisable bird checklist based on a specific dataset downloaded from eBird.',
    url="https://github.com/Zoziologie/ebird2latex",
    download_url="https://github.com/Zoziologie/ebird2latex/archive/refs/tags/v0.0.3.tar.gz",
    py_modules=["e2L"],
        install_requires=['requests', 're', 'lxml'],

    keywords=['python', 'eBird', 'LaTeX'],
    classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
    ]
)
