from mcp.registry import register_tool
from mcp.tools.transaction_status.schema import TransactionStatusInput, TransactionStatusOutput
from mcp.tools.transaction_status.service import get_transaction_status


@register_tool(
    name="get_transaction_status@v1",
    description="Fetch the status of a transaction by its ID.",
    input_schema=TransactionStatusInput,
    output_schema=TransactionStatusOutput,
)

def get_transaction_status_tool(args: TransactionStatusInput) -> TransactionStatusOutput:
    try:
        data = get_transaction_status(args.transaction_id)
        return TransactionStatusOutput(ok=True, data=data)
    except Exception as e:
        return TransactionStatusOutput(ok=False, error=str(e))
