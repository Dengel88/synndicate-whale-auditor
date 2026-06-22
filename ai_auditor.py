import os
import logging
from google import genai
from google.genai import types
from models import AuditResult

logger = logging.getLogger("SyNNdicate-Auditor")

class GeminiAuditor:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is missing.")
        self.client = genai.Client(api_key=self.api_key)

    def audit_contract(self, source_code: str, token_name: str):
        """Sends Solidity code to Gemini 3.1 Pro for a rigorous security audit."""
        
        system_instruction = (
            "You are an elite Smart Contract Security Auditor for the Binance Smart Chain (BSC).\n"
            "Your objective is to analyze the provided Solidity source code and determine if the token is a SCAM or SAFE.\n\n"
            "CRITICAL VULNERABILITIES TO DETECT:\n"
            "1. Honeypot: Can users buy but not sell? (Check transfer/transferFrom logic, custom fees).\n"
            "2. Minting: Can the owner arbitrarily mint new tokens?\n"
            "3. High Tax: Are buy/sell fees hardcoded above 10% or dynamically changeable to 100%?\n"
            "4. Blacklists/Whitelists: Can the owner block arbitrary addresses from trading?\n"
            "5. Hidden Pauses: Can the owner pause trading indefinitely?\n\n"
            "If ANY of the above exist and can be maliciously triggered by the owner, verdict MUST be 'SCAM' with a high risk score.\n"
            "Output strictly conforming to the requested JSON schema."
        )

        user_prompt = f"Token Name: {token_name}\n\nSolidity Source Code:\n{source_code[:60000]}" # Limit size safely

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema=AuditResult,
            temperature=0.1 # Очень низкая температура для строгой логики
        )

        try:
            logger.info(f"Sending contract {token_name} to Gemini 3.1 Pro for audit...")
            response = self.client.models.generate_content(
                model='gemini-3.1-pro',
                contents=user_prompt,
                config=config
            )
            return AuditResult.model_validate_json(response.text)
        except Exception as e:
            logger.error(f"Gemini API Error during audit: {e}")
            return None