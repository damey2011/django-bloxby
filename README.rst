=============================
Django Bloxby
=============================

.. image:: https://badge.fury.io/py/django-bloxby.svg
    :target: https://badge.fury.io/py/django-bloxby

.. image:: https://travis-ci.org/damey2011/django-bloxby.svg?branch=master
    :target: https://travis-ci.org/damey2011/django-bloxby

.. image:: https://codecov.io/gh/damey2011/django-bloxby/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/damey2011/django-bloxby

A django application for bridging bloxby and your django software supporting User creation, package creation and autologin

Documentation
-------------

The full documentation is at https://django-bloxby.readthedocs.io.

Quickstart
----------

Install Django Bloxby::

    pip install django-bloxby

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'bloxby.apps.BloxbyConfig',
        ...
    )

Add Django Bloxby's URL patterns:

.. code-block:: python

    from bloxby import urls as bloxby_urls


    urlpatterns = [
        ...
        url(r'^', include(bloxby_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
