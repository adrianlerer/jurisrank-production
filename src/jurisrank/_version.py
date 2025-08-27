"""Version information for JurisRank package."""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)

# Release information
MAJOR = 1
MINOR = 0  
PATCH = 0

# Build metadata
BUILD_DATE = "2025-08-27"
BUILD_TYPE = "stable"
API_VERSION = "v1"

def get_version_string():
    """Get formatted version string."""
    return f"{MAJOR}.{MINOR}.{PATCH}"

def get_full_version():
    """Get full version with metadata."""
    return {
        "version": __version__,
        "build_date": BUILD_DATE,
        "build_type": BUILD_TYPE,
        "api_version": API_VERSION
    }
