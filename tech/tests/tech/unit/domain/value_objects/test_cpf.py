# tests/unit/domain/value_objects/test_cpf.py
import pytest
from tech.domain.value_objects import CPF


class TestCPF:
    """Unit tests for the CPF value object."""

    def test_cpf_initialization(self):
        """Test that a CPF with 11 numeric digits can be initialized."""
        # Valid CPF with 11 digits
        cpf = CPF("12345678901")
        assert cpf.value == "12345678901"
        assert str(cpf) == "12345678901"

    def test_invalid_cpf_format_raises_error(self):
        """Test that invalid CPF formats raise ValueError."""
        # CPF with non-numeric characters
        with pytest.raises(ValueError) as exc_info:
            CPF("123.456.789-01")
        assert "CPF must contain exactly 11 digits and be numeric" in str(exc_info.value)

        # CPF that's too short
        with pytest.raises(ValueError):
            CPF("1234567890")  # 10 digits

        # CPF that's too long
        with pytest.raises(ValueError):
            CPF("123456789012")  # 12 digits

        # CPF with letters
        with pytest.raises(ValueError):
            CPF("abcdefghijk")

    def test_cpf_string_representation(self):
        """Test string representation of CPF."""
        cpf = CPF("12345678901")
        assert str(cpf) == "12345678901"

    def test_cpf_repr_representation(self):
        """Test repr representation of CPF."""
        cpf = CPF("12345678901")
        assert repr(cpf).startswith("<tech.domain.value_objects.CPF object at")

    def test_cpf_direct_value_access(self):
        """Test that CPF value can be accessed directly."""
        cpf = CPF("12345678901")
        assert cpf.value == "12345678901"

    def test_cpf_value_is_stored_as_string(self):
        """Test that CPF value is stored as a string."""
        cpf = CPF("12345678901")
        assert isinstance(cpf.value, str)