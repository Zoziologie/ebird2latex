# eBird2LaTeX

[![PyPI version](https://img.shields.io/pypi/v/e2L.svg)](https://pypi.org/project/e2L/) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Zoziologie/ebird2latex/blob/master/script_e2L.ipynb)

eBird2LaTeX is a Python module which generates a customisable bird checklist based on [eBird barchart data](https://ebird.org/GuideMe?cmd=changeLocation).

> [!WARNING]  
> The web version of the generator is not available anymore as eBird is requiring to login to get barchart data.

## How to use?

The easiest way to use it is to run this notebook on colab: [`script_e2L.ipynb`](https://github.com/Zoziologie/ebird2latex/blob/master/script_e2L.ipynb)

## Install locally

Clone the e2L repository from GitHub to your local machine:

```bash
git clone https://github.com/Zoziologie/ebird2latex.git
cd ebird2latex
```

Use the following command to install the package locally:

```bash
python setup.py install
```

You can now edit and run the script `script_e2L.py` or notebook `script_e2L.ipynb`.

## Authentification

You'll need to add your credidential of eBird in a new `auth.json` file:

```json
{
  "username": "your_ebird_username",
  "password": "your_ebird_password"
}
```

## Requirement

- eBird login to download barchart data and your target.
- python (only python3 has been tested) with a a couple of standard libraries: `requests`,`re`,`lxml`
- latex (`pdflatex`) with some additional package needed

```bash
tlmgr install colortbl xtab fp ulem hyperref
```

## Example

[See the example folder.](https://github.com/Zoziologie/ebird2latex/tree/master/example)
