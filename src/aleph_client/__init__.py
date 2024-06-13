from importlib.metadata import PackageNotFoundError, distribution

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "aleph-client"
    __version__ = distribution(dist_name).version
except PackageNotFoundError:
    __version__ = "unknown"
finally:
    del distribution, PackageNotFoundError

# Deprecation check
moved_types = ["AlephClient", "AuthenticatedAlephClient", "synchronous", "asynchronous"]


def __getattr__(name):
    if name in moved_types:
        raise ImportError(
            f"The 'aleph_client.{name}' type is deprecated and has been removed from aleph_client. Please use `aleph.sdk.{name}` instead."
        )
