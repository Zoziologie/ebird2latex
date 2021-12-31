from setuptools import setup, find_packages

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="e2L", 
        version='0.0.1',
        author="Raphaël Nussbaumer",
        author_email="<rafnuss@gmail.com>",
        description='Generate custom PDF checklists with eBird occurrence data.',
        long_description='eBirdToLaTex Checklist Generator is a Python module which generates a customisable bird checklist based on a specific dataset downloaded from eBird.',
        packages=find_packages(),
        install_requires=['urllib','json', 'requests','codecs'],
        
        keywords=['python', 'eBird', 'LaTeX'],
        classifiers= [
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)