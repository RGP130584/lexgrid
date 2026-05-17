import pytest
import tempfile
from pathlib import Path
from data_governance.classification.classifier import DataClassifier
from data_governance.classification.sensitivity_levels import SensitivityLevel
from data_governance.integrity.checksum_validator import ChecksumValidator
from data_governance.retention.purge_manager import PurgeManager

def test_data_classifier_secret():
    content = "A senha de produção é lexpassword_secure_2026."
    level = DataClassifier.classify_text(content)
    assert level == SensitivityLevel.SECRET

def test_data_classifier_public():
    content = "Segundo a lei nº 10.406 publicada no diário oficial."
    level = DataClassifier.classify_text(content)
    assert level == SensitivityLevel.PUBLIC

def test_checksum_validation():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"Backup Data Fake")
        filepath = Path(f.name)
        
    try:
        sha256 = ChecksumValidator.generate_sha256(filepath)
        assert ChecksumValidator.verify_integrity(filepath, sha256) is True
    finally:
        filepath.unlink()

def test_secure_delete_missing_file():
    fake_path = Path("/tmp/does_not_exist_ever_lexgrid.txt")
    result = PurgeManager.secure_delete(fake_path)
    assert result is False
