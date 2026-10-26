from langchain_core.tools import tool
import requests


# Tool for conversion 

@tool
def get_conversion_factor(base_currency : str, target_currency : str) -> float:

    """
    This Function fetches the currency conversion between a given base_currency  and the target_currency
    """

    url = f"https://v6.exchangerate-api.com/v6/294829fc75e1f80a13ccd7e6/pair/{base_currency}/{target_currency}"

    response = requests.get(url)

    return response.json()



response = get_conversion_factor.invoke({"base_currency": "USD","target_currency" :"INR"})


# Tool for Multiplying

@tool
def convert(base_currency_value : int, conversion_rate : float)-> float:

    """
    given a currency conversion rate this function calculates the target currency value from a given base currency value
    """

    return base_currency_value*conversion_rate


conversion_response = convert.invoke({"base_currency_value": 10, "conversion_rate" : 85})

print(conversion_response)