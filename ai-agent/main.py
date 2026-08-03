import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_functions import available_functions, call_function
from config import MAX_ITERATIONS


def run_agent(client, model: str, messages: list, verbose: bool = False) -> str | None:
    """Drive the model until it produces a final answer.

    Returns the final response text, or None if the iteration limit was hit
    before the model stopped requesting tool calls.
    """

    for _ in range(MAX_ITERATIONS):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=available_functions,
        )

        if not response:
            raise RuntimeError("No response received from the OpenAI API.")

        if verbose:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")  # type: ignore
            print(f"Response tokens: {response.usage.completion_tokens}")  # type: ignore
            print(f"Model used: {response.model}")

        # the assistant turn, including any tool calls it wants to make
        message = response.choices[0].message
        messages.append(message)

        # no tool calls means the model is done working and has an answer
        if not message.tool_calls:
            return message.content or ""

        # every tool call must be answered before the next assistant turn
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose)
            if not result_message.get("content"):
                raise RuntimeError(f"Function call {tool_call.function.name} returned no content")
            if verbose:
                print(f"-> {result_message['content']}")
            messages.append(result_message)

    return None


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
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": args.user_prompt
        }
    ]

    if args.verbose:
        print(f"User prompt:\n{args.user_prompt}\n")

    final_response = run_agent(client, model, messages, args.verbose)

    if final_response is None:
        print(
            f"Agent stopped: reached the {MAX_ITERATIONS} iteration limit without a final response.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"\nAI response:\n{final_response}")


if __name__ == "__main__":
    main()
