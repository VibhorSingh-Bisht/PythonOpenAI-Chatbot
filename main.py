# main.py
import os
from prompts import new_prompt, instruction_str, context
from note_engine import note_engine
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.agent import ReActAgent
from llama_index.llms import OpenAI
from dotenv import load_dotenv
from pdf import canoo_engine
from note_engine import save_note, response_needs_saving
import scrape

# Loading environment variables from .env file
load_dotenv()

tools = [
    note_engine,
    QueryEngineTool(
        query_engine=canoo_engine,
        metadata=ToolMetadata(
            name="Canoo_PDF_Data",
            description="Provides information about Canoo Inc. from the PDF.",
        ),
    )
]

# Initializing OpenAI language model
llm = OpenAI(model="gpt-3.5-turbo-0613")

# Creating an agent with defined tools and context
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)

def main():
    """
    Entry point for the script.
    """
    # Handling user queries
    while True:
        user_query = input("Enter your question (q to quit): ")
        if user_query.lower() == 'q':
            break
        else:
            # Passing user query to the agent for handling
            response = agent.query(user_query) 
            if response_needs_saving(response):
                save_note(response)
            print("Response:", response)

if __name__ == "__main__":
    main()
