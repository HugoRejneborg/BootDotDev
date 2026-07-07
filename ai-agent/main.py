import os
from dotenv import load_dotenv
from openai import OpenAI

def main():

    print("\nHello from ai-agent\n")

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable is not set.")
    else:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

    model = "openrouter/free"
    messages=[
        {
            "role": "user",
            "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
        }
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages  # type: ignore
    )

    print(response.choices[0].message.content)

    print("\nGoodbye from ai-agent\n")

if __name__ == "__main__":
    main()
