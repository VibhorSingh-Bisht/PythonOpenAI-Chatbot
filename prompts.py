#prompts.py file
from llama_index import PromptTemplate


instruction_str = """\
    1. Convert the query to executable Python code using Pandas.
    2. The final line of code should be a Python expression that can be called with the `eval()` function.
    3. The code should represent a solution to the query.
    4. PRINT ONLY THE EXPRESSION.
    5. Do not quote the expression."""

new_prompt = PromptTemplate(
    """\
    You are conducting research on Canoo Inc., a company operating in the automotive industry.

    Follow these instructions:
    1. Identify the industry in which Canoo operates, along with its size, growth rate, trends, and key players.
    2. Analyze Canoo's main competitors, including their market share, products or services offered, pricing strategies, and marketing efforts.
    3. Identify key trends in the market, including changes in consumer behavior, technological advancements, and shifts in the competitive landscape.
    4. Gather information on Canoo's financial performance, including its revenue, profit margins, return on investment, and expense structure.

    Expression: """
)

context = """Purpose: The primary role of this agent is to assist users by providing accurate 
            information about canoo inc. and about its competitors. """
