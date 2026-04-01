*************
Installation
*************

Installing the package is as easy as using ``pip install``, However there are a few considerations that are detailed on this section. Please refer to prerequisites prior to installing the package.

Prerequisites
=============

#. **CEMENTO package.** This is a listed dependency for the ``ASFALTO`` package and will be installed on your system.
#. **draw.io diagram.** Though ``ASFALTO`` only operates on Turtle files, using ``CEMENTO`` and ``draw.io`` allows a more visual approach to editing ontologies and conceptualizing templates and abstractions.
#. **A plain text editor.** ``ASFALTO`` functions revolve around the manipulation and serialization of Turtle (``.ttl``) files. Please makes sure to have a text editor installed to inspect and check the output of ``ASFALTO`` functions.
#. **Stable internet connection (on first use).** ``ASFALTO`` will require the download of two critical prerequisite applications—``OTTR`` and ``ROBOT``—that it uses under the hood. The program will attempt to download both as ``.jar`` files that become cached and used for subsequent ``ASFALTO`` calls.
#. **A Java Runtime Environment (JRE).** ``ASFALTO`` requires the use of two Java based applications, ``OTTR`` and ``ROBOT``, in order to function. If the user is unable to install ``java`` on their system, ASFALTO has the asfalto java_setup command to download an lightweight open-source JRE from Adoptium (Eclipse Foundation). Check the relevant section below for more information.

Standard PyPi installation
==========================

We recommend users to install their package in a virtual environment. To create a virtual environment, you can refer to the following command:

.. code-block:: console

    (.venv) $ python3 -m venv <environment-name>

We strongly suggest an environment name of ``.venv`` or ``.asfalto`` to follow along with the user guide. Activate the environment with:

.. code-block:: console

    (.venv) $ source <environment-name>/bin/activate

Once activated, go ahead and install the package as usual.

.. code-block:: console

    (.venv) $ pip install asfalto

Afterwards, the user should now be able to use the asfalto keyword on their terminal.

**NOTE:** Feel free to use non-native environment managers like `conda <https://anaconda.org/anaconda/conda>`_ and `mamba <https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html>`_. As long as yours has access to ``pypi``, you are good to go.

Dependency Downloads
====================

When ASFALTO is first called with any accompanying command, the package will attempt to download two critical dependencies. The program will terminate if this is not achieved. An internet connection is needed for this initial dependency download.

+--------------+--------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------+
| Program      | Brief Description                                                                                            | Package Use                                                                                                                 | Download URL                                                         |
+==============+==============================================================================================================+=============================================================================================================================+======================================================================+
| OTTR (Lutra) | A framework (and associated application) for creating reusable ontology templates.                           | Template parsing and resolution from template sheets.                                                                       | https://www.ottr.xyz/downloads/lutra/lutra-v0.6.20.jar               |
+--------------+--------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------+
| ROBOT        | A popular ontology toolkit for command-line based ontology creation, modification, reasoning and management. | Used for reasoning capabilities for the verify command. Tools utilized for merging, combining and aggregating turtle files. | https://github.com/ontodev/robot/releases/download/v1.9.10/robot.jar |
+--------------+--------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------+

Note on Java Runtime Environments (JREs)
----------------------------------------

Both ``OTTR`` (Lutra) and ``ROBOT`` require JREs to run on your system. Installing the latest ``java`` version, or at the least, versions ``>= 11``, are strongly recommended to ensure functionality.

If you do not wish to install ``java``, or are unable to do so, ``ASFALTO`` provides the ``java_setup`` subcommand to download and cache a lightweight open-source JRE on your system, courtesy of Acodium. To do so, type the following command:

.. code-block:: console

    (.venv) $ asfalto setup_java

**NOTE:** This step requires an internet connection. Once this is downloaded and cached, future ``ASFALTO`` commands will utilize the JRE to run the ``OTTR`` and ``ROBOT`` commands required by the package.

Note on Download Locations
--------------------------

If you wish to inspect the downloaded entities for debugging or security purposes, ``ASFALTO`` uses the platformdirs package to determine the location of these cached programs. The following table roughly points to where they are located for three operating systems:

+---------------+--------------------------------+
| OS            | Likely Location                |
+===============+================================+
| MacOS         | ~/Library/Application Support/ |
+---------------+--------------------------------+
| Windows       | C:\Users\<User>\AppData\Local  |
+---------------+--------------------------------+
| Kubuntu Linux | ~/.local/share/                |
+---------------+--------------------------------+

Look for the asfalto folder in those locations, to find the cached programs.

If your system is not listed above, or the locations do not show the cached programs even after downloading, you can refer to the ``platformdirs`` documentation and learn more about where the package stores program data.

Installing from the repository
==============================

If you wish to download the developer version of the ``ASFALTO`` codebase, you are free to clone the repository and set up the environment. If you are looking to edit or contribute, we strongly recommend that you download the ``uv`` package manager to handle the package dependencies. You can check how to install ``uv`` here.

To setup a development environment, you can use the following commands:

.. code-block:: console

    (.venv) $ git clone https://github.com/Gabbyton/asfalto
    (.venv) $ cd asfalto
    (.venv) $ uv sync

The last command will attempt to replicate the python environment that was used to develop ``ASFALTO``. If you choose to use another package manager, all dependencies are listed in the pyproject.toml file for your reference.

To get access to the asfalto keyword, you can install the package locally via:

.. code-block:: console

    (.venv) $ uv pip install -e .

This command looks for files associated with any python package and installs the package locally into your system. After doing so, you will now be able to use the asfalto keyword.

After installing ASFALTO, you are now set to start creating ontology templates. You can refer to the next section for information about the example we will be using throughout the user guide.
