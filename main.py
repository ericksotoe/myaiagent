import sys
import os
from prompts import system_prompt
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from dotenv import load_dotenv


def main():
    load_dotenv()

    # checking if --verbose is provided, if its provided we are removing it from the command to avoid future errors
    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    # if no user input output example
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Missing GEMINI_API_KEY in environment.")
        sys.exit(1)
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    # avail func is a list of functions that the llm can use
    available_functions = types.Tool(function_declarations=[schema_get_files_info,])

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    if response.function_calls:
        for func in response.function_calls:
            print(f"Calling function: {func.name}({func.args})")
    else:
        print("Response:")
        print(response.text)




if __name__ == "__main__":
    main()
