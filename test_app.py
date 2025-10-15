import unittest
import json
import os
from app import app


class TestGuardarEndpoint(unittest.TestCase):
    def setUp(self):
        """Set up test client and remove test file if exists"""
        self.app = app.test_client()
        self.app.testing = True
        self.test_file = 'datos_personales.json'
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def tearDown(self):
        """Clean up test file after each test"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_guardar_single_person(self):
        """Test saving a single person's data"""
        datos = {
            'nombre': 'Juan',
            'apellidos': 'Pérez',
            'email': 'juan@example.com',
            'direccion': 'Calle 123',
            'fecha_nacimiento': '1990-01-01'
        }
        
        response = self.app.post('/guardar',
                                data=json.dumps(datos),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('mensaje', json.loads(response.data))
        
        # Verify file was created and contains data
        self.assertTrue(os.path.exists(self.test_file))
        with open(self.test_file, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
            self.assertIsInstance(saved_data, list)
            self.assertEqual(len(saved_data), 1)
            self.assertEqual(saved_data[0]['nombre'], 'Juan')
    
    def test_guardar_multiple_people(self):
        """Test saving multiple people's data (append functionality)"""
        datos1 = {
            'nombre': 'Juan',
            'apellidos': 'Pérez',
            'email': 'juan@example.com',
            'direccion': 'Calle 123',
            'fecha_nacimiento': '1990-01-01'
        }
        
        datos2 = {
            'nombre': 'María',
            'apellidos': 'García',
            'email': 'maria@example.com',
            'direccion': 'Avenida 456',
            'fecha_nacimiento': '1995-05-15'
        }
        
        datos3 = {
            'nombre': 'Carlos',
            'apellidos': 'López',
            'email': 'carlos@example.com',
            'direccion': 'Plaza 789',
            'fecha_nacimiento': '1988-12-20'
        }
        
        # Save first person
        response1 = self.app.post('/guardar',
                                 data=json.dumps(datos1),
                                 content_type='application/json')
        self.assertEqual(response1.status_code, 200)
        
        # Save second person
        response2 = self.app.post('/guardar',
                                 data=json.dumps(datos2),
                                 content_type='application/json')
        self.assertEqual(response2.status_code, 200)
        
        # Save third person
        response3 = self.app.post('/guardar',
                                 data=json.dumps(datos3),
                                 content_type='application/json')
        self.assertEqual(response3.status_code, 200)
        
        # Verify all three people are in the file
        with open(self.test_file, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
            self.assertIsInstance(saved_data, list)
            self.assertEqual(len(saved_data), 3)
            self.assertEqual(saved_data[0]['nombre'], 'Juan')
            self.assertEqual(saved_data[1]['nombre'], 'María')
            self.assertEqual(saved_data[2]['nombre'], 'Carlos')
    
    def test_guardar_no_data(self):
        """Test error handling when no data is provided"""
        response = self.app.post('/guardar',
                                data=json.dumps(None),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', json.loads(response.data))


if __name__ == '__main__':
    unittest.main()
