import pytest
from unittest.mock import Mock

from backend.app.application.use_cases.create_denuncia import CreateDenunciaUseCase
from app.domain.denuncias.models.denuncia import Denuncia


def test_create_denuncia_success():
    repo_mock = Mock()
    use_case = CreateDenunciaUseCase(repo_mock)

    repo_mock.save.return_value = {"message": "Denuncia almacenada"}

    result, success = use_case.execute(
        categoria="Robo",
        descripcion="Me robaron mi mochila",
        lugar="Centro",
        fecha_hecho="2024-01-01",
        involucrados=["desconocido"],
        evidencia=["foto1.jpg"],
        usuario="juan123"
    )

    assert success is True
    repo_mock.save.assert_called_once()
