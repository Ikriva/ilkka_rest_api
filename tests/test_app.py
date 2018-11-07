import os
import tempfile
import pytest
import sys



@pytest.fixture
def client():
    # Importing app root
    sys.path.append('../')
    from app import app

    temp_file_name = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = temp_file_name
    client = app.test_client()

    os.close(tempfile_name)


def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data
