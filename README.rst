=============================
Django Bloxby
=============================

.. image:: https://badge.fury.io/py/django-bloxby.svg
    :target: https://badge.fury.io/py/django-bloxby

A django application for bridging bloxby and your django software supporting User creation, package creation and autologin
and also bloxby publishing through FTP to your django application. Though the later needs an intermediate server.


Quick Flow Explanation
----------------------


For your application to communicate with the bloxby builder instance which provides interface for only
:code:`user management`, :code:`package management` and :code:`autologin`, it can do a direct interfacing with
the builder application because the builder application provides APIs for that.

.. image:: https://i.ibb.co/SPRRGB3/Django-Bloxby.png
    :target: https://i.ibb.co/SPRRGB3/Django-Bloxby.png


Quickstart
----------

Install Django Bloxby::

    pip install django-bloxby

Add it to your `INSTALLED_APPS`:

App name you add to INSTALLED_APPS used to be :code:`bloxby` you add to :code:`INSTALLED_APPS` in versions :code:`0.0.19` downwards, but
it has changed in version :code:`0.0.20` since the ftp part has been integrated into the library.

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'djbloxby.bloxby',

        # optional, if you are running the FTP server
        'djbloxby.ftp'
        ...
    )


The following settings are available to you (in :code:`settings.py`), these settings are only necessary for :code:`djbloxby.bloxby`:

.. code-block:: python

    BLOXBY_BUILDER = {
        'url': 'http://clouddigitalmarketing.com',
        'username': 'hello@linkfusions.com',
        'password': 'accountpassword',
        'package_prefix': 'LF-',
        'account_email_prefix': 'LF',
        'public_key': 'Yourpublickeyasstatedinthebloxbyapplicationsettings',
        'autologin_hash': 'Yourautologinhash',
        'default_package_id': 1
    }



- *url*: This is the base url of the server that hosts the bloxby builder.
- *username*: Admin user username
- *password*: Password of an admin user
- *package_prefix*: This could be empty, but it is used to distinguish packages in case of your builder being accessed by more than one application.
- *account_prefix*: Same explanation goes here, in case you have some users shared across your applications.
- *public_key*: API key you generated and saved in the admin settings on your bloxby dashboard.
- *autologin_hash*: The auto login hash which you as well got from the dashboard.
- *default_package_id*: Default package to add for new users being created if none is provided.


Then run migrate command. :code:`python manage.py migrate`.


Usage
-----

Once the settings are configured you could run requests this way:

.. code-block:: python

    from djbloxby.bloxby.functions import Bloxby
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



Template
--------

.. code-block:: html

    <!-- You could autologin user in html by getting the autologin URL for the current user -->

    {% load bloxby %}

    <h1>Click <a href="{% user_builder_dashboard %}">here</a> to login to your builder dashboard.


Setup FTP Server
----------------

**In Production Environment**

This part assumes you have python, pip and virtualenv installed globally on your server.

Make :code:`setup_ftp_server.sh` and :code:`start_ftp_server.sh` executable if they are not already
executable. :code:`chmod u+x setup_ftp_server.sh` and :code:`chmod u+x start_ftp_server.sh`.

Run:

.. code-block:: bash

    ./setup_ftp_server.sh


This installs certain dependencies needed.

** To start the servers **

Run

.. code-block:: bash

    ./start_ftp_server.sh


This starts the FTP server on port 21 and the django server on port 8000. The servers work together, the django server started on port 8000
provides the admin dashboard to manage the external applications that want to receive files through FTP.

So rather than running an FTP server on each and every one of those applications, we'd register them here
and also have this library running on them to allow authentication of users, receipt and processing of files.


These processes are managed by `PM2 <https://pm2.keymetrics.io/docs/usage/quick-start/>`_. So this allows you to use some of the
PM2 commands if you are familiar with them.

For example, you just did a git pull and you want to restart, you could just do:

.. code-block:: bash

    pm2 restart all


This restarts the django server and the ftp server.


Why the Django Server inside of the library
===========================================

The Django server provides admin interface to manage external applications.
You just need to add a model object named :code:`Application` that takes in the auth URL and file receiving URL of the 
external application (these are automatically also provided by this library), this where the FTP server performs 
authentication for users that want to publish pages.

e.g. I have an external application at https://dev.linkfusions.com , and in this external application, I have
:code:`django-bloxby` installed already with the URLs set. I can just add an Application model instance through the FTP server 
instance admin, name it 'dev-fusions', provide the auth url as installed in my external application (How to do this in 
the next section), provide the auth and receiving url and that's all.


How to add the URLs to your external application
================================================

In your :code:`urls.py`, you can add these:

.. code-block:: python

    urlpatterns = [
        ...

        path('bloxby/', include('djbloxby.bloxby.urls')),
        ...
    ]


If I setup this way, my auth URL is going to be :code:`http://<mydomain>/bloxby/ftp/auth/` and my
receiving URL is going to be :code:`http://<mydomain>/bloxby/ftp/receive/`. (These are the URLs you
register in the :code:`Application` model with the FTP server).


How to access the pages published to your external application
==============================================================

A couple of models are made available for this :code:`Template`, :code:`Page`,
:code:`TemplateAsset`. The :code:`Template` is just a sugar-coated name for Website.
It encapsulates the assets and the HTML pages. The :code:`Page` represents the HTML files and they
have two major attributes (functions) which are :code:`render` and :code:`process`.

The :code:`render` function returns HTML string of a page. :code:`process`, swaps all the URLs with
the django application compatible URLs depending on your default file storage, it's only called once
for every page (at initial page request, the very first time the page is being accessed).It parses all the
CSS files also and makes sure their URLs are valid.

The other challenge now is distinguishing Templates which is covered in the next section.


Distinguishing Templates
========================

Coming


Possible Issues
===============

Make sure to set the correct address to the :code:`Site` in admin.

FTP Client is able to connect and authenticate but unable to list directory. Enable passive ports
on your server (where the FTP server runs). In this, passive ports run in the range 60000-65535.
You can enable this by running:


.. code-block:: bash

    sudo ufw allow from ip_address to any port 60000:65535 proto tcp


Where :code:`ip_address` is whatever (domain or IP address) you configure in the :code:`Site`
in admin.


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
