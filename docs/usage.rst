=====
Usage
=====

To use Django Bloxby in a project, add it to your `INSTALLED_APPS`:

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
