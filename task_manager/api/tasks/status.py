from api.exceptions import InvalidStateTransition

STATUS = str
SUCCESS = True
FAILED = False

PENDING = "pending"
IN_PROGRESS = "in progress"
EMAIL_PENDING = "email pending"
DONE = "done"
FILE_ERROR = "file error"
TRANSACTION_ERROR = "transaction error"
EMAIL_ERROR = "email error"

ALL = [
    PENDING,
    IN_PROGRESS,
    EMAIL_PENDING,
    DONE,
    FILE_ERROR,
    TRANSACTION_ERROR,
    EMAIL_ERROR,
]

TERMINALS = [
    DONE,
    FILE_ERROR,
    TRANSACTION_ERROR,
    EMAIL_ERROR,
]

__TRANSITIONS = {
    PENDING: {
        SUCCESS: IN_PROGRESS,
        FAILED: FILE_ERROR,
    },
    IN_PROGRESS: {
        SUCCESS: EMAIL_PENDING,
        FAILED: TRANSACTION_ERROR,
    },
    EMAIL_PENDING: {
        SUCCESS: DONE,
        FAILED: EMAIL_ERROR,
    },
}


def transition_from(state: STATUS, successful: bool) -> STATUS:
    try:
        return __TRANSITIONS[state][successful]
    except KeyError:
        raise InvalidStateTransition("Unexpected state transition request.")
