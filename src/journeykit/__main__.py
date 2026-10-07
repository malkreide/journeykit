"""``python -m journeykit`` - Einstieg ohne PATH-Abhängigkeit (Windows-Nutzerinstallationen)."""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
