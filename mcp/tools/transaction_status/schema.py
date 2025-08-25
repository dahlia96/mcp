from pydantic import BaseModel


class TransactionStatusInput(BaseModel):
    """Input schema for get_transaction_status."""
    transaction_id: str

class TransactionStatusOutput(BaseModel):
    """Output schema for get_transaction_status."""
    ok: bool
    data: dict | None = None
    error: str | None = None