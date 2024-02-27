# main.py
import os
import pandas as pd
from prompts import new_prompt, instruction_str, context
from note_engine import note_engine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.query_engine import PandasQueryEngine
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
from pdf import canoo_engine
from note_engine import save_note, response_needs_saving
import scrape_selenium

# Loading environment variables from .env file
load_dotenv()

def main():
    """
    Entry point for the script.
    """
    scrape_selenium.main()
    canoo_data = os.path.join("data", "canoo.csv")
    canoo_df = pd.read_csv(canoo_data)

    canoo_query_engine = PandasQueryEngine(
        df=canoo_df, verbose=True, instruction_str=instruction_str
    )
    canoo_query_engine.update_prompts({"pandas_prompt": new_prompt})

    
    tools = [
        note_engine,
        QueryEngineTool(
        query_engine=canoo_query_engine,
        metadata=ToolMetadata(
            name="canoo_data",
            description="this gives information of canoo stocks",
            )
        ),
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
