
import os
import json
import requests

from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()


@tool
def get_conversion_factor(
    base_currency: str,
    target_currency: str
) -> str:
    """Get the latest conversion rate between two currencies.
    
    Args:
        base_currency: Source currency code, e.g. INR.
        target_currency: Target currency code, e.g. USD.
    """
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")

    if not api_key:
        raise ValueError(
            "EXCHANGE_RATE_API_KEY is missing from .env"
        )

    url = (
        f"https://v6.exchangerate-api.com/v6/{api_key}"
        f"/pair/{base_currency.upper()}/{target_currency.upper()}"
    )

    response = requests.get(url, timeout=15)
    response.raise_for_status()

    data = response.json()

    if data.get("result") != "success":
        raise ValueError(f"ExchangeRate-API error: {data}")

    # Always return valid JSON text
    return json.dumps(data)


@tool
def convert(amount: float, conversion_rate: float) -> str:
    """Convert an amount using the provided exchange rate.
    
    Args:
        amount: Amount in the source currency.
        conversion_rate: Exchange rate from source to target.
    """
    if amount < 0:
        raise ValueError("Amount cannot be negative.")

    converted_amount = amount * conversion_rate

    return f"{converted_amount:.4f}"
