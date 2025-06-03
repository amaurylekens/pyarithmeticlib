# read version from installed package
from importlib.metadata import PackageNotFoundError, version

try:  # pragma: no cover - used only when package is installed
    __version__ = version("pyarithmeticlib")
except PackageNotFoundError:  # pragma: no cover - fallback for tests
    __version__ = "0.0.0"
