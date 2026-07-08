import os
from dotenv import load_dotenv, parser
from openai import OpenAI
import argparse

def main():

    # set up LLM client
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable is not set.")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    # set up argparse to accept user prompt from command line
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()




    model = "openrouter/free"
    messages=[
        {
            "role": "user",
            "content": args.user_prompt
        }
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages  # type: ignore
    )

    if not response:
        raise RuntimeError("No response received from the OpenAI API.")

    if(args.verbose):
        print(f"Prompt tokens: {response.usage.prompt_tokens}") # type: ignore
        print(f"Response tokens: {response.usage.completion_tokens}") # type: ignore
        print(f"Model used: {response.model}") # type: ignore
        print(f"\nUser prompt:\n{messages[0]['content']}")
    print(f"\nAI response:\n{response.choices[0].message.content}")

if __name__ == "__main__":
    main()
