************************************
Named Individuals, Classes and Types
************************************

For ``ASFALTO``, an ontology template is a turtle file composed of classes, named individuals (also called as instances), literals and blank nodes where each named individual (except for properties) and literal are treated as placeholders for values that will be input in a sheet.

Converting from draw.io to Template
===================================

The following diagram walks you through the key distinctions between the three types of acceptable inputs:

.. iframe:: https://viewer.diagrams.net?#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FGabbyton%2Fasfalto%2Frefs%2Fheads%2Fmain%2Ffigures%2Fdo-not-input-this-motor-example-fig-2.drawio
    :height: auto
    :width: 100%
    :aspectratio: 1.77
Having trouble? Download the figure above as a :download:`draw.io diagram <https://raw.githubusercontent.com/Gabbyton/asfalto/refs/heads/main/figures/do-not-input-this-happy-motor-example-fig-2.drawio>`.

For the purposes of the package, using the rdf:type between an individual and a class indicates the former as a placeholder. Using any kind of literal connected to a named individual will mark that literal as a placeholder value.

**NOTE:**  Some named individuals that could be used in templates may be fixed members of enumerations. The ``ASFALTO`` package currently does not support their use. Enumeration-member named individuals will be treated like placeholders.

Once you have the terms in the diagram defined, you can now use the CEMENTO package to convert into a turtle file:

.. code-block:: console

    (.venv) $ cemento drawio_ttl motor.drawio motor.ttl

Then afterwards, you can now use ``ASFALTO`` to generate the template

.. code-block:: console

    (.venv) $ asfalto template motor.ttl .

An Unexpected Error
-------------------

In some cases, you may encounter the following error:

::

    ValueError: Cannot automatically name the template if the template head is not defined. Did you forget to add `isTemplateHead`?

This error arises because every Turtle file in ``ASFALTO`` is treated as a template, and any template you declare must have a name! To do so, ``ASFALTO`` uses the required keyword isTemplateHead which you attach to the head of the template.


What is a Head Node?
--------------------

A head node is the focal point of the template. In our case, the focal point of the template is the motor and the motor has a triple that designates it as the head. Practically, this means the ``motor.ttl`` file is about the motor, and any term included into it is associated with, named after, and about the motor term. Head nodes must be named IRI terms.

 The ``ASFALTO`` package treats all templates as ego-centric, and recommends users to separate templates by different focal points, rather than putting them into one big file.

**NOTE:** This feature is a design choice made by the developers to ensure ``ASFALTO`` is only used for abstraction and reduced repetition. Though ``ASFALTO`` could theoretically be used for linked data mapping and KG population, we recommend sticking with the FAIRLinked package for these purposes.

After you get the ``motor-template_sheet.csv`` file, you are now ready to start populating the template sheet. The next section deals with this step, including important information about the two kinds of null values.



