***************************************
Normalization and Bottom-up Abstraction
***************************************

In the last section, we encountered a problem where the EPICS Variables we input aren’t showing up on the final file.

This is because the EPICS variable term is actually a reference to another template that comes with its own terms!

You can check this template file with the diagram below. This is our original diagram with the template part highlighted:

.. iframe:: https://viewer.diagrams.net?#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FGabbyton%2asfalto%2Frefs%2Fheads%2Fmaster%2Ffigures%2Fdo-not-input-this-motor-example-fig-3.drawio
    :height: auto
    :width: 100%
    :aspectratio: 1.77
**Figure 1.** Diagram of motor example to be used for guide. You can find the file in the ``examples/motor-example`` folder in the repo.

Through ASFALTO, we can essentially represent one graph with a box inside a diagram! This allows us to use an idea called abstraction, or the practice of representing more complex information with simpler symbols.

However, to expand these abstractions, and fix our missing variable problem, we can use the normalize command:

.. code-block:: console

    (.venv) $ asfalto normalize motor.ttl motor-final ../templates

This command takes all the template Turtle files inside the templates folder and looks for matching terms in our current ``motor.ttl`` file (This is why naming all the templates are important!).

**Tip:** Notice that we work on the turtle file and not the diagram. This is because ASFALTO was made to be neutral about how the Turtle file came to be (but CEMENTO just gives us a visual way to represent our diagrams).

After we normalize, we can proceed as usual with the following commands:

.. code-block:: console

    (.venv) $ asfalto template .
    (.venv) $ asfalto expand motor-template_sheet.csv
    (.venv) $ asfalto merge .

Don’t worry about the template sheet you already populated! ``ASFALTO`` makes sure to retain previously held information even when generating a new template. You will also notice new columns added to the sheet. The ``normalize`` command essentially flattens or normalizes our templates into one, allowing the user to fill up the sheets once!

After these steps, you will now see the EPICS variables represented in the final ``motor-final.ttl`` file!

Bottom Up Abstraction
=====================

Templates you include in a template can also refer to other templates. Leading to multilevel template references from the bottom-up! The diagram below illustrates how this is done on a simpler example:

.. image:: /_static/null-vs-none-figures/fig-2.png
        :width: 700
        :alt: diagrams illustrating the bottom-up abstraction concept
**Figure 2.**  A diagram showing the concept of bottom-up abstraction. Each subsequent layer of templates are used to build the other, until you get to the top level.

And the final sheet will look like:

.. csv-table::
   :file: ../_tables/bottom-up-example-template_sheet.csv
   :header-rows: 1
**Figure 3.** The final sheet after all normalization operations are complete.

The normalize command flattens this to one sheet that contains all the placeholders defined across all three templates. To accomplis this, you will have to perform the normalize command on each sheet, as ``ASFALTO`` only supports normalizing one level at a time.

**NOTE:** We understand normalization can lead to an absurdly large number of columns. We are currently trying to develop ways to identify the most salient columns to place on the left side of CSVs. We are also determining best practices to avoid having to use many columns for sheets.

We have seen how normalization can enable bottom-up abstraction through multi-level template references. But what happens when we want to break those abstractions? The next section discusses ways ASFALTO allows abstractions to connect to triples from a diagram, and the syntax required to make it happen.
