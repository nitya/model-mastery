"""Optional OpenTelemetry hooks that degrade to no-op spans locally."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator


class _NoOpSpan:
    def set_attribute(self, name: str, value: Any) -> None:
        del name, value


@contextmanager
def span(name: str, **attributes: str) -> Iterator[Any]:
    try:
        from opentelemetry import trace
    except ImportError:
        yield _NoOpSpan()
        return

    tracer = trace.get_tracer("product-launch-studio")
    with tracer.start_as_current_span(name) as current:
        for key, value in attributes.items():
            current.set_attribute(key, value)
        yield current


def configure_telemetry(connection_string: str | None) -> None:
    if not connection_string:
        return
    try:
        from azure.monitor.opentelemetry import configure_azure_monitor
    except ImportError as exc:
        raise RuntimeError(
            "APPLICATIONINSIGHTS_CONNECTION_STRING is set, but "
            "azure-monitor-opentelemetry is not installed"
        ) from exc
    configure_azure_monitor(connection_string=connection_string)
