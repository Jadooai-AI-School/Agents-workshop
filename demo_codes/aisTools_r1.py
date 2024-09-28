
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
x = load_dotenv()
print("Environment variables loaded successfully") if x else print("Error: Failed to load environment variables.")
###################################################################################################################
def calculate(expression: str) -> float:
    """
    Evaluate a mathematical expression and return the result as a float.    
    :param expression: A string representing the mathematical expression to evaluate.
    :return: The result of the evaluation as a float. If an error occurs during evaluation, returns NaN.
    """
    try:
        print('-> TOOL-CALCULATE CALLED')
        return float(eval(expression))
    except Exception as e:
        # Return NaN (Not a Number) in case of an error
        return float('nan')
###################################################################################################################
def get_planet_mass(planet_name: str) -> float:
    """
    Retrieve the mass of a specified planet in kilograms.
    :param planet_name: The name of the planet for which to retrieve the mass. The name is case-insensitive.
    :return: The mass of the specified planet in kilograms as a float. If the planet is not found, returns NaN.
    """
    planet_masses = {
        "mercury": 3.3011e23,
        "venus":   4.8675e24,
        "earth":   5.9723e24,
        "mars":    6.4171e23,
        "jupiter": 1.8982e27,
        "saturn":  5.6834e26,
        "uranus":  8.6810e25,
        "neptune": 1.02413e26
    }
    print('-> TOOL-GET_PLANET_MASS CALLED')
    return planet_masses.get(planet_name.lower(), float('nan'))
###################################################################################################################
import requests
def currency_converter_v4(amount, source_curr, target_curr):
    """
    Converts an amount from a source currency to a target currency.
    :param amount: The amount in the source currency.
    :param source_curr: The source currency code (e.g., 'USD').
    :param target_curr: The target currency code (e.g., 'EUR').
    :return: A formatted string with the converted amount.
    '''Example: currency_converter(100, 'USD', 'EUR')
    '100.00 USD is equivalent to: 80.00 EUR' '''
    """
    # A free API for currency conversion
    url = f"https://api.exchangerate-api.com/v4/latest/{source_curr}"
    
    response = requests.get(url)
    data = response.json()
    
    # Checking if the target currency is available
    if target_curr not in data["rates"]:
        return f"Error: Target currency '{target_curr}' not available in the exchange rates."
    amount = float(amount)
    # Calculating the conversion
    conv = data["rates"][target_curr] * amount

    print('-> TOOL-CURRENCY_CONVERTER CALLED')
    return f'{amount:.2f} {source_curr} is equivalent to: {conv:.2f} {target_curr}'
####################################################################################################################
def currency_converter(amount, from_currency: str, to_currency: str) -> str:
    """
    Convert an amount from one currency to another using real-time exchange rates.
    :param amount: The amount to convert.
    :param from_currency: The currency to convert from.
    :param to_currency: The currency to convert to.
    :return: A string with the converted amount or an error message.
    """
    try:
        #api_key = os.environ.get('EXCHRATE_API_KEY')
        api_key = "a71dffbb1968f78f3cf3e22f"  # will expire on 11th Oct 2024
        
        if not api_key:
            return "Error: API key not found. Set 'EXCHRATE_API_KEY' in environment variables."
        
        amount = float(amount)  # Convert amount to float

        # API URL with from_currency and to_currency
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}"
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()

        # Check for a successful response
        if data.get("result") != "success":
            return f"Error: Failed to retrieve exchange rate. {data.get('error-type', 'Unknown error')}"

        # Access the conversion rate
        rate = data['conversion_rate']
        converted = amount * rate
        
        return f"{amount} {from_currency} is equal to {converted:.2f} {to_currency}"
    
    except ValueError:
        return "Error: Invalid amount. Please provide a numeric value."
    except requests.RequestException as e:
        return f"Error fetching exchange rates: {str(e)}"
####################################################################################################################
import json
from duckduckgo_search import DDGS
from typing import Optional, Any
# Default headers for requests
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# DuckDuckGo search function
def ddg_search(query: str, max_results = "10", headers: Optional[Any] = None, timeout: Optional[int] = 10) -> str:
    """
    Search DuckDuckGo for a query and return the results.

    :param query: The query to search for.
    :param max_results: The maximum number of results to return (default=10).
    :param headers: Optional headers for the request. If not provided, defaults to DEFAULT_HEADERS.
    :param timeout: Optional timeout for the request (default=10 seconds).
    :return: A JSON string containing the search results.
    """
    headers = headers or DEFAULT_HEADERS
    ddgs = DDGS(headers=headers, timeout=timeout)
    results = ddgs.text(keywords=query, max_results=int(max_results)) 
    return json.dumps(results, indent=2)
####################################################################################################################
# DuckDuckGo news function
def get_news(topic: str, max_results = "10") -> str:
    """
    Search DuckDuckGo for the latest news based on a query and return the results.
    :param topic: The query to search for news.
    :param max_results: The maximum number of news results to return (default=10).
    :return: A JSON string containing the news results.
    """
    headers = DEFAULT_HEADERS
    ddgs = DDGS(headers=headers, timeout=60)
    results = ddgs.news(keywords=topic, max_results=int(max_results))
    return json.dumps(results, indent=2)
####################################################################################################################
# Example Usage:
if __name__ == "__main__":
    import os
    #os.system('clear')
    # Example: Search for web results
    search_results = ddg_search("what daye is today in USA?")
    print("Search_results\n",14*'-')
    print(search_results)

    # Example: Search for news
    news_results = get_news("AI breakthroughs")
    print("News_results\n",14*'-')
    print(news_results)
    
    conversion =  currency_converter(100, 'USD', 'EUR')
    print("Conversion:\n",conversion)
    
