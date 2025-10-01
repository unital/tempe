# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

from .raster import Raster
from .surface import Surface
from .shapes import Shape


class Window(Shape):
    """A Shape which displays a surface."""

    def __init__(self, offset=None, *, surface=None, clip=None):
        super().__init__(surface, clip)
        if offset is None:
            if clip is not None:
                offset = clip[:2]
            else:
                offset = (0, 0)
        self.offset = offset
        self.subsurface = Surface()

    def draw_raster(self, raster):
        x, y = self.offset
        # new raster translated to subsurface coordinates
        if self.clip is None:
            raster = raster.clip(self.clip)
            raster.x -= x
            raster.y -= y
        else:
            raster = Raster(
                raster.buf,
                raster.x - x,
                raster.y - y,
                raster.w,
                raster.h,
                raster.stride,
                raster.offset,
            )
        self.subsurface.draw(raster)

    def update(self, offset=None):
        if offset is None:
            if self.surface:
                for rect in self.subsurface._damage:
                    x, y, w, h = rect
                    self.surface.damage(
                        (
                            (x + self.offset[0]),
                            (y + self.offset[1]),
                            w,
                            h,
                        )
                    )
            self.subsurface._damage = []
            self.subsurface.refresh_needed.clear()
        elif self.clip is None:
            # invalidate old drawing areas
            for layer_shapes in self.subsurface.layers.values:
                for shape in layer_shapes:
                    shape.update()
            self.update()
            # shift
            self.offset = offset
            # invalidate new drawing areas
            for layer_shapes in self.subsurface.layers.values:
                for shape in layer_shapes:
                    shape.update()
            self.update()
        else:
            self.offset = offset
            if self.surface:
                self.surface.damage(self.clip)
