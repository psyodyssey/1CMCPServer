"""Data models for troubleshooting reports."""

from dataclasses import dataclass


@dataclass
class TroubleshootingReport:
    """A single troubleshooting conclusion for a detected problem."""

    problem_code: str
    probable_cause: str
    recommended_action: str
