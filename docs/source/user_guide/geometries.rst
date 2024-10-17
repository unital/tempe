==============
Geometry Types
==============

.. py:currentmodule:: tempe.shape

The :py:class:`~tempe.geometry.Geometry` classes are fairly abstract, and
in particular don't specify what they produce when iterated, other than
some sequence of integers.  However the :py:class:`~tempe.shape.Shape` classes
that use those Geoemtries have expectations about what those sequences look
like.

The following are the specific data types that these objects expect:

.. py:class:: geom

   A generic geometry as a sequence of ints of unspecified length.

.. py:class:: point

   A sequence of ints of the form (x, y).

.. py:class:: points

   A sequence of ints of the form (x0, y0, x1, y1).

.. py:class:: point_array

   An array of signed 16-bit integers giving point coordinates of the
   form ``array('h', [x0, y0, x1, y1, ...])``.

.. py:class:: rectangle

   A sequence of ints of the form (x, y, w, h).

.. py:class:: ellipse

   A sequence of ints of the form (center_x, center_y, radius_x, radius_y).

.. py:class:: point_length

   A sequence of ints of the form (x, y, length).  The length can also be
   used as a size parameter for markers or radius of a circle, as appropriate.
