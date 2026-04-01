*************
Introduction
*************

Throughout the user guide, we will be taking beamline motors as an example for how to use ASFALTO. This example also illustrates the impetus behind the project: a means to streamline the management of thousands of similar components of large systems like beamline facilities.

The Data
========

The full diagram can be found below:

.. iframe:: https://viewer.diagrams.net?#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FGabbyton%2Fasfalto%2Frefs%2Fheads%2Fmain%2Ffigures%2Fdo-not-input-this-slit-motor-example-fig-1.drawio
    :height: auto
    :width: 100%
    :aspectratio: 1.77
**Figure 1.** Diagram of motor example to be used for guide. You can find the file in the ``examples/motor-example`` folder in the repo.

The data table to populate it is found below:

.. csv-table::
   :file: ../_tables/motor-template_sheet-populated.csv
   :header-rows: 1
**Figure 1.** Table of populated template sheet to be used in this user guide. You can find the file as ``motor-template-sheet-populated.csv`` in the ``examples/motor-example`` folder in the repo.

These files can be found in the ``examples/motor-example`` folder in the repository for your reference. Please make sure to work in one folder for each template that you use. We will show you later how to refer to other templates (from other folders in subsequent sections).

User Guide Overview
===================

As an overview, we will be performing the following steps:

1. Creating a template, and differentiating between named individuals, classes and types
2. Generating the template sheet, and learning about two types of placeholder values: inherited defaults and explicit absence (Null vs. None)
3. Applying Normalization, and how we can use ASFALTO to achieve Bottom-up Abstraction
4. Breaking abstraction, either through cross-level triples, or via named template instances

The next section will focus on Step 1, and delineate the various components that go into creating a template diagram.