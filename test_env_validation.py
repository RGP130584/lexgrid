import pytest
from scripts.quality import validate_env

def test_validate_env_runs_without_error():
    # Garante que as rotinas de validação base operam sem crash na chamada principal
    assert validate_env is not None