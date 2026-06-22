from pydantic import BaseModel, Field

class AuditResult(BaseModel):
    """Strict JSON output required from the Gemini AI Auditor."""
    verdict: str = Field(..., description="Must be strictly 'SAFE' or 'SCAM'.")
    risk_score: int = Field(..., description="Risk score from 0 (safest) to 100 (absolute scam).")
    reason: str = Field(..., description="A short, one-sentence explanation of the verdict focusing on contract code evidence.")