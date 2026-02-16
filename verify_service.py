import os
import sys
import django
from django.conf import settings
from unittest.mock import MagicMock, patch

# Setup Django minimal settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CodeVenture.settings")
django.setup()

from CodeVenture.services.judge0_service import Judge0Service

def test_judge0_service():
    print("Testing Judge0Service...")

    with patch('requests.post') as mock_post, patch('requests.get') as mock_get:
        # Mock POST response
        mock_post.return_value.json.return_value = {'token': 'test_token'}
        mock_post.return_value.status_code = 201

        # Mock GET response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'status_id': 3,
            'stdout': 'SGVsbG8gV29ybGQ=', # Hello World
            'status': {'description': 'Accepted'},
            'time': '0.01',
            'memory': '1024'
        }

        service = Judge0Service()
        result = service.run_code("print('Hello World')")

        print("Result:", result)

        if result.get('success') and result.get('stdout') == 'Hello World':
            print("SUCCESS: Service Logic Verified")
        else:
            print("FAILURE: Service Logic Failed")

if __name__ == "__main__":
    test_judge0_service()
