Rodolphe
========
Anonymous image board

Quick Start
-----------
1. Clone the repository

        git clone git@github.com:entwanne/Rodolphe.git

2. Install the dependancies

        pip install -r stable-req.txt

3. Configure the settings

  By copying `rodolphe/rodolphe/local_settings.py.example` into `rodolphe/rodolphe/local_settings.py` and setting website's name, secret key, database, language.

4. Deploy

  Serve statically `/media/` directory, and deploy the application with your favorite server.


Requirements
------------
Only tested with this configuration:
* *Python 3.3.3*
* [*Django 1.6.1*](https://www.djangoproject.com/)
* [*Markdown 2.3.1*](https://pypi.python.org/pypi/Markdown)
* [*Pillow 2.3.0*](https://pypi.python.org/pypi/Pillow)
* [*django-bootstrap3 2.5.5*](https://github.com/dyve/django-bootstrap3)
* [*fake-factory 0.3.2*](https://pypi.python.org/pypi/fake-factory/0.3.2)

(see [stable-req.txt](stable-req.txt))
