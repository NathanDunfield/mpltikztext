===========
mpltikztext
===========

Saving Matplotlib figures so that all text becomes a TikZ overlay.
This allows for easy customization of the text on the LaTeX
side. Nominally for use with the LaTeX style ``nmd/graphics`` from `my
personal document class
<https://bitbucket.org/nathan_dunfield/latex_class>`_, though it only
depends on a few lines of that.


Installation
============

Assuming you are using Python 3, do::

  python3 -m pip install -U https://bitbucket.org/nathan_dunfield/mpltikztext/get/tip.zip


Examples and testing
====================

Download the `source code zipfile
<https://bitbucket.org/nathan_dunfield/mpltikztext/get/tip.zip>`_ and
in the resulting directory do::

  cd examples
  python3 sine_wave.py
  pdflatex sine_wave.tex
  python3 scatter.py
  pdflatex scatter.tex

See the above Python and TeX files for more on usage.


License
=======

Copyright Nathan Dunfield, 2014-present.  Released under the terms of
the GNU General Public License, version 2 or later.

