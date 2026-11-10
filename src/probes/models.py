"""Django model discovery entrypoint for the probes app."""

from probes.infrastructure.models import ProbeRecord

__all__ = ["ProbeRecord"]
