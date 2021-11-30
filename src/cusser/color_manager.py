"""Utilities for managing colors and color pairs in curses."""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable, Optional, Text

import ochre


@dataclass
class ColorPair:
    """A color pair of foreground and background colors."""

    # TODO: move this to ochre
    foreground: Optional[ochre.Color] = None
    background: Optional[ochre.Color] = None



def encode(
    value: Optional[ochre.Color] | ColorPair,
) -> Optional[Text] | tuple[Optional[Text], Optional[Text]]:
    """Encode a color or color pair into optional strings to use as dictionary keys."""
    if value is None:
        return None

    if isinstance(value, ochre.Color):
        return hex(value)

    if isinstance(value, ColorPair):
        return (
            hex(value.foreground) if value.foreground else None,
            hex(value.background) if value.background else None,
        )

    raise TypeError(f"Unsupported type: {type(value)}")


@dataclass
class ColorManager:
    """A class for managing curses colors and color pairs."""

    color_indices: dict[Optional[Text], int] = field(default_factory=lambda: {None: -1})
    next_color_index = 0

    pair_indices: dict[tuple[Optional[Text], Optional[Text]], int] = field(
        default_factory=lambda: {(None, None): -1}
    )
    next_pair_index = 0

    on_add_color: Optional[Callable[[ochre.Color, ColorManager], None]] = None
    on_add_pair: Optional[Callable[[ColorPair, ColorManager], None]] = None

    current_pair: ColorPair = ColorPair()

    @property
    def foreground(self) -> ochre.Color:
        """Return the current foreground color."""
        return self.current_pair.foreground

    @property
    def background(self) -> ochre.Color:
        """Return the current background color."""
        return self.current_pair.background

    @foreground.setter
    def foreground(self, color: ochre.Color) -> None:
        """Set the current foreground color."""
        self.current_pair.foreground = color
        self.add_color(color)
        self.add_pair(self.current_pair)

    @background.setter
    def background(self, color: ochre.Color) -> None:
        """Set the current background color."""
        self.current_pair.background = color
        self.add_color(color)
        self.add_pair(self.current_pair)

    def add(self, value: Optional[ochre.Color] | ColorPair) -> None:
        """Register a color or color pair with the color manager."""
        if value is None or isinstance(value, ochre.Color):
            self.add_color(value)
        elif isinstance(value, ColorPair):
            self.add_pair(value)
        else:
            raise TypeError(f"Unsupported type: {type(value)}")

    def add_color(self, color: Optional[ochre.Color], callback: bool = True) -> None:
        """Register a color with the color manager."""
        c = encode(color)
        if c in self.color_indices:
            return

        self.color_indices[c] = self.next_color_index
        self.next_color_index += 1
        if callback and self.on_add_color:
            self.on_add_color(color, self)

    def add_pair(self, pair: ColorPair, callback: bool = True) -> None:
        """Register a color pair with the color manager."""
        self.add_color(pair.foreground)
        self.add_color(pair.background)

        p = encode(pair)
        if p in self.pair_indices:
            return

        self.pair_indices[p] = self.next_pair_index
        self.next_pair_index += 1
        if callback and self.on_add_pair:
            self.on_add_pair(pair, self)

    def discard(self, value: Optional[ochre.Color] | ColorPair) -> None:
        """Unregister a color or color pair from the color manager."""
        if value is None or isinstance(value, ochre.Color):
            self.discard_color(value)
        elif isinstance(value, ColorPair):
            self.discard_pair(value)
        else:
            raise TypeError(f"Unsupported type: {type(value)}")

    def discard_color(self, color: Optional[ochre.Color]) -> None:
        """Unregister a color from the color manager."""
        c = encode(color)
        if c not in self.color_indices:
            return

        del self.color_indices[c]

    def discard_pair(self, pair: ColorPair) -> None:
        """Unregister a color pair from the color manager."""
        p = encode(pair)
        if p not in self.pair_indices:
            return

        del self.pair_indices[p]

    @property
    def colors(self) -> Iterable[ochre.Color]:
        """Return all colors currently registered."""
        return map(
            lambda c: ochre.Hex(c) if c is not None else None, self.color_indices.keys()
        )

    @property
    def pairs(self) -> Iterable[ColorPair]:
        """Return all color pairs currently registered."""
        return map(
            lambda p: ColorPair(
                foreground=ochre.Hex(p[0]) if p[0] is not None else None,
                background=ochre.Hex(p[1]) if p[1] is not None else None,
            ),
            self.pair_indices.keys(),
        )

    def __getitem__(self, value: Optional[ochre.Color] | ColorPair) -> int:
        """Return the index of a color or color pair."""
        if value is None or isinstance(value, ochre.Color):
            return self.color_indices[encode(value)]

        if isinstance(value, ColorPair):
            return self.pair_indices[encode(value)]

        raise TypeError(f"Unsupported type: {type(value)}")

    def __contains__(self, value: Optional[ochre.Color] | ColorPair) -> bool:
        """Return whether a color or color pair is registered."""
        if value is None or isinstance(value, ochre.Color):
            return encode(value) in self.color_indices

        if isinstance(value, ColorPair):
            return encode(value) in self.pair_indices

        raise TypeError(f"Unsupported type: {type(value)}")

    def __iter__(self) -> Iterable[ochre.Color]:
        """Return an iterator over all colors currently registered."""
        return self.colors

    def __len__(self) -> int:
        """Return the number of colors currently registered."""
        return len(self.color_indices)
