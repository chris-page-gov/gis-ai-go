"""Explicit loopback-only execution-service process entry point."""

from __future__ import annotations

import argparse

from .http import DEFAULT_PORT, serve


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the private GIS AI GO execution service")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    arguments = parser.parse_args()
    serve(port=arguments.port)


if __name__ == "__main__":
    main()
