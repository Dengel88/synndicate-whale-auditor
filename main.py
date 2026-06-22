import os
import time
import logging
from dotenv import load_dotenv

from bsc_scanner import BscScanner
from ai_auditor import GeminiAuditor
from twak_executor import TwakExecutor

# Профессиональная настройка логов
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("SyNNdicate-Core")

def main():
    load_dotenv()
    whale_address = os.getenv("WHALE_ADDRESS")

    logger.info("🚀 Initializing SyNNdicate Whale-Auditor (BNB Hackathon Track 1)...")
    
    scanner = BscScanner()
    auditor = GeminiAuditor()
    executor = TwakExecutor()

    processed_txs = set()

    logger.info(f"🎯 Sniper locked on Whale: {whale_address}")
    logger.info("⏳ Entering 24/7 monitoring loop. Press Ctrl+C to stop.")

    # ==========================================
    # 🎬 DEMO MODE: FORCE AUDIT FOR SCREENCAST
    # ==========================================
    logger.info("🎬 [DEMO MODE] Forcing audit on known token for screencast presentation...")
    demo_token_address = "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82" # PancakeSwap Token (CAKE)
    demo_token_name = "PancakeSwap Token"
    
    logger.info(f"🚨 SNIPER ALERT: Whale interacted with a new token: {demo_token_name} ({demo_token_address})")
    demo_source = scanner.get_contract_source_code(demo_token_address)
    
    if demo_source:
        logger.info("🔍 AUDITOR: Analyzing Solidity code via Gemini 3.1 Pro...")
        demo_result = auditor.audit_contract(demo_source, demo_token_name)
        if demo_result:
            if demo_result.verdict == "SAFE":
                logger.info(f"✅ VERDICT: SAFE (Risk Score: {demo_result.risk_score}/100)")
                logger.info(f"📝 REASON: {demo_result.reason}")
                executor.execute_buy(demo_token_address, demo_token_name, amount_bnb=0.01)
            else:
                logger.warning(f"☠️ VERDICT: SCAM (Risk Score: {demo_result.risk_score}/100)")
                logger.warning(f"📝 REASON: {demo_result.reason}")
    # ==========================================
    try:
        
        while True:
            # 1. СНАЙПЕР
            transfers = scanner.get_latest_token_transfers(whale_address, limit=5)
            
            for tx in transfers:
                tx_hash = tx.get("hash")
                
                if tx_hash not in processed_txs:
                    token_address = tx.get("contractAddress")
                    token_name = tx.get("tokenName", "Unknown Token")
                    
                    logger.info(f"🚨 SNIPER ALERT: Whale interacted with a new token: {token_name} ({token_address})")
                    processed_txs.add(tx_hash)

                    source_code = scanner.get_contract_source_code(token_address)
                    
                    if not source_code:
                        logger.warning(f"Source code for {token_name} is not verified. Skipping.")
                        continue

                    # 2. ДЕТЕКТИВ
                    logger.info("🔍 AUDITOR: Analyzing Solidity code via Gemini 3.1 Pro...")
                    audit_result = auditor.audit_contract(source_code, token_name)

                    if audit_result:
                        if audit_result.verdict == "SAFE":
                            logger.info(f"✅ VERDICT: SAFE (Risk Score: {audit_result.risk_score}/100)")
                            logger.info(f"📝 REASON: {audit_result.reason}")
                            
                            # 3. ЭКЗЕКУТОР
                            executor.execute_buy(token_address, token_name, amount_bnb=0.01)
                            
                        else:
                            logger.warning(f"☠️ VERDICT: SCAM (Risk Score: {audit_result.risk_score}/100)")
                            logger.warning(f"📝 REASON: {audit_result.reason}")
                            logger.info("🛡️ Action: Skipping purchase. Safely dodged a rugpull.")
                    
            # Пауза 10 секунд, чтобы не отлететь в бан по лимитам BscScan
            time.sleep(10)

    except KeyboardInterrupt:
        logger.info("🛑 System gracefully shut down by user.")

if __name__ == "__main__":
    main()