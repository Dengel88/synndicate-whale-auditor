import os
import requests
import logging
from typing import Optional

logger = logging.getLogger("SyNNdicate-Scanner")

class BscScanner:
    def __init__(self):
        self.api_key = os.getenv("BSCSCAN_API_KEY")
        self.base_url = "https://api.bscscan.com/api"

    def get_latest_token_transfers(self, wallet_address: str, limit: int = 5) -> list:
        """Fetches the latest BEP-20 token transfers for a specific whale address."""
        params = {
            "module": "account",
            "action": "tokentx",
            "address": wallet_address,
            "page": 1,
            "offset": limit,
            "sort": "desc",
            "apikey": self.api_key
        }
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            if data.get("status") == "1" and data.get("message") == "OK":
                return data.get("result", [])
            return []
        except Exception as e:
            logger.error(f"Error fetching transactions: {e}")
            return []

    def get_contract_source_code(self, contract_address: str) -> Optional[str]:
        """Pulls the verified Solidity source code of a smart contract."""
        params = {
            "module": "contract",
            "action": "getsourcecode",
            "address": contract_address,
            "apikey": self.api_key
        }
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            if data.get("status") == "1" and data.get("result"):
                source_code = data["result"][0].get("SourceCode", "")
                if source_code:
                    return source_code
            return None
        except Exception as e:
            logger.error(f"Error fetching source code for {contract_address}: {e}")
            return None