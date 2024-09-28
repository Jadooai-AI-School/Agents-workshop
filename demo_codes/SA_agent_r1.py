import os
from dotenv import load_dotenv
from jinja2 import Template
from bs4 import BeautifulSoup
import requests
from groq import Groq

# Load environment variables
load_dotenv()
x = load_dotenv()
print(x)

class GroqLLM:
    def __init__(self, api_key="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", model="llama3-70b-8192"):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided either as an argument or through the 'GROQ_API_KEY' environment variable.")
        self.client = Groq(api_key=self.api_key)
        self.model = model

    def generate_response(self, messages):
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
            
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return completion.choices[0].message.content

def ddg_search(query: str) -> str:
    """
    Perform a search using DuckDuckGo and return the top result.
    :param query: The search query to perform.
    :return: A string containing the result or an error message.
    """
    url = "https://api.duckduckgo.com"
    params = {
        "q": query,
        "format": "json",
        "pretty": 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if "AbstractText" in data and data["AbstractText"]:
        return f"Result: {data['AbstractText']}"
    elif "RelatedTopics" in data and len(data["RelatedTopics"]) > 0:
        return f"Top result: {data['RelatedTopics'][0]['Text']}"
    else:
        return "No relevant results found."
    
def currency_converter0(amount: str, from_currency: str, to_currency: str) -> str:
    """
    Convert an amount from one currency to another using real-time exchange rates.
    :param amount: The amount to convert (as a string).
    :param from_currency: The currency to convert from.
    :param to_currency: The currency to convert to.
    :return: A string with the converted amount or an error message.
    """
    try:
        amount = float(amount)
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if to_currency not in data["rates"]:
            return f"Error: Currency '{to_currency}' not available."
        
        rate = data["rates"][to_currency]
        converted = amount * rate
        return f"{amount} {from_currency} is equal to {converted:.2f} {to_currency}"
    except ValueError:
        return "Error: Invalid amount. Please provide a numeric value."
    except requests.RequestException as e:
        return f"Error fetching exchange rates: {str(e)}"

    
def currency_converter(amount: str, from_currency: str, to_currency: str) -> str:
    """
    Convert an amount from one currency to another using real-time exchange rates.
    :param amount: The amount to convert (as a string).
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



def get_news(topic: str) -> str:
    """
    Get the latest news on a specific topic using DuckDuckGo.
    :param topic: The topic to search for news.
    :return: A string containing the latest news or an error message.
    """
    url = f"https://duckduckgo.com/html/?q={topic}+news"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = soup.find_all('div', class_='result__body')
        if results:
            top_result = results[0]
            title = top_result.find('h2', class_='result__title').text.strip()
            snippet = top_result.find('a', class_='result__snippet').text.strip()
            return f"Latest news on {topic}: {title} - {snippet}"
        else:
            return f"No recent news found on the topic: {topic}"
    except requests.RequestException as e:
        return f"Error fetching news: {str(e)}"


# Define the system prompt template
system_prompt_template = """
You are an intelligent agent capable of answering questions and performing tasks using the following tools:

{% for tool_name, tool_func in tools.items() %}
{{ tool_name }}:
Usage: {{ tool_func.__doc__.strip() }}

{% endfor %}

Respond in this format:
Thought: Your reasoning about the task
Action: tool_name: arguments
PAUSE

After receiving an observation, continue with:
Thought: Your interpretation of the observation
Action: Next action or "Answer" if you have the final response

Answer: Your final response to the user's query

Begin!
"""

class Agent:
    def __init__(self, llm, system_prompt=system_prompt_template, tools=None):
        self.llm = llm
        self.tools = tools or {}
        self.system = Template(system_prompt).render(tools=self.tools)
        self.messages = [{"role": "system", "content": self.system}]

    def __call__(self, message=""):
        if message:
            self.messages.append({"role": "user", "content": message})
        result = self.llm.generate_response(self.messages)
        self.messages.append({"role": "assistant", "content": result})
        return result

    def run(self, query, max_iterations=10):
        print(f"User: {query}")
        next_prompt = query
        
        for i in range(max_iterations):
            result = self(next_prompt)
            print(f"Agent: {result}")
            
            if "Action" in result and "PAUSE" in result:
                action_parts = result.split("Action:", 1)[1].split("PAUSE", 1)[0].strip().split(":", 1)
                if len(action_parts) == 2:
                    action, args = action_parts
                    action = action.strip()
                    args = [arg.strip() for arg in args.split(",")]
                    
                    if action in self.tools:
                        try:
                            tool_result = self.tools[action](*args)
                            next_prompt = f"Observation: {tool_result}"
                            print(f"Tool ({action}): {next_prompt}")
                        except Exception as e:
                            next_prompt = f"Observation: Error occurred while executing {action}: {str(e)}"
                            print(next_prompt)
                    else:
                        next_prompt = f"Observation: Tool '{action}' not found"
                        print(next_prompt)
                else:
                    next_prompt = "Observation: Invalid action format"
                    print(next_prompt)
            elif "Answer:" in result:
                break
            else:
                break

        print("Agent run completed.")

if __name__ == "__main__":
    # Initialize the LLM
    llm = GroqLLM()

    # Define tools
    tools = {
        "ddg_search": ddg_search,
        "currency_converter": currency_converter,
        "get_news": get_news
    }

    # Create an agent instance
    agent = Agent(llm, tools=tools)

    # Start the agent's interaction
    agent.run("What's the latest news about AI and how much is 100 USD in EUR?")