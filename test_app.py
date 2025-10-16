import pytest
import json
import os
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def cleanup_json():
    """Clean up the datos_personales.json file after tests."""
    yield
    if os.path.exists('datos_personales.json'):
        os.remove('datos_personales.json')


def test_guardar_multiple_nombres_no_sobrescribe(client, cleanup_json):
    """Test that multiple POST requests to /guardar accumulate data instead of overwriting."""
    # First POST
    response1 = client.post('/guardar', 
                            json={'nombre': 'Ana'},
                            content_type='application/json')
    assert response1.status_code == 200
    assert response1.json['mensaje'] == 'Datos guardados correctamente'
    
    # Second POST
    response2 = client.post('/guardar',
                            json={'nombre': 'Luis'},
                            content_type='application/json')
    assert response2.status_code == 200
    assert response2.json['mensaje'] == 'Datos guardados correctamente'
    
    # Verify that both names are in the file
    with open('datos_personales.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # The data should be a list containing both entries
    assert isinstance(data, list), "Data should be a list"
    assert len(data) == 2, "Should have 2 entries"
    assert data[0]['nombre'] == 'Ana'
    assert data[1]['nombre'] == 'Luis'


def test_guardar_empty_file_initializes_list(client, cleanup_json):
    """Test that the first POST creates a list with one entry."""
    response = client.post('/guardar',
                          json={'nombre': 'Pedro'},
                          content_type='application/json')
    assert response.status_code == 200
    
    with open('datos_personales.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    assert isinstance(data, list), "Data should be a list"
    assert len(data) == 1, "Should have 1 entry"
    assert data[0]['nombre'] == 'Pedro'


def test_guardar_full_form_data(client, cleanup_json):
    """Test saving complete form data."""
    datos1 = {
        'nombre': 'María',
        'apellidos': 'García',
        'email': 'maria@example.com',
        'direccion': 'Calle Principal 123',
        'fecha_nacimiento': '1990-05-15'
    }
    
    datos2 = {
        'nombre': 'Juan',
        'apellidos': 'Pérez',
        'email': 'juan@example.com',
        'direccion': 'Avenida Central 456',
        'fecha_nacimiento': '1985-10-20'
    }
    
    response1 = client.post('/guardar', json=datos1, content_type='application/json')
    assert response1.status_code == 200
    
    response2 = client.post('/guardar', json=datos2, content_type='application/json')
    assert response2.status_code == 200
    
    with open('datos_personales.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    assert len(data) == 2
    assert data[0] == datos1
    assert data[1] == datos2


def test_guardar_no_data(client, cleanup_json):
    """Test that sending no data returns an error."""
    response = client.post('/guardar', content_type='application/json')
    assert response.status_code == 400
    # When no JSON is sent, Flask returns HTML error page, not JSON
