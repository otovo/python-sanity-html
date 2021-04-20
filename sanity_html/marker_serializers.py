from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Type

    from sanity_html.types import Block, Span


class MarkerSerializer:
    """Base class for marker definition handlers."""

    tag: str

    @classmethod
    def render_prefix(cls: Type[MarkerSerializer], span: Span, marker: str, context: Block) -> str:
        """Render the prefix for the marked span.

        Usually this this the opening of the HTML tag.
        """
        return f'<{cls.tag}>'

    @classmethod
    def render_suffix(cls: Type[MarkerSerializer], span: Span, marker: str, context: Block) -> str:
        """Render the suffix for the marked span.

        Usually this this the closing of the HTML tag.
        """
        return f'</{cls.tag}>'

    @classmethod
    def render(cls: Type[MarkerSerializer], span: Span, marker: str, context: Block) -> str:
        """Render the marked span directly with prefix and suffix."""
        result = cls.render_prefix(span, marker, context)
        result += str(span.text)
        result += cls.render_suffix(span, marker, context)
        return result


# Decorators


class DefaultMarkerSerializer(MarkerSerializer):
    """Marker used for unknown definitions."""

    tag = 'span'


class EmphasisSerializer(MarkerSerializer):
    """Marker definition for <em> rendering."""

    tag = 'em'


class StrongSerializer(MarkerSerializer):
    """Marker definition for <strong> rendering."""

    tag = 'strong'


class CodeSerializer(MarkerSerializer):
    """Marker definition for <code> rendering."""

    tag = 'code'


class UnderlineSerializer(MarkerSerializer):
    """Marker definition for <u> rendering."""

    tag = 'span'

    @classmethod
    def render_prefix(cls: Type[MarkerSerializer], span: Span, marker: str, context: Block) -> str:
        """Render the span with the appropriate style for underline."""
        return '<span style="text-decoration:underline;">'


class StrikeThroughSerializer(MarkerSerializer):
    """Marker definition for <strike> rendering."""

    tag = 'del'


# Annotations


class LinkSerializer(MarkerSerializer):
    """Marker definition for link rendering."""

    tag = 'a'

    @classmethod
    def render_prefix(cls: Type[MarkerSerializer], span: Span, marker: str, context: Block) -> str:
        """Render the opening anchor tag with the href attribute set.

        The href attribute is fetched from the provided block context using
        the provided marker key.
        """
        marker_definition = next((md for md in context.markDefs if md['_key'] == marker), None)
        if not marker_definition:
            raise ValueError(f'Marker definition for key: {marker} not found in parent block context')
        href = marker_definition.get('href', '')
        return f'<a href="{href}">'


class CommentSerializer(MarkerSerializer):
    """Marker definition for HTML comment rendering."""

    tag = '!--'

    @classmethod
    def render_prefix(cls: Type[MarkerSerializer], span: Span, marker: str, context: Block) -> str:
        """Render the opening of the HTML comment block."""
        return '<!-- '

    @classmethod
    def render_suffix(cls: Type[MarkerSerializer], span: Span, marker: str, context: Block) -> str:
        """Render the closing part of the HTML comment block."""
        return ' -->'