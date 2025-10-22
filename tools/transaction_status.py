from pydantic import BaseModel
from typing import Optional, List
from google.cloud import bigquery
import os

# Point to your service account JSON file
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/dahliaradif/.config/gcloud/conversations-api-sandbox.json"

class TransactionStatusInput(BaseModel):
    user_id: str

class TransactionStatusOutput(BaseModel):
    ok: bool
    data: Optional[List[dict]] = None
    error: Optional[str] = None

def get_transaction_status(user_id: str):
    # client = bigquery.Client(project="data-eng-prod-431217")
    # query = """
    # SELECT *
    # FROM `data-eng-prod-431217.int_remittances.near_realtime_remmitances_chat`(@user_id)
    # """
    # job_config = bigquery.QueryJobConfig(
    #     query_parameters=[
    #         bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
    #     ],
    # )

    # try:
    #     job = client.query(query, job_config=job_config)
    #     results = list(job.result())

    # except Exception as e:
    #     print("!!! BigQuery query failed !!!: ", e)
    #     results = []

    # map BigQuery row → dict for proto
    def row_to_receipt_dict(row):
        return {
            "payment_id": str(row.get("payment_id", "")),
            "user_id": str(row.get("user_id", "")),
            "disbursement_id": str(row.get("disbursement_id", "")),
            "amount_charged": str(row.get("amount_charged", "")),
            "exchange_rate": str(row.get("rate", "")),
            "fee": str(row.get("fee", "")),
            "promotion_amount": str(row.get("promotion_amount", "")),
            "beneficiary_delivery_method_id": str(row.get("delivery_method", "")),
            "pickup_place": str(row.get("pickup_place", "")),
            "date": str(row.get("payment_date", "")),
            "payment_created_at": str(row.get("payment_created_at", "")),
            "disbursement_updated_at": str(row.get("disbursement_updated_at", "")),
            "status": str(row.get("final_status_spanish", "")),
            "disbursement_provider": row.get("disbursement_provider", ""),
            "payment_reference_number": str(row.get("payment_reference_number", "")),
            "beneficiary_id": str(row.get("beneficiary_id", "")),
            "recipients_name": str(row.get("recipients_beneficiary_name", "")),
            "beneficiary_full_address": str(row.get("beneficiary_full_address", "")),
            "total_cost": str(row.get("payment_amount", "")),
            "destination_currency": str(row.get("destination_currency", "")),
            "destination_amount": str(row.get("disbursement_amount", "")),
        }

    # formatted_transactions = []
    # # Cap at max of 9 transactions
    # for transaction in results[:9]:
    #     receipt = row_to_receipt_dict(transaction)
    #     formatted_transactions.append(receipt)

    formatted_transactions = [
    {
        "payment_id": "pay_987654321",
        "user_id": "user_12345",
        "disbursement_id": "disb_123456789",
        "amount_charged": "105.00",  # USD charged to sender
        "exchange_rate": "7.80",  # USD → GTQ
        "fee": "4.99",  # transaction fee
        "promotion_amount": "0.00",
        "beneficiary_delivery_method_id": "store_pickup",
        "pickup_place": "Banrural Guatemala - Zona 1",
        "date": "2025-10-08T15:47:22Z",
        "payment_created_at": "2025-10-08T15:45:05Z",
        "disbursement_updated_at": "2025-10-08T15:48:30Z",
        "status": "Entregado",  # Delivered
        "disbursement_provider": "Banrural",
        "payment_reference_number": "REF123456789GT",
        "beneficiary_id": "bene_7777",
        "recipients_name": "Carlos López",
        "beneficiary_full_address": "6a Avenida 12-45, Zona 1, Ciudad de Guatemala",
        "total_cost": "109.99",  # amount + fee
        "destination_currency": "GTQ",
        "destination_amount": "819.00",  # 105 * 7.80
    },
    {
        "payment_id": "pay_111122222",
        "user_id": "user_12345",
        "disbursement_id": "disb_333344444",
        "amount_charged": "233.00", # USD charged to sender
        "exchange_rate": "7.90", # USD → GTQ
        "fee": "4.99", # transaction fee
        "promotion_amount": "0.00",
        "beneficiary_delivery_method_id": "store_pickup",
        "pickup_place": "Banrural Guatemala - Zona 1",
        "date": "2025-10-12T11:13:27Z",
        "payment_created_at": "2025-10-12T12:31:01Z",
        "disbursement_updated_at": "2025-10-12T13:32:20Z",
        "status": "Incompleto",
        "disbursement_provider": "Banrural",
        "payment_reference_number": "REF999999999GT",
        "beneficiary_id": "bene_8888",
        "recipients_name": "Maria López",
        "beneficiary_full_address": "6a Avenida 12-45, Zona 1, Ciudad de Guatemala",
        "total_cost": "237.99", # amount + fee
        "destination_currency": "GTQ",
        "destination_amount": "1840.70",
    }
]

    return formatted_transactions


def get_transaction_status_tool(user_id: str) -> TransactionStatusOutput:
    try:
        data = get_transaction_status(user_id)
        return TransactionStatusOutput(ok=True, data=data)
    except Exception as e:
        return TransactionStatusOutput(ok=False, error=str(e))
