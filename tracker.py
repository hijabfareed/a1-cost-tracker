
import os
import json
import time
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types
from groq import Groq


# 1. LOAD ENVIRONMENT VARIABLES

load_dotenv()


# 2. MODEL CONFIGURATION

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite"
)

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)

print("Gemini model configured:", GEMINI_MODEL)
print("Gemini API key loaded:", bool(os.getenv("GEMINI_API_KEY")))

print("Groq model configured:", GROQ_MODEL)
print("Groq API key loaded:", bool(os.getenv("GROQ_API_KEY")))


# 3. MODEL PRICING PER 1 MILLION TOKENS (USD)

GEMINI_INPUT_PRICE = float(
    os.getenv("GEMINI_INPUT_PRICE", "0.30")
)

GEMINI_OUTPUT_PRICE = float(
    os.getenv("GEMINI_OUTPUT_PRICE", "2.50")
)

GROQ_INPUT_PRICE = float(
    os.getenv("GROQ_INPUT_PRICE", "0.075")
)

GROQ_OUTPUT_PRICE = float(
    os.getenv("GROQ_OUTPUT_PRICE", "0.30")
)


# 4. CALCULATE COST

def calculate_cost(
    input_tokens,
    output_tokens,
    input_price,
    output_price
):

    input_cost = (
        input_tokens * input_price / 1_000_000
    )

    output_cost = (
        output_tokens * output_price / 1_000_000
    )

    return input_cost + output_cost


# 5. GEMINI PROVIDER

def run_gemini(prompt):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("\nGemini API key is missing.")
        return None

    client = None

    try:

        client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(
                timeout=120_000
            )
        )

        print("\nSending request to Gemini...")

        start_time = time.perf_counter()

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        elapsed_time = (
            time.perf_counter() - start_time
        )

        reply = response.text or ""

        usage = response.usage_metadata

        if usage is None:
            print("Gemini token usage is unavailable.")
            return None

        if usage.prompt_token_count is None:
            print("Gemini input token count is unavailable.")
            return None

        if usage.candidates_token_count is None:
            print("Gemini output token count is unavailable.")
            return None

        # Actual API token usage

        input_tokens = usage.prompt_token_count

        visible_output_tokens = (
            usage.candidates_token_count
        )

        thinking_tokens = (
            getattr(usage, "thoughts_token_count", 0) or 0
        )

        output_tokens = (
            visible_output_tokens + thinking_tokens
        )

        total_tokens = usage.total_token_count

        # Calculate estimated cost

        cost = calculate_cost(
            input_tokens,
            output_tokens,
            GEMINI_INPUT_PRICE,
            GEMINI_OUTPUT_PRICE
        )

        # Display response

        print("\nGEMINI RESPONSE")
        print(reply)

        print("\nGEMINI TOKEN USAGE")

        print("Input tokens:", input_tokens)
        print("Visible output tokens:", visible_output_tokens)
        print("Thinking tokens:", thinking_tokens)
        print("Billable output tokens:", output_tokens)
        print("Total tokens:", total_tokens)

        print("\nGEMINI COST")

        print(f"Gemini time: {elapsed_time:.2f} seconds")
        print(f"Total estimated cost: ${cost:.8f}")

        print("Pricing basis: Published standard paid rates.")
        print("Cost is an estimate, not an actual billing statement.")

        # Exactly eight required JSON fields

        result = {
            "provider": "gemini",
            "model": GEMINI_MODEL,
            "reply": reply,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "input_price_per_m": GEMINI_INPUT_PRICE,
            "output_price_per_m": GEMINI_OUTPUT_PRICE,
            "cost_usd": cost
        }

        return result, elapsed_time

    except Exception as error:

        print("\nGemini API error:", error)

        status_code = getattr(error, "code", None)

        if status_code in (401, 403):
            print("Check Gemini API key and permissions.")

        elif status_code == 404:
            print("Check the Gemini model ID.")

        elif status_code == 429:
            print("Gemini quota or rate limit may be exhausted.")

        elif status_code in (503, 504):
            print("Gemini service is temporarily unavailable.")
            print("Groq will still be attempted.")

        else:
            print("Check your Gemini configuration and internet connection.")

        return None

    finally:

        if client is not None:
            client.close()


# 6. GROQ PROVIDER

def run_groq(prompt):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print("\nGroq API key is missing.")
        return None

    client = None

    try:

        client = Groq(
            api_key=api_key,
            timeout=60.0,
            max_retries=1
        )

        print("\nSending request to Groq...")

        start_time = time.perf_counter()

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        elapsed_time = (
            time.perf_counter() - start_time
        )

        reply = (
            response.choices[0].message.content or ""
        )

        usage = response.usage

        if usage is None:
            print("Groq token usage is unavailable.")
            return None

        if usage.prompt_tokens is None:
            print("Groq input token count is unavailable.")
            return None

        if usage.completion_tokens is None:
            print("Groq output token count is unavailable.")
            return None

        # Actual API token usage

        input_tokens = usage.prompt_tokens

        output_tokens = usage.completion_tokens

        total_tokens = usage.total_tokens

        # Calculate estimated cost

        cost = calculate_cost(
            input_tokens,
            output_tokens,
            GROQ_INPUT_PRICE,
            GROQ_OUTPUT_PRICE
        )

        # Display response

        print("\nGROQ RESPONSE")
        print(reply)

        print("\nGROQ TOKEN USAGE")

        print("Input tokens:", input_tokens)
        print("Output tokens:", output_tokens)
        print("Total tokens:", total_tokens)

        print("\nGROQ COST")

        print(f"Groq time: {elapsed_time:.2f} seconds")
        print(f"Total estimated cost: ${cost:.8f}")

        print("Pricing basis: Published standard paid rates.")
        print("Cost is an estimate, not an actual billing statement.")

        # Exactly eight required JSON fields

        result = {
            "provider": "groq",
            "model": GROQ_MODEL,
            "reply": reply,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "input_price_per_m": GROQ_INPUT_PRICE,
            "output_price_per_m": GROQ_OUTPUT_PRICE,
            "cost_usd": cost
        }

        return result, elapsed_time

    except Exception as error:

        print("\nGroq API error:", error)

        return None

    finally:

        if client is not None:
            client.close()


# 7. PRINT COMPARISON TABLE

def print_comparison(results):

    print("\nPROVIDER COMPARISON")

    print(
        f"{'Provider':<12}"
        f"{'Input':>10}"
        f"{'Output':>10}"
        f"{'Seconds':>12}"
        f"{'Cost USD':>16}"
    )

    print("-" * 60)

    for item in results:

        print(
            f"{item['provider']:<12}"
            f"{item['input_tokens']:>10}"
            f"{item['output_tokens']:>10}"
            f"{item['seconds']:>12.2f}"
            f"{item['cost_usd']:>16.8f}"
        )


# 8. SAVE ALL RESULTS TO JSON

def save_results(results):

    file_name = "results.json"

    # Load previously saved results

    if os.path.exists(file_name):

        try:

            with open(
                file_name,
                "r",
                encoding="utf-8"
            ) as file:

                all_results = json.load(file)

            if not isinstance(all_results, list):
                print("\nError: Existing JSON must contain a list.")
                return False

        except (json.JSONDecodeError, OSError) as error:

            print("\nUnable to read existing results.json:", error)
            print("Previous results have not been overwritten.")
            return False

    else:

        all_results = []

    # Remove execution time from current records
    # Assignment requires exactly eight JSON fields

    json_results = []

    for item in results:

        result = item.copy()

        result.pop("seconds", None)

        json_results.append(result)

    # Append new results instead of replacing old results

    all_results.extend(json_results)

    # Save complete history

    try:

        with open(
            file_name,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                all_results,
                file,
                indent=4,
                ensure_ascii=False
            )

        print("\nResults successfully saved to results.json")
        print("New provider records:", len(json_results))
        print("Total provider records:", len(all_results))

        return True

    except OSError as error:

        print("\nUnable to save results:", error)
        return False


# 9. MAIN PROGRAM

def main():

    parser = argparse.ArgumentParser(
        description="Two Provider Cost Tracker"
    )

    parser.add_argument(
        "prompt",
        nargs="?",
        default=(
            "Explain what Artificial Intelligence is "
            "in three simple sentences."
        )
    )

    args = parser.parse_args()

    prompt = args.prompt

    print("\nTWO PROVIDER COST TRACKER")

    print("\nShared prompt:")
    print(prompt)

    results = []

    # Run Gemini

    gemini_result = run_gemini(prompt)

    print("\nGemini successful:", gemini_result is not None)

    if gemini_result is not None:

        result, seconds = gemini_result

        result["seconds"] = seconds

        results.append(result)

    # Run Groq

    groq_result = run_groq(prompt)

    print("\nGroq successful:", groq_result is not None)

    if groq_result is not None:

        result, seconds = groq_result

        result["seconds"] = seconds

        results.append(result)

    # Print comparison and save results

    if results:

        print_comparison(results)

        save_results(results)

    else:

        print("\nNo successful provider responses to save.")

    print("\nEXECUTION COMPLETED")


# 10. ENTRY POINT

if __name__ == "__main__":
    main()
