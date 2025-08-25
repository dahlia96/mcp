import httpx

# TODO: replace with actual API call
def get_transaction_status(user_id: str):
    url = f"https://api.example.com/v1/transactions/{user_id}"
    r = httpx.get(url)
    r.raise_for_status()
    return r.json()
