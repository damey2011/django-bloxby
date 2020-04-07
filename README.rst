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


Quickstart
----------

Install Django Bloxby::

    pip install django-bloxby

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'bloxby',
        ...
    )


The following settings are available to you (in settings.py):

.. code-block:: python

    BLOXBY_BUILDER = {
        'url': 'http://clouddigitalmarketing.com',
        'username': 'hello@linkfusions.com',
        'password': 'accountpassword',
        'package_prefix': 'LF-',
        'account_email_prefix': 'LF',
        'public_key': 'Yourpublickeyasstatedinthebloxbyapplicationsettings',
        'autologin_hash': 'Yourautologinhash'
    }



- *url*: This is the base url of the server that hosts the bloxby builder.
- *username*: Admin user username
- *password*: Password of an admin user
- *package_prefix*: This could be empty, but it is used to distinguish packages in case of your builder being accessed by more than one application.
- *account_prefix*: Same explanation goes here, in case you have some users shared across your applications.
- *public_key*: API key you generated and saved in the admin settings on your bloxby dashboard.
- *autologin_hash*: The auto login hash which you as well got from the dashboard.


Usage
-----

Once the settings are configured you could run requests this way:

.. code-block:: python

    from bloxby.functions import Bloxby
    b = Bloxby()
    # Retrieve User with id of 4
    b.Users.retrieve(4)
    # Update user with id of 4
    b.Users.update(4, last_name='New')
    # Create new user
    b.Users.create(first_name='John', last_name='Felix', email='jfelix@localhost.com', password=generate_password(), type='User', package_id=5)

    # Working with Packages
    b.Packages.create(name='New Free Package', sites_number=10,
                      disk_space=100,
                      export_site=True,
                      ftp_publish=True, price=4.00, currency='USD')
    # .....
    # Could also do .update, .retrieve, .delete with this.


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
