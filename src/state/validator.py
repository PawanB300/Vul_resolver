from pydantic import BaseModel


class ValidationResult(BaseModel):

    success: bool
    vulnerability_id: str
    remaining_findings: int
    message: str
