import pbr.version

# Setup version
VERSION = pbr.version.VersionInfo('pypillar')
try:
    __version__ = VERSION.version_string()
    __release__ = VERSION.release_string()
except (ValueError, AttributeError):
    __version__ = None
__release__ = None
