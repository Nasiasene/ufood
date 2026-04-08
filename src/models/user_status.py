from enum import Enum


class UserStatus(str, Enum):
    ACTIVE = "active"
    PENDING_DELETION = "pending_deletion"
