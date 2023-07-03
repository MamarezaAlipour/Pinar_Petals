==========================
Welcome to PINAR Petals!
==========================

.. image:: img/PINAR_logo_QR.png
   :align: center
   :alt: PINAR Logo

PINAR stands for CLIMate ADAptation and is a probabilistic natural catastrophe impact model, that also calculates averted damage (benefit) thanks to adaptation measures of any kind (from grey to green infrastructure, behavioural, etc.).

PINAR is primarily developed and maintained by the `Weather and Climate Risks Group <https://wcr.ethz.ch/>`_ at `ETH Zürich <https://ethz.ch/en.html>`_.

This is the documentation of the PINAR **Petals** module.
Its purpose is generating different types of hazards and more specialized applications than available in the PINAR Core module.

.. attention::

   PINAR Petals builds on top of PINAR Core and is **not** a standalone module.
   Before you start working with Petals, please check out the documentation of the `PINAR Core <https://pinar-python.readthedocs.io/en/latest/>`_ module, in particular the `installation instructions <https://pinar-python.readthedocs.io/en/latest/guide/install.html>`_.

Jump right in:

* :doc:`README <misc/README>`
* `Installation (Core and Petals) <https://pinar-python.readthedocs.io/en/latest/guide/install.html>`_
* `GitHub Repository <https://github.com/PINAR-project/pinar_petals>`_
* :doc:`Module Reference <pinar_petals/pinar_petals>`

.. ifconfig:: readthedocs

   .. hint::

      ReadTheDocs hosts multiple versions of this documentation.
      Use the drop-down menu on the bottom left to switch versions.
      ``stable`` refers to the most recent release, whereas ``latest`` refers to the latest development version.

.. admonition:: Copyright Notice

   Copyright (C) 2017 ETH Zurich, PINAR contributors listed in :doc:`AUTHORS.md <misc/AUTHORS>`.

   PINAR is free software: you can redistribute it and/or modify it under the
   terms of the GNU General Public License as published by the Free
   Software Foundation, version 3.

   PINAR is distributed in the hope that it will be useful, but WITHOUT ANY
   WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
   PARTICULAR PURPOSE.  See the GNU General Public License for more details.

   You should have received a copy of the GNU General Public License along
   with PINAR. If not, see https://www.gnu.org/licenses/.


.. toctree::
   :hidden:

   GitHub Repositories <https://github.com/PINAR-project>
   PINAR Core <https://pinar-python.readthedocs.io/en/latest/>
   Weather and Climate Risks Group <https://wcr.ethz.ch/>


.. toctree::
   :caption: API Reference
   :hidden:

   Python Modules <pinar_petals/pinar_petals>


.. toctree::
   :caption: Tutorials
   :hidden:
   :maxdepth: 2

   Hazard <tutorial/hazard>
   tutorial/pinar_engine_SupplyChain
   tutorial/pinar_entity_BlackMarble
   tutorial/pinar_exposures_openstreetmap
   tutorial/pinar_hazard_drought
   Crop Production Risk <tutorial/pinar_hazard_entity_Crop>
   Warning Module <tutorial/pinar_engine_Warn>


.. toctree::
   :caption: Miscellaneous
   :hidden:
   :maxdepth: 1

   README <misc/README>
   Changelog <misc/CHANGELOG>
   List of Authors <misc/AUTHORS>
   Contribution Guide <https://pinar-python.readthedocs.io/en/latest/misc/CONTRIBUTING.html>
