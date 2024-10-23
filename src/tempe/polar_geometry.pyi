"""Conversion from polar coordinate geometries to cartesian geometries.

These convert geometries in (r, theta) polar coordinates to cartesian
coordinates.

As elsewhere, all coordinates are integers.  For simplicity this means
that angles are measured in degrees since there is no way to represent
a full revolution in rational numbers of radians.
"""

from math import cos, sin, pi

from .geometry import Geometry, RowGeometry


def polar_points(cx: int, cy: int, geometry: Geometry) -> RowGeometry:
    """Convert (r, theta) point geometry to (x, y) geometry.

    Parameters
    ----------
    cx : int
        The x-coordinate of the center of the polar coordinates.
    cy : int
        The y-coordinate of the center of the polar coordinates.
    geometry : Geometry
        A geometry which produces (r, theta) points when iterated.
        Angles are measured in degrees.

    Returns
    -------
    geometry : RowGeometry
        A geometry which yields (x, y) point coordinates when iterated.
    """

def polar_point_arrays(cx: int, cy: int, geometry: Geometry) -> RowGeometry:
    """Convert (r, theta) point array geometry to (x, y) point array geometry.

    Parameters
    ----------
    cx : int
        The x-coordinate of the center of the polar coordinates.
    cy : int
        The y-coordinate of the center of the polar coordinates.
    geometry : Geometry
        A geometry which produces (r0, theta0, r1, theta1, ...) point arrays
        when iterated.  Angles are measured in degrees.

    Returns
    -------
    geometry : RowGeometry
        A geometry which yields (x0, y0, x1, y1, ...) point coordinates when
        iterated.
    """

def polar_rects(cx: int, cy: int, geometry: Geometry, *, decimation: int = 8):
    """Convert polar annular sector geometry to cartesian polygon geometry.

    Parameters
    ----------
    cx : int
        The x-coordinate of the center of the polar coordinates.
    cy : int
        The y-coordinate of the center of the polar coordinates.
    geometry : Geometry
        A geometry which produces (r, theta, delta_r, delta_theta) coordinates
        corresponding to an annular sector when iterated.  Angles are measured
        in degrees.
    decimation : int
        Factor by which to decimate approximating points in angular arcs.
        Number of polygon vertices is proportional to
        ``(delta_r * delta_theta) >> decimation``.

    Returns
    -------
    geometry : RowGeometry
        A geometry which yields (x0, y0, x1, y1, ...) point coordinates when
        iterated.  Each polygon approximates the corresponding annular sector.
    """

def polar_r_lines(cx: int, cy: int, geometry: Geometry) -> RowGeometry:
    """Convert polar radial lines to cartesian lines.

    Parameters
    ----------
    cx : int
        The x-coordinate of the center of the polar coordinates.
    cy : int
        The y-coordinate of the center of the polar coordinates.
    geometry : Geometry
        A geometry which produces (r, theta, delta_r) coordinates
        corresponding to a radial line segment when iterated.  Angles are
        measured in degrees.

    Returns
    -------
    geometry : RowGeometry
        A geometry which yields (x0, y0, x1, y1) point coordinates when
        iterated.
    """

def polar_theta_lines(
        cx: int,
        cy: int,
        geometry: Geometry,
        *,
        include_center: bool = False,
        decimation: int = 8,
    ) -> RowGeometry:
    """Convert polar arc geometry to cartesian polyline geometry.

    Parameters
    ----------
    cx : int
        The x-coordinate of the center of the polar coordinates.
    cy : int
        The y-coordinate of the center of the polar coordinates.
    geometry : Geometry
        A geometry which produces (r, theta, delta_theta) coordinates
        corresponding to an arc when iterated.  Angles are measured
        in degrees.
    include_center : bool
        Whether the result should include the center point, giving a sector
        instead of an arc.
    decimation : int
        Factor by which to decimate approximating points in angular arcs.
        Number of polygon vertices is proportional to
        ``(delta_r * delta_theta) >> decimation``.

    Returns
    -------
    geometry : RowGeometry
        A geometry which yields (x0, y0, x1, y1, ...) point coordinates when
        iterated.  Each polyline approximates the corresponding arc.
        If the center is included, they it is the last pair of coordinates.
    """

def polar_lines(
        cx: int,
        cy: int,
        geometry: Geometry,
        *,
        include_center: bool = False,
        decimation: int = 8,
    ) -> RowGeometry:
    """Convert polar geodesic lines to cartesian polyline geometry.

    Polar geodesic lines are linear spirals arcs.

    Parameters
    ----------
    cx : int
        The x-coordinate of the center of the polar coordinates.
    cy : int
        The y-coordinate of the center of the polar coordinates.
    geometry : Geometry
        A geometry which produces (r0, theta0, r1, theta1) coordinates
        corresponding to a linear spiral arc when iterated.  Angles are
        measured in degrees.
    include_center : bool
        Whether the result should include the center point, giving a sector
        instead of an arc.
    decimation : int
        Factor by which to decimate approximating points in angular arcs.
        Number of polygon vertices is proportional to
        ``(delta_r * delta_theta) >> decimation``.

    Returns
    -------
    geometry : RowGeometry
        A geometry which yields (x0, y0, x1, y1, ...) point coordinates when
        iterated.  Each polyline approximates the corresponding linear spiral
        arc.
    """
