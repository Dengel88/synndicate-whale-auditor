# 🐋 SyNNdicate Whale-Auditor
**An Autonomous On-Chain Security & Trading Agent powered by Gemini 3.1 Pro and Trust Wallet Agent Kit (TWAK).**

Built for the **BNB Chain Hackathon (Track 1)**.

SyNNdicate is a highly performant, serverless-ready Python backend designed to track Smart Money ("Whales") on the Binance Smart Chain (BSC). Instead of blindly copy-trading, SyNNdicate introduces a rigorous **AI-Auditor layer**, ensuring that every copied trade is safe from honeypots, malicious minting, and hidden taxes.

## 🧠 Agent Architecture

The system is composed of 3 core modules operating in a continuous 24/7 pipeline:

### 1. 🎯 The Sniper (Data Ingestion)
- Continuously polls the BscScan API for specific Whale wallet addresses.
- Triggers instantly when the target interacts with a new, unknown BEP-20 token contract.
- Automatically fetches the verified Solidity Source Code of the target token.

### 2. 🔍 The Security-Auditor (Gemini 3.1 Pro Core)
- The raw Solidity source code is injected into the **Gemini 3.1 Pro** API via the official `google-genai` SDK.
- The model operates under strict system prompts at `temperature=0.1` to perform a deterministic security audit.
- **Vulnerabilities checked:** Honeypots (transfer restrictions), arbitrary minting, dynamic high-tax modifications, and blacklist/whitelist abuse.
- Outputs a strict, validated **JSON schema (Pydantic)** defining the `verdict` (SAFE/SCAM), `risk_score`, and `reason`.

### 3. ⚡ The Executor (Trust Wallet Agent Kit)
- If the AI Auditor returns a "SAFE" verdict, the Executor module kicks in.
- Integrates with the **Trust Wallet Agent Kit (TWAK)** via Web3.py to build, sign (non-custodial), and broadcast the buy transaction directly to the BSC Mainnet.

## 🛠️ Tech Stack
- **AI Engine:** Google Gemini 3.1 Pro (via `google-genai`)
- **Blockchain:** Web3.py, Trust Wallet Agent Kit (TWAK), Binance Smart Chain Mainnet
- **Data Provider:** BscScan API V2
- **Backend:** Python 3.10+, Pydantic, python-dotenv

## 🚀 How to Run Locally

1. Clone the repository:
```bash
git clone https://github.com/your-username/synndicate-whale.git
cd synndicate-whale