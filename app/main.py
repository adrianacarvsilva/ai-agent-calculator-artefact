from app.agent import build_agent
from dotenv import load_dotenv

load_dotenv()

def main():
    agent = build_agent()

    print("Welcome to the AI Agent!")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        try:
            response = agent.invoke(user_input)
            print(f"Response: {response}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")   

if __name__ == "__main__":
    main()