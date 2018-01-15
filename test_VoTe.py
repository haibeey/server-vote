import os
import json
import tempfile
import pytest
from model import db
import VoTe as app


@pytest.fixture
def client():
    db_fd, app.vote.config['DATABASE'] = tempfile.mkstemp()
    
    app.vote.config['TESTING'] = True
    
    client = app.vote.test_client()
   
    yield client
    os.close(db_fd)
    os.unlink(app.vote.config['DATABASE'])
    
def test_register(client):

    temp=client.post("/signup",data=dict(
            firstname="firstname",
            lastname="lastname",
            email="a@mabgdsd.com",
            password="password"
        )
    )
    
    
    assert "response" in temp.data

def test_home(client):
    response=client.get("/?category=1")
    assert "response" in response.data and "ok" in response.data
    assert "topics" in response.data and "users" in response.data
