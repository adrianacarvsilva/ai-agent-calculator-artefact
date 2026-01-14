import re

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

from app.tools import calculator


def build_agent():
 
    """Builds an AI agent that can route user queries to either a calculation tool or provide direct answers."""

    # Hugging Face endpoint configuration
    endpoint = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct-v0.2", 
        task="conversational",
        max_new_tokens=256,
        temperature=0
    )

    # Chat LLM with Hugging Face
    llm = ChatHuggingFace(llm=endpoint)

    # Prompt with strict rules for routing responses to calculation tool or direct answer
    prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an intelligent assistant responsible for deciding whether to respond directly "
        "or delegate an exact mathematical calculation to an external tool.\n\n"

        "IMPORTANT RULES:\n"

        "1. If the user question can be answered exclusively by a SINGLE exact mathematical expression "
        "(addition, subtraction, multiplication, division, percentage, etc.), "
        "extract the valid mathematical expression and respond ONLY in the format:\n"
        "CALC: <mathematical_expression>\n\n"

        "2. Do NOT include explanations, additional text, or comments when using the CALC format.\n\n"

        "3. Do NOT attempt to solve the mathematical expression yourself.\n\n"

        "4. NEVER modify the extracted mathematical expression and NEVER change logical operators.\n\n"

        "5. If the question does NOT require a mathematical calculation, respond normally in plain text.\n\n"

        "6. If the question contains MORE THAN ONE INTENT "
        "(for example: a calculation AND general knowledge), "
        "respond ONLY with:\n"
        "REJECT: Please ask only one and valid question at a time.\n\n"

        "7. ALWAYS respond in the SAME LANGUAGE used by the user.\n\n"

        "OUTPUT FORMAT CONTRACT:\n"
        "- CALC: <expression>\n"
        "- TEXT: <text response>\n"
        "- REJECT: Please ask only one and valid question at a time. Details: <rejection message>\n\n"

        "EXAMPLES:\n"
        "User: How much is 2 + 2?\n"
        "Response: CALC: <2+2>\n\n"

        "User: Who was Albert Einstein?\n"
        "Response: TEXT: Albert Einstein was a theoretical physicist...\n\n"

        "User: How much is 1 + 1 and who was Albert Einstein?\n"
        "Response: REJECT: Please ask only one and valid question at a time. Details: <rejection message>\n\n"

        "User: Quanto é 2 + 2?\n"
        "Response: CALC: <2+2>\n\n"

        "User: Quem foi Albert Einstein?\n"
        "Response: TEXT: Albert Einstein foi um físico teórico...\n"
    ),
    ("human", "{input}")
])
    
    def route_response(message):
        raw_content = message.content.strip()

        print("\n*****\nLLM Raw Response:\n", raw_content + "\n******\n")  # log 

        first_line = raw_content.splitlines()[0].strip()

        if "reject" in first_line.strip().lower():
            return first_line.replace("CALC:", "").strip()
        
    
        # Handle calculation requests - only realize calculations in a safe tool
        if first_line.startswith("CALC:"):
            expression = first_line.replace("CALC:", "").strip() 
            expression = expression.replace("<", "")  
            expression = expression.replace(">", "")

             # Remove escape characters
            expression = (
                expression
                .replace("\\*", "*")
                .replace("\\+", "+")
                .replace("\\-", "-")
                .replace("\\/", "/")
            )

            print("Detected calculation expression:", expression)  # log

            match = re.search(r"[0-9+\-*/(). ]+", expression)
            if not match:
                return "Error: No valid mathematical expression found."

            expression = match.group()

            return calculator.run(expression)
        
        if "text:" in first_line.strip().lower():
            print("Detected direct text response.")  # log
            return raw_content.replace("TEXT:", "").strip()

        return raw_content

    chain = (
        prompt
        | llm
        | RunnableLambda(route_response)
    )

    return chain
