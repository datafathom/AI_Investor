
import unittest
import os
import json
import uuid
from services.portfolio.assets_service import AssetsService
from web.app import create_app

class TestAssetsBackend(unittest.TestCase):
    def setUp(self):
        # Use a temporary file for testing
        self.test_data_file = 'data/test_assets.json'
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)
        
        self.service = AssetsService(data_file=self.test_data_file)
        
        # Setup Flask test client
        self.app, _ = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def tearDown(self):
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)

    def test_service_add_get_asset(self):
        asset_data = {
            'name': 'Test Mansion',
            'category': 'Real Estate',
            'value': 1000000.0,
            'location': 'Beverly Hills'
        }
        new_asset = self.service.add_asset(asset_data)
        self.assertIn('id', new_asset)
        self.assertEqual(new_asset['name'], 'Test Mansion')
        
        assets = self.service.get_all_assets()
        self.assertEqual(len(assets), 1)
        self.assertEqual(assets[0]['name'], 'Test Mansion')

    def test_service_update_delete_asset(self):
        new_asset = self.service.add_asset({'name': 'Old Name', 'value': 100})
        asset_id = new_asset['id']
        
        updated = self.service.update_asset(asset_id, {'name': 'New Name', 'value': 200})
        self.assertEqual(updated['name'], 'New Name')
        self.assertEqual(updated['value'], 200.0)
        
        success = self.service.delete_asset(asset_id)
        self.assertTrue(success)
        self.assertEqual(len(self.service.get_all_assets()), 0)

    def test_api_endpoints(self):
        # Create
        response = self.client.post('/api/v1/assets/', json={
            'name': 'API Asset',
            'category': 'Art',
            'value': 50000
        })
        self.assertEqual(response.status_code, 201)
        asset = response.get_json()
        asset_id = asset['id']
        
        # Get List
        response = self.client.get('/api/v1/assets/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.get_json()), 1)
        
        # Update
        response = self.client.put(f'/api/v1/assets/{asset_id}', json={'value': 55000})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['value'], 55000.0)
        
        # Delete
        response = self.client.delete(f'/api/v1/assets/{asset_id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
