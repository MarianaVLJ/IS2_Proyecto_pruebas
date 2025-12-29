import pytest
from unittest.mock import MagicMock
from backend.app.domain.services.password_service import PasswordService
from backend.app.application.use_cases.register_user import RegisterUserUseCase
from app.domain.users.models.user import User



def test_register_user_success(monkeypatch):
    # Fake repository
    fake_repo = MagicMock()
    fake_repo.find_by_alias.return_value = None  # user does not exist

    # Fake hash function
    monkeypatch.setattr(PasswordService, "hash_password", lambda pwd: "HASHEDPWD")

    # Fake User.create to avoid DB or constraints
    monkeypatch.setattr(User, "create", lambda alias, pwd: User(alias, pwd))

    use_case = RegisterUserUseCase(fake_repo)
    result = use_case.execute("clau", "1234")

    assert result is True
    fake_repo.save.assert_called_once()


def test_register_user_fails_if_alias_exists():
    fake_repo = MagicMock()
    fake_repo.find_by_alias.return_value = User("clau", "oldpass")

    use_case = RegisterUserUseCase(fake_repo)
    result = use_case.execute("clau", "1234")

    assert result is False
    fake_repo.save.assert_not_called()
