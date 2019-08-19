from ..asserts import *
from .fixtures import test_payload
import pytest
import datetime
from ..exceptions import ValidationException

##### assertz #####

def test_assertz_ok(test_payload):

    assert assertz(True, "Error", 0, 500) == None
    assert assertz(test_payload["username"] == "", "Error", 0, 500) == None

def test_assertz_nok(test_payload):

    with pytest.raises(ValidationException):
        assertz(False, "Error", 0, 500)

    with pytest.raises(ValidationException):
        assertz(type(test_payload["application_ids"]) is not list, "Error", 0, 500)

##### assertz_mandatory #####

def test_assertz_mandatory_ok(test_payload):

    assert assertz_mandatory(test_payload, "password") == None
    assert assertz_mandatory(test_payload["application_ids"], 1) == None


def test_assertz_mandatory_nok(test_payload):

    with pytest.raises(ValidationException) as e:
        assertz_mandatory(test_payload, "non_existent_key")
    assert str(e.value) == "Mandatory: non_existent_key"

    with pytest.raises(ValidationException) as e:
        assertz_mandatory(test_payload, "")
    assert str(e.value) == "Key must not be emtpy"

    with pytest.raises(ValidationException) as e:
        assertz_mandatory(test_payload, "username")

    with pytest.raises(ValidationException) as e:
        assertz_mandatory(test_payload["user"], "last_name")
    assert str(e.value) == "Mandatory: last_name"

    with pytest.raises(ValidationException) as e:
        assertz_mandatory({})
    assert str(e.value) == "Mandatory: {}"

    with pytest.raises(ValidationException) as e:
        assertz_mandatory(test_payload, "features")
    assert str(e.value) == "Mandatory: features"

    with pytest.raises(ValidationException) as e:
        null_value = None
        assertz_mandatory(null_value)
    assert str(e.value) == "Mandatory: None"


##### assertz_string #####

def test_assertz_string_ok(test_payload):

    assert assertz_string(test_payload["user"]["name"]) == None
    assert assertz_string(u"random unicode string") == None
    assert assertz_string(None) == None
    assert assertz_string(test_payload, "password") == None

def test_assertz_string_nok(test_payload):

    with pytest.raises(ValidationException) as e:
        assert assertz_string(test_payload, "application_ids", 2000, 400) is not None
    assert str(e.value) == f"Invalid value type: {test_payload['application_ids']}"

    with pytest.raises(ValidationException) as e:
        assert assertz_string(test_payload, "age", 2000) is not None
    assert str(e.value) == f"Invalid value type: {test_payload['age']}"

##### assertz_integer #####

def test_assertz_integer_ok(test_payload):

    assert assertz_integer(test_payload["age"]) == None
    assert assertz_integer(-40000) == None
    assert assertz_integer(None) == None

def test_assertz_integer_nok(test_payload):

    with pytest.raises(ValidationException) as e:
        assert assertz_integer(test_payload["user"], "name", 2000, 400) is not None
    assert str(e.value) == f"Invalid value type: {test_payload['user']['name']}"

    with pytest.raises(ValidationException) as e:
        assert assertz_integer(test_payload, "user", 2001) is not None
    assert str(e.value) == f"Invalid value type: {test_payload['user']}"

##### assertz_float #####

def test_assertz_float_ok(test_payload):

    assert assertz_float(test_payload["value"]) == None
    assert assertz_float(3.14159265359) == None
    assert assertz_float(None) == None


def test_assertz_float_nok(test_payload):

    with pytest.raises(ValidationException) as e:
        assert assertz_float(test_payload["user"], "name", 2000, 400) is not None
    assert str(e.value) == f"Invalid value type: {test_payload['user']['name']}"

    with pytest.raises(ValidationException) as e:
        assert assertz_float(test_payload, "user", 2001) is not None
    assert str(e.value) == f"Invalid value type: {test_payload['user']}"

##### assertz_timestamp #####

def test_assertz_timestamp_ok(test_payload):

    assert assertz_timestamp(test_payload["created"]) == None
    assert assertz_timestamp(datetime.datetime.now()) == None
    assert assertz_timestamp(datetime.date.today()) == None
    assert assertz_timestamp(None) == None


def test_assertz_timestamp_nok(test_payload):

    with pytest.raises(ValidationException) as e:
        assert assertz_timestamp(test_payload["user"], "name", 2000, 400)
    assert str(e.value) == f"Invalid value type: {test_payload['user']['name']}"

    with pytest.raises(ValidationException) as e:
        assert assertz_timestamp(test_payload["user"])
    assert str(e.value) == f"Invalid value type: {test_payload['user']}"

##### assertz_boolean #####

def test_assertz_boolean_ok(test_payload):

    assert assertz_boolean(test_payload["active"]) == None
    assert assertz_boolean(False) == None
    assert assertz_boolean(None) == None


def test_assertz_boolean_nok(test_payload):

    with pytest.raises(ValidationException) as e:
        assertz_boolean(test_payload["user"], "name", 2000, 400)
    assert str(e.value) == f"Invalid value type: {test_payload['user']['name']}"

    with pytest.raises(ValidationException) as e:
        assertz_boolean(test_payload, "user", 2001)
    assert str(e.value) == f"Invalid value type: {test_payload['user']}"


##### assertz_complex #####

def test_assertz_complex_ok(test_payload):

    assert assertz_complex(test_payload, "user") == None
    assert assertz_complex(test_payload["application_ids"]) == None
    assert assertz_complex('{"key": "value", "key1": {"key2": "value"}}') == None
    assert assertz_complex(None) == None


def test_assertz_complex_nok(test_payload):

    with pytest.raises(ValidationException) as e:
        assertz_complex(test_payload["user"], "name", 2000, 400)
    assert str(e.value) == f"Invalid value type: {test_payload['user']['name']}"

    with pytest.raises(ValidationException) as e:
        assertz_complex(test_payload, "created", 2001)
    assert str(e.value) == f"Invalid value type: {test_payload['created']}"

    with pytest.raises(ValidationException) as e:
        assertz_complex('[]')
    assert str(e.value) == "Invalid value type: []"

##### assertz_dict #####

def test_assertz_dict_ok(test_payload):

    assert assertz_dict(test_payload, "user") == None
    assert assertz_dict({"key": "value", "key1": {"key2": "value"}}) == None
    assert assertz_dict(None) == None


def test_assertz_dict_nok(test_payload):

    with pytest.raises(ValidationException) as e:
        assertz_dict(test_payload["user"], "name", 2000, 400)
    assert str(e.value) == f"Invalid value type: {test_payload['user']['name']}"

    with pytest.raises(ValidationException) as e:
        assertz_dict(test_payload, "password", 2001)
    assert str(e.value) == f"Invalid value type: {test_payload['password']}"

    with pytest.raises(ValidationException) as e:
        assertz_dict({})
    assert str(e.value) == "Invalid value type: {}"

##### assertz_json #####

def test_assertz_json_ok(test_payload):

    assert assertz_json(test_payload, "headers") == None
    assert assertz_json('{"key": "value", "key1": {"key2": "value"}}') == None
    assert assertz_json(None) == None


def test_assertz_json_nok(test_payload):

    with pytest.raises(ValidationException) as e:
        assertz_json(test_payload["user"], "name", 2000, 400)
    assert str(e.value) == f"Invalid value type: {test_payload['user']['name']}"

    with pytest.raises(ValidationException) as e:
        assertz_json(test_payload, "features", 2001)
    assert str(e.value) == f"Invalid value type: {test_payload['features']}"

    with pytest.raises(ValidationException) as e:
        assertz_json('{}')
    assert str(e.value) == "Invalid value type: {}"

##### assertz_array #####

def test_assertz_array_ok(test_payload):

    assert assertz_array(test_payload, "application_ids") == None
    assert assertz_array(["a", "b", "c"]) == None
    assert assertz_array(None) == None


def test_assertz_array_nok(test_payload):

    with pytest.raises(ValidationException) as e:
        assertz_array(test_payload["user"], "name", 2000, 400)
    assert str(e.value) == f"Invalid value type: {test_payload['user']['name']}"

    with pytest.raises(ValidationException) as e:
        assertz_array(test_payload, "user", 2001)
    assert str(e.value) == f"Invalid value type: {test_payload['user']}"

    with pytest.raises(ValidationException) as e:
        assertz_array([])
    assert str(e.value) == f"Invalid value type: []"

