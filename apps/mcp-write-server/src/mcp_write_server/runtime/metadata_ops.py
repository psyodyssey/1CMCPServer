"""Internal metadata patch helper layer for mcp-write-server runtime.

This module is **internal**. It is intended to be consumed by future
metadata tools of Phase 3 / Step 4–6 and Phase 6 / Step 5, but is
not registered as a public tool and never returns ``ToolResult``.
Helpers operate on plain strings, concrete file paths, or
``xml.etree.ElementTree`` trees: no network I/O, no subprocess,
no audit, no snapshots — those responsibilities belong to the tool
layer (``tools.py``) and the write-flow pipeline
(``runtime/flow.py``).

Failure is loud: a missing XML block, malformed XML, or an unreadable
file raises a plain ``ValueError`` / ``ET.ParseError`` / ``OSError``
respectively, without silent fallbacks.

BSL fragment format: methods are emitted as ``Процедура`` blocks
with an optional ``Экспорт`` directive. This is the single canonical
format this layer exposes; richer shapes (functions, directives,
annotations) are out of scope for Step 3.

Structural XML editing (Phase 6 / Step 5): the
``parse_xml_file`` / ``write_xml_file`` /
``find_form_element`` / ``get_or_create_form_attributes_block`` /
``add_attribute_to_form_attributes_block`` /
``form_has_attribute`` set provides the first true DOM-style edit
path on top of stdlib ``xml.etree.ElementTree``, used by the
``add_form_attribute`` tool. Scope is intentionally narrow:
- no XML namespace handling (test fixtures and Phase 3 tools use
  un-namespaced cards; namespaced 1cv8 cards are out of scope for
  this slice and would need explicit namespace plumbing);
- no whitespace / pretty-print preservation (ElementTree does not
  round-trip arbitrary XML byte-for-byte);
- empty containers stay open (``<Tag></Tag>``) rather than
  self-closing, to keep substring-based tools (e.g.
  ``add_form_element``'s ``</Elements>`` lookup) compatible.
The narrow path stays additive: existing string-based helpers
(``insert_fragment_into_named_block``, ``patch_xml_file``, …) are
not removed and the long-existing ``add_catalog_attribute`` /
``add_document_attribute`` tools keep using them.
"""

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Callable

_BSL_METHOD_RE_TEMPLATE = (
    r"\b(Процедура|Функция|Procedure|Function)\s+{name}\s*\("
)


# ---------------------------------------------------------------------------
# XML / text structural helpers
# ---------------------------------------------------------------------------


def load_xml_text(path: Path) -> str:
    """Read ``path`` as UTF-8 XML text. ``OSError`` propagates."""
    return Path(path).read_text(encoding="utf-8")


def insert_before_last_closing_tag(xml_text: str, fragment: str) -> str:
    """Insert ``fragment`` before the last ``</...>`` in ``xml_text``.

    Fallback helper for cases where no specific named block is known.
    Prefer :func:`insert_fragment_into_named_block` when the target
    block can be addressed by name.

    Raises:
        ValueError: if ``xml_text`` contains no closing tag at all.
    """
    close_idx = xml_text.rfind("</")
    if close_idx == -1:
        raise ValueError("No closing tag found in XML text.")
    return xml_text[:close_idx] + fragment + xml_text[close_idx:]


def insert_fragment_into_named_block(
    xml_text: str,
    block_name: str,
    fragment: str,
) -> str:
    """Insert ``fragment`` inside ``<block_name>...</block_name>``.

    The fragment lands just before the closing tag of the first
    occurrence of the named block. The block must be paired
    (open + close); a self-closing ``<block_name/>`` does not
    qualify.

    Raises:
        ValueError: if ``xml_text`` does not contain a matching
            open/close pair for ``block_name``.
    """
    closing_tag = f"</{block_name}>"
    if closing_tag not in xml_text:
        raise ValueError(
            f"XML block <{block_name}> not found (no closing tag)."
        )
    opening_plain = f"<{block_name}>"
    opening_with_attrs = f"<{block_name} "
    if opening_plain not in xml_text and opening_with_attrs not in xml_text:
        raise ValueError(
            f"XML block <{block_name}> not found (no opening tag)."
        )
    idx = xml_text.find(closing_tag)
    return xml_text[:idx] + fragment + xml_text[idx:]


# ---------------------------------------------------------------------------
# Metadata XML / BSL fragment builders
# ---------------------------------------------------------------------------


def build_attribute_fragment(
    name: str,
    attr_type: str,
    synonym: str | None = None,
) -> str:
    """Build a minimal ``<Attribute>`` XML fragment."""
    if synonym:
        return (
            f'<Attribute name="{name}">'
            f"<Type>{attr_type}</Type>"
            f"<Synonym>{synonym}</Synonym>"
            f"</Attribute>"
        )
    return (
        f'<Attribute name="{name}">'
        f"<Type>{attr_type}</Type>"
        f"</Attribute>"
    )


def build_form_fragment(form_name: str) -> str:
    """Build a minimal ``<Form>`` XML stub fragment.

    Intended as an internal building block for form-creation tools;
    not a complete 1C managed form card. Contains an empty
    ``<Elements></Elements>`` block so that subsequent
    ``add_form_element`` calls have a deterministic insertion point.
    """
    return (
        f'<Form name="{form_name}">'
        f"<Type>ManagedApplicationForm</Type>"
        f"<Elements></Elements>"
        f"</Form>"
    )


def build_module_method_fragment(
    method_name: str,
    body: str,
    export: bool = False,
) -> str:
    """Build a BSL ``Процедура`` block, optionally with ``Экспорт`` directive.

    The chosen canonical format is Cyrillic procedure syntax:

    ``Процедура <name>() [Экспорт]\\n<body>\\nКонецПроцедуры\\n``.
    """
    export_directive = " Экспорт" if export else ""
    return (
        f"Процедура {method_name}(){export_directive}\n"
        f"{body}\n"
        f"КонецПроцедуры\n"
    )


# ---------------------------------------------------------------------------
# Structural XML helpers (Phase 6 / Step 5)
# ---------------------------------------------------------------------------
#
# These helpers operate on ``xml.etree.ElementTree`` (stdlib only) and
# are the first DOM-style edit path in the metadata helper layer. They
# are intentionally narrow: only the operations the
# ``add_form_attribute`` tool needs. No "universal XML framework"
# pretensions — the substring helpers above remain the path of choice
# for everything else.


def parse_xml_file(path: Path) -> ET.ElementTree:
    """Parse an XML file from disk into an ``ElementTree``.

    ``OSError`` (file missing, permission, …) and
    ``xml.etree.ElementTree.ParseError`` (malformed XML) propagate
    unchanged — this is fail-loud by design; the caller (write-flow
    operation) translates exceptions into ``ToolResult(ok=False, ...)``
    via the standard flow boundary.
    """
    return ET.parse(Path(path))


def write_xml_file(path: Path, tree: ET.ElementTree) -> None:
    """Serialize ``tree`` back to ``path`` as UTF-8 with an XML declaration.

    ``short_empty_elements=False`` is passed deliberately so that
    empty containers stay as ``<Tag></Tag>`` rather than collapsing
    to ``<Tag/>``. Two reasons:
    - existing substring-based tools (``add_form_element``, future
      slices) rely on a literal ``</Tag>`` closing token to find
      insertion points;
    - operator-readable diffs are easier to follow when the open/close
      pair stays visible.

    ``OSError`` propagates unchanged.
    """
    tree.write(
        Path(path),
        encoding="utf-8",
        xml_declaration=True,
        short_empty_elements=False,
    )


def find_form_element(root: ET.Element, form_name: str) -> ET.Element | None:
    """Find the first ``<Form name="form_name">`` descendant of ``root``.

    Search is recursive (``Element.iter("Form")``): real 1С object
    cards typically nest forms under
    ``<ChildObjects><Forms>`` while the test fixtures used here
    place ``<Form>`` directly under ``<Catalog>`` / ``<Document>``.
    Both shapes are handled. Returns ``None`` if no ``Form`` element
    with that ``name`` attribute is present anywhere under ``root``.
    """
    for elem in root.iter("Form"):
        if elem.get("name") == form_name:
            return elem
    return None


def get_or_create_form_attributes_block(form_elem: ET.Element) -> ET.Element:
    """Return ``form_elem``'s ``<Attributes>`` child, creating it if absent.

    On creation the new ``<Attributes></Attributes>`` element is
    appended at the end of ``form_elem``'s children — no clever
    re-ordering, no whitespace shimming. The caller writes the tree
    back via :func:`write_xml_file`, which preserves the open/close
    pair shape thanks to ``short_empty_elements=False``.

    Mutates ``form_elem`` in place when the block is created.
    """
    attrs = form_elem.find("Attributes")
    if attrs is None:
        attrs = ET.SubElement(form_elem, "Attributes")
    return attrs


def add_attribute_to_form_attributes_block(
    attributes_block: ET.Element,
    name: str,
    attr_type: str,
    synonym: str | None = None,
) -> ET.Element:
    """Append a new ``<Attribute name="name">`` element to ``attributes_block``.

    Shape produced (matches what the existing
    ``build_attribute_fragment`` text helper would emit, just built
    via DOM):

    .. code-block:: xml

        <Attribute name="...">
          <Type>...</Type>
          <Synonym>...</Synonym>   <!-- only when synonym is truthy -->
        </Attribute>

    No de-duplication / replacement is done here — the caller is
    expected to have first checked uniqueness via
    :func:`form_has_attribute`. Returns the newly-created element.
    """
    attribute = ET.SubElement(attributes_block, "Attribute", attrib={"name": name})
    type_elem = ET.SubElement(attribute, "Type")
    type_elem.text = attr_type
    if synonym:
        syn_elem = ET.SubElement(attribute, "Synonym")
        syn_elem.text = synonym
    return attribute


def form_has_attribute(form_elem: ET.Element, attribute_name: str) -> bool:
    """Return ``True`` iff ``form_elem`` already has an ``<Attribute name=...>``.

    Looks **only** inside the form's own ``<Attributes>`` child(ren)
    — object-level attributes (the ``<Attributes>`` block at
    ``<Catalog>``/``<Document>`` level) are deliberately not
    consulted here, since they are a different metadata surface.
    """
    for attrs in form_elem.iterfind("Attributes"):
        for attr in attrs.iterfind("Attribute"):
            if attr.get("name") == attribute_name:
                return True
    return False


# ---------------------------------------------------------------------------
# BSL helpers
# ---------------------------------------------------------------------------


def module_contains_method(module_text: str, method_name: str) -> bool:
    """Return True if ``module_text`` declares a method named ``method_name``.

    Detection is lenient: matches a ``Процедура`` / ``Функция``
    (or Latin ``Procedure`` / ``Function``) keyword followed by the
    method name and an opening parenthesis, case-insensitively.
    Not a full BSL parser.
    """
    pattern = re.compile(
        _BSL_METHOD_RE_TEMPLATE.format(name=re.escape(method_name)),
        re.IGNORECASE,
    )
    return bool(pattern.search(module_text))


def append_method_to_module(
    module_text: str,
    method_fragment: str,
) -> str:
    """Append ``method_fragment`` to ``module_text`` with predictable separators.

    A leading ``\\n`` separator is inserted only if ``module_text``
    does not already end with a newline; a trailing ``\\n`` is
    appended if ``method_fragment`` does not already end with one.
    """
    separator = "" if not module_text or module_text.endswith("\n") else "\n"
    trailing = "" if method_fragment.endswith("\n") else "\n"
    return f"{module_text}{separator}{method_fragment}{trailing}"


# ---------------------------------------------------------------------------
# File patch helpers
# ---------------------------------------------------------------------------


def patch_xml_file(path: Path, patcher: Callable[[str], str]) -> None:
    """Read an XML file, transform its text via ``patcher``, write UTF-8 back.

    Errors from the filesystem (``OSError``) propagate unchanged.
    """
    target = Path(path)
    text = target.read_text(encoding="utf-8")
    target.write_text(patcher(text), encoding="utf-8")


def patch_text_file(path: Path, patcher: Callable[[str], str]) -> None:
    """Read a text (BSL/plain) file, transform, and write UTF-8 back."""
    target = Path(path)
    text = target.read_text(encoding="utf-8")
    target.write_text(patcher(text), encoding="utf-8")
