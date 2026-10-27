
import json

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from toolcreation import get_conversion_factor, convert

load_dotenv()

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)

llm_with_tools = llm.bind_tools([
    get_conversion_factor,
    convert
])


def main():
    print("\n===== Currency Converter =====")

    try:
        # Get input from the user
        amount = float(input("Enter amount: "))
        base_currency = input(
            "Enter source currency (e.g. INR): "
        ).strip().upper()
        target_currency = input(
            "Enter target currency (e.g. USD): "
        ).strip().upper()

        if amount < 0:
            print("Amount cannot be negative.")
            return

        if not base_currency or not target_currency:
            print("Currency codes cannot be empty.")
            return

        print("\nFetching exchange rate...")

        # Ask Gemini to select the exchange-rate tool
        messages = [
            HumanMessage(
                content=(
                    f"Get the exchange rate from {base_currency} "
                    f"to {target_currency} using "
                    "get_conversion_factor."
                )
            )
        ]

        ai_response = llm_with_tools.invoke(messages)

        conversion_rate = None

        # Execute the rate tool if Gemini requests it
        for tool_call in ai_response.tool_calls:
            if tool_call["name"] == "get_conversion_factor":
                rate_result = get_conversion_factor.invoke(
                    tool_call
                )

                rate_data = json.loads(rate_result)
                conversion_rate = float(
                    rate_data["conversion_rate"]
                )
                break

        # Fallback if Gemini doesn't request the tool
        if conversion_rate is None:
            rate_result = get_conversion_factor.invoke({
                "base_currency": base_currency,
                "target_currency": target_currency
            })

            rate_data = json.loads(rate_result)
            conversion_rate = float(
                rate_data["conversion_rate"]
            )

        # Perform the conversion
        converted_amount = float(
            convert.invoke({
                "amount": amount,
                "conversion_rate": conversion_rate
            })
        )

        # Display the result
        print("\n===== Conversion Result =====")
        print(f"Source currency: {base_currency}")
        print(f"Target currency: {target_currency}")
        print(f"Amount: {amount:,.2f} {base_currency}")
        print(f"Exchange rate: {conversion_rate}")
        print(
            f"Converted amount: "
            f"{converted_amount:,.4f} {target_currency}"
        )
        print("=============================")

    except ValueError as error:
        print(f"Invalid input or conversion data: {error}")
    except Exception as error:
        print(f"Something went wrong: {error}")


if __name__ == "__main__":
    main()
