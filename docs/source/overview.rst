Overview
********

Transmission Line Design Python Toolkit

Composition
===========

Currently there are three sets of tools:

- `rectLTX` : Rectangular waveguide design
- `cylLTX` : Cylindrical waveguide design
- `uStripDesign` : Microstrip design

Installing
==========

Clone this repository wherever you like, but remember to check your path for importing.

Usage
=====

From the Python interpreter: ::

  import LTXKit.rectLTX
  import LTXKit.cylLTX
  import LTXKit.uStripDesign

or: ::

  from LTXKit.rectLTX import *
  from LTXKit.cylLTX import *
  from LTXKit.uStripDesign import *

From there you can call the functions individually. The last method is recommended when you only want one set of tools.

Contributing
============

Currently the toolkit only has functions related to microstrip lines and rectangular waveguides. Contributions appreciated via pull requests.
