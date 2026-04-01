.. ASFALTO documentation master file, created by
   sphinx-quickstart on Mon Jul 21 10:58:46 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. meta::
    :google-site-verification: IR9RTySb3FPwmbsK5FVfOqHoVuhW1P2WqIq9n8hWxhg

.. image:: /_static/logo.svg
    :width: 250px
    :class: homepage-logo

***********
ASFALTO
***********

.. toctree::
   :maxdepth: 1
   :hidden:

   quickstart
   user-guide
   modules
   faqs
   about
   changelog
   license-info/licenses

**Version:** |release|

**Useful links**:
`Source Repository <https://github.com/Gabbyton/asfalto>`_ |
`Issue Tracker <https://github.com/Gabbyton/asfalto/issues>`_ |
`PyPI Page <https://pypi.org/project/asfalto/>`_


``ASFALTO`` is a python package for creating, generating and reusing ontology templates to accelerate ontology and Knowledge Graph development, especially for systems with multiple structurally similar components.
The ``ASFALTO`` package can:

- convert turtle files with named individuals into template sheets over those individuals.
- expand a template ``csv`` into a turtle file with all specified component variations.
- generate reusable templates that can be utilized in other turtle files, enabling "bottom-up" abstraction.
- perform consistency checks on templates prior to reuse.

``ASFALTO`` currently supports turtle files only.

.. grid:: 2
   
    .. grid-item-card::
        :img-top: _static/running_person.svg

        Quick Start
        ^^^^^^^^^^^

        Do you want to reduce repetitions? Check out our quick start guide to get started on creating templates and filling up sheets.

        +++

        .. button-ref:: quickstart
            :expand:
            :color: dark
            :click-parent:

            To Quick Start

    .. grid-item-card::
        :img-top: _static/book.svg

        Guide
        ^^^^^

        A detailed guide for using the CLI and the scripting tools.

        +++

        .. button-ref:: user-guide
            :expand:
            :color: dark
            :click-parent:

            To the User Guide

    .. grid-item-card::
        :img-top: _static/more.svg

        API Reference
        ^^^^^^^^^^^^^

        The full documentation for all things ASFALTO.

        +++

        .. button-ref:: modules
            :expand:
            :color: dark
            :click-parent:

            To the API Reference


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`