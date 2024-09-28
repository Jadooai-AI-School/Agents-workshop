import os
from jinja2 import Template
#####################################################FIX################################################################################
# Defining the Jinja2 template for the system prompt
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
#####################################################FIX################################################################################
class AgentS:
    def __init__(self, llm: any, system_prompt: str = system_prompt_template, tools: dict = {}) -> None:
        """
        Initializes the Agent with an LLM instance and an optional system message.
        :param llm: An instance of the LLM class used to generate responses.
        :param system_prompt: An optional system message to initialize the conversation context.
        """
        self.llm = llm
        self.tools = tools or {}
        self.system = Template(system_prompt).render(tools=self.tools)
        self.messages = [{"role": "system", "content": self.system}]
        
    def __call__(self, message=""):
        """
        Handle incoming user messages and generate a response using the LLM.
        
        :param message: The user's message to be added to the conversation.
        :return: The assistant's response to the user.
        """
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
#####################################################FIX################################################################################
class Agent:
    def __init__(self, llm: any, system_prompt: str = system_prompt_template, tools: dict = {}) -> None:
        """
        Initializes the Agent with an LLM instance and an optional system message.
        :param llm: An instance of the LLM class used to generate responses.
        :param system_prompt: An optional system message to initialize the conversation context.
        """
        self.llm = llm
        self.tools = tools or {}
        self.system = Template(system_prompt).render(tools=self.tools)
        self.messages = [{"role": "system", "content": self.system}]
        
    def __call__(self, message=""):
        """
        Handle incoming user messages and generate a response using the LLM.
        
        :param message: The user's message to be added to the conversation.
        :return: The assistant's response to the user.
        """
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
#####################################################FIX################################################################################
if __name__ == "__main__":
    import os
    os.system('clear')
    # Initialize the LLM
    from aisModels_r1 import GroqLLM
    from aisTools_r1 import calculate, currency_converter, ddg_search, get_news

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
    agent.run("What's are the top 10 the latest news about AI and how much is 100 USD in EUR?")