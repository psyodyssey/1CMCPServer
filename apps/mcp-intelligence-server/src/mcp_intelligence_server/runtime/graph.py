"""Minimal dependency-graph scaffolding for intelligence helpers.

Deliberately tiny: a dataclass for nodes, a dataclass for edges and a
dataclass for the graph with an adjacency map. No traversal
algorithms beyond one-hop ``neighbors`` — the real subgraph /
BFS-depth-limited traversal belongs to ``build_dependency_subgraph``
in Step 4+, not here.

Purpose: provide a stable in-memory shape that future public tools
(``analyze_object_dependencies``, ``find_references_to_object``,
``build_dependency_subgraph``, ``estimate_change_impact``,
``find_affected_forms``, ``find_affected_modules``) can fill in and
consume uniformly.

Read-only helpers as a matter of construction — the graph mutates
only in-memory and never touches disk.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DependencyNode:
    """One node in a dependency graph.

    ``name`` is the stable identifier used in adjacency lookups.
    ``kind`` is an optional short tag such as ``"object"``, ``"module"``,
    ``"form"``; intelligence tools pick their own conventions.
    """

    name: str
    kind: str | None = None


@dataclass(frozen=True)
class DependencyEdge:
    """One directed edge in a dependency graph.

    ``from_node`` and ``to_node`` are node names (not full
    :class:`DependencyNode` objects) so edges stay comparable and
    hashable. ``kind`` is an optional short tag such as
    ``"references"`` or ``"binds"``.
    """

    from_node: str
    to_node: str
    kind: str | None = None


@dataclass
class DependencyGraph:
    """Lightweight dependency graph: nodes + edges + adjacency map."""

    nodes: list[DependencyNode] = field(default_factory=list)
    edges: list[DependencyEdge] = field(default_factory=list)
    adjacency: dict[str, list[str]] = field(default_factory=dict)


def empty_graph() -> DependencyGraph:
    """Return a fresh empty :class:`DependencyGraph`."""
    return DependencyGraph()


def add_node(
    graph: DependencyGraph, name: str, *, kind: str | None = None
) -> bool:
    """Add a node by ``name``. Returns ``True`` if inserted, ``False`` if existed.

    Idempotent: re-adding an existing name is a no-op and does not
    overwrite its ``kind``.
    """
    if name in graph.adjacency:
        return False
    graph.nodes.append(DependencyNode(name=name, kind=kind))
    graph.adjacency[name] = []
    return True


def add_edge(
    graph: DependencyGraph,
    from_node: str,
    to_node: str,
    *,
    kind: str | None = None,
) -> None:
    """Record a directed edge ``from_node → to_node``.

    If either endpoint is missing it is inserted with ``kind=None``
    (this keeps edge-first building convenient). Duplicate edges are
    allowed in ``edges`` (they are not deduplicated), but adjacency
    keeps each target at most once per source.
    """
    add_node(graph, from_node)
    add_node(graph, to_node)
    graph.edges.append(
        DependencyEdge(from_node=from_node, to_node=to_node, kind=kind)
    )
    if to_node not in graph.adjacency[from_node]:
        graph.adjacency[from_node].append(to_node)


def neighbors(graph: DependencyGraph, name: str) -> list[str]:
    """Return the list of direct successors of ``name`` (empty if unknown)."""
    return list(graph.adjacency.get(name, ()))
