"""Provides the class Systembolaget."""
import json
import sys
from http.client import HTTPException
from typing import List

import requests


class Systembolaget:
    """Handles loading of products from Systembolaget."""

    API_ENDPOINT = 'https://api-extern.systembolaget.se/product/v1/product'

    def __init__(
            self,
            api_key: str,
    ):
        self.headers = {
            'Ocp-Apim-Subscription-Key': api_key,
        }

    def get_products(self) -> List[bytes]:
        """Return JSON strings of all products from Systembolaget."""
        data: List[bytes] = []

        try:
            response = requests.get(
                self.API_ENDPOINT,
                headers=self.headers
            )
            data = [json.dumps(product).encode('utf-8')
                    for product in
                    json.loads(response.content.decode('utf-8'))]
            response.close()
        except HTTPException as err:
            print(err, file=sys.stderr)

        return data
