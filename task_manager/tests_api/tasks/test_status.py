import api.tasks.status as s
from api.exceptions import InvalidStateTransition
from pytest import raises as pytest_raises


def test_status_types() -> None:
    assert s.STATUS == str
    assert s.SUCCESS
    assert not s.FAILED


def test_all_status() -> None:
    assert len(s.ALL) == 7
    assert s.PENDING in s.ALL
    assert s.IN_PROGRESS in s.ALL
    assert s.EMAIL_PENDING in s.ALL
    assert s.DONE in s.ALL
    assert s.FILE_ERROR in s.ALL
    assert s.TRANSACTION_ERROR in s.ALL
    assert s.EMAIL_ERROR in s.ALL


def test_terminals() -> None:
    assert len(s.TERMINALS) == 4
    assert s.DONE in s.TERMINALS
    assert s.FILE_ERROR in s.TERMINALS
    assert s.TRANSACTION_ERROR in s.TERMINALS
    assert s.EMAIL_ERROR in s.TERMINALS


def test_transitions() -> None:
    assert s.transition_from(s.PENDING, successful=True) == s.IN_PROGRESS
    assert s.transition_from(s.IN_PROGRESS, successful=True) == s.EMAIL_PENDING
    assert s.transition_from(s.EMAIL_PENDING, successful=True) == s.DONE
    assert s.transition_from(s.PENDING, successful=False) == s.FILE_ERROR

    transaction_error: s.STATUS = s.transition_from(
        s.IN_PROGRESS,
        successful=False,
    )
    assert transaction_error == s.TRANSACTION_ERROR
    email_pending: s.STATUS = s.transition_from(
        s.EMAIL_PENDING,
        successful=False,
    )
    assert email_pending == s.EMAIL_ERROR

    for status in s.TERMINALS:
        for result in [s.SUCCESS, s.FAILED]:
            with pytest_raises(InvalidStateTransition) as error:
                s.transition_from(status, successful=result)
            assert "Unexpected state transition request." in str(error.value)
