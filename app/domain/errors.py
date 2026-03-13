class DomainError(Exception):
    """Base domain error."""


class VMNotFoundError(DomainError):
    """Raised when a VM does not exist."""


class InvalidStateTransitionError(DomainError):
    """Raised when an operation is not valid for VM current state."""
