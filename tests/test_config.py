import os
import pytest
import tempfile
import yaml


@pytest.fixture
def empty_config_file():
    _, path = tempfile.mkstemp()
    return path


@pytest.fixture
def config_file(empty_config_file):
    config_file = empty_config_file

    with open(config_file, 'wb') as outfile:
        outfile.write(yaml.dump({
            'some': 'value'
        }, default_flow_style=False, encoding='utf-8'))

    return config_file


def test_config_imports_properly():
    from bentham import configObject  # noqa


def test_config_is_dictionary(config_file):
    from bentham import configObject

    # todo - This can probably be a fixture as well
    os.environ.update({
        'BENTHAM_CONFIG': config_file
    })

    assert type(configObject.load()) == dict


def test_config_database_fails_if_no_datastore_specified(empty_config_file):
    from bentham import configObject

    os.environ.update({
        'BENTHAM_CONFIG': empty_config_file
    })

    with pytest.raises(Exception) as e:
        configObject.get_pg_db()

    assert str(e.value) == 'No datastore found in configuration.'


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

    assert str(e.value) == 'No configuration file found.'
