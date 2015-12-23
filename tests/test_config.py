import os
import pytest
import tempfile

@pytest.fixture
def empty_config_file():
    _, path = tempfile.mkstemp()
    return path

def test_config_imports_properly():
    from bentham import configObject

def test_config_is_dictionary():
    from bentham import configObject

    assert type(configObject.load()) == dict

def test_config_database_fails_if_no_datastore_specified(empty_config_file):
    from bentham import configObject

    os.environ.update({
        'BENTHAM_CONFIG': empty_config_file
    })

    with pytest.raises(Exception) as e:
        configObject.get_pg_db()

    assert e.value.message == 'No datastore found in configuration.'

def test_config_raises_exception_if_no_configuration_file(monkeypatch):
    """
    This monkey patches os.path.exists to always return False so we can
    assert config_file will raise an exception if it thinks there is no
    existing configuration file.
    """
    from bentham import configObject
    monkeypatch.setattr(os.path, 'exists', lambda x: False)

    with pytest.raises(Exception) as e:
        configObject.config_file()

    assert e.value.message == 'No configuration file found.'
