import requests
import time
import base64
import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class Judge0Service:
    """
    Service for interacting with the Judge0 API to execute code.
    """
    SUCCESS = 3
    WRONG_ANSWER = 4
    RUN_TIME_ERROR = 11

    def __init__(self):
        self.api_key = getattr(settings, 'RAPIDAPI_KEY', '')
        self.api_host = getattr(settings, 'RAPIDAPI_HOST', 'judge0-ce.p.rapidapi.com')
        self.base_url = f"https://{self.api_host}"

        if not self.api_key:
            logger.warning("RAPIDAPI_KEY is not set in settings.")

    def _get_headers(self):
        return {
            "content-type": "application/json",
            "Content-Type": "application/json",
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.api_host
        }

    def run_code(self, source_code, language_id=71, stdin=None, expected_output=None, timeout=10):
        """
        Submits code to Judge0 and polls for the result.

        Args:
            source_code (str): The source code to execute.
            language_id (int): language ID (default 71 for Python 3.8.1).
            stdin (str): Standard input for the program.
            expected_output (str): Expected output for verification.
            timeout (int): Max time to wait for execution in seconds.

        Returns:
            dict: The result from Judge0 or error information.
        """
        # Encode inputs
        encoded_code = base64.b64encode(source_code.encode('utf-8')).decode('utf-8')

        payload = {
            "language_id": language_id,
            "source_code": encoded_code,
            "redirect_stderr_to_stdout": True
        }

        if stdin:
            # Check if stdin is already base64 encoded or needs encoding
            # For safety, we assume it's raw string if passing to this service method
            # unless it looks like valid base64, but simplest is to just require raw string input
            payload["stdin"] = base64.b64encode(stdin.encode('utf-8')).decode('utf-8')

        if expected_output:
            payload["expected_output"] = base64.b64encode(expected_output.encode('utf-8')).decode('utf-8')

        querystring = {"base64_encoded": "true", "wait": "false", "fields": "*"}
        url = f"{self.base_url}/submissions"

        try:
            response = requests.post(
                url,
                json=payload,
                headers=self._get_headers(),
                params=querystring,
                timeout=10
            )
            response.raise_for_status()

            token = response.json().get('token')
            if not token:
                return {'error': 'Failed to retrieve submission token.'}

            return self._poll_result(token, timeout)

        except requests.RequestException as e:
            logger.error(f"Judge0 API connection error: {e}")
            return {'error': f'Error communicating with execution service: {str(e)}'}
        except Exception as e:
            logger.error(f"Judge0 execution error: {e}")
            return {'error': f'An unexpected error occurred: {str(e)}'}

    def _poll_result(self, token, timeout):
        """Polls the submission URL until completion or timeout."""
        url = f"{self.base_url}/submissions/{token}"
        querystring = {"base64_encoded": "true", "fields": "*"}
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                response = requests.get(
                    url,
                    headers=self._get_headers(),
                    params=querystring,
                    timeout=5
                )

                if response.status_code != 200:
                    time.sleep(0.5)
                    continue

                data = response.json()
                status_id = data.get('status_id')

                # status_id < 3 means In Queue or Processing
                if status_id is not None and status_id >= 3:
                    return self._process_response(data)

                time.sleep(0.5)
            except requests.RequestException:
                time.sleep(0.5)

        return {'error': 'Execution timed out.'}

    def _process_response(self, data):
        """Decodes and formats the Judge0 response."""
        status_id = data.get('status_id')
        stdout_encoded = data.get('stdout', '')
        decoded_output = ""

        if stdout_encoded:
            try:
                decoded_output = base64.b64decode(stdout_encoded).decode('utf-8', errors='replace')
            except Exception:
                decoded_output = "Error decoding output."

        result = {
            'status_id': status_id,
            'stdout': decoded_output,
            'description': data.get('status', {}).get('description', 'Unknown'),
            'time': data.get('time'),
            'memory': data.get('memory'),
        }

        if status_id == self.SUCCESS:
            result['success'] = True
        else:
            result['success'] = False
            # Try to get extra info errors
            stderr_encoded = data.get('stderr', '')
            compile_output_encoded = data.get('compile_output', '')

            if stderr_encoded:
                result['error_message'] = base64.b64decode(stderr_encoded).decode('utf-8', errors='replace')
            elif compile_output_encoded:
                result['error_message'] = base64.b64decode(compile_output_encoded).decode('utf-8', errors='replace')

            # Handle expected output mismatch info
            if status_id == self.WRONG_ANSWER:
                 expected_out_b64 = data.get('expected_output', '')
                 if expected_out_b64:
                     result['expected_output'] = base64.b64decode(expected_out_b64).decode('utf-8', errors='replace')

        return result
