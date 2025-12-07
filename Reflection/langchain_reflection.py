import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

# Optional: import the specific exception class used in your traceback
try:
    from google.api_core.exceptions import NotFound as GoogleNotFound
except Exception:
    GoogleNotFound = None

# --- Configuration ---
load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in .env file. Please add it.")

# Candidate models to try (most-likely/current first)
MODEL_CANDIDATES = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-1.5-flash",   # keep the old one as a last resort
]

def get_working_llm(candidates, temperature=0.1):
    """
    Try to create a ChatGoogleGenerativeAI for each candidate model.
    Return the first working `llm` instance. If none work, raise RuntimeError.
    """
    last_exception = None
    for model_name in candidates:
        print(f"Trying model: {model_name} ...")
        try:
            llm = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)
            # Do a lightweight probe call to verify model availability.
            # Use a tiny prompt so we confirm the model responds before running the full loop.
            probe = [HumanMessage(content="Say 'ok'")]
            resp = llm.invoke(probe)
            # If we get here without raising, model works
            print(f"Model '{model_name}' appears to be available — using it.\n")
            return llm, model_name
        except Exception as e:
            # Distinguish NotFound where possible
            if GoogleNotFound is not None and isinstance(e, GoogleNotFound):
                print(f"Model '{model_name}' not found (404). Trying next candidate...")
            else:
                # Generic fallback message; still continue trying other candidates.
                print(f"Failed to use model '{model_name}': {type(e).__name__}: {e}")
                print("Trying next candidate (if any)...")
            last_exception = e

    # If we reach here, no candidate worked.
    msg = (
        "None of the candidate models worked. "
        "Recommended actions:\n"
        "  1) Upgrade the client libraries: "
        "`pip install --upgrade google-genai langchain-google-genai langchain`\n"
        "  2) Check your Google AI / Vertex AI console or AI Studio to list available models for your account.\n"
        "  3) Replace MODEL_CANDIDATES with a model name available to your account.\n"
        f"Last error: {last_exception}"
    )
    raise RuntimeError(msg)

def run_reflection_loop(llm):
    """
    Demonstrates a multi-step AI reflection loop to progressively improve a Python function.
    """
    task_prompt = """
    Your task is to create a Python function named `calculate_factorial`.
    This function should do the following:
    1. Accept a single integer `n` as input.
    2. Calculate its factorial (n!).
    3. Include a clear docstring explaining what the function does.
    4. Handle edge cases: The factorial of 0 is 1.
    5. Handle invalid input: Raise a ValueError if the input is a negative number.
    """

    max_iterations = 3
    current_code = ""
    message_history = [HumanMessage(content=task_prompt)]

    for i in range(max_iterations):
        print("\n" + "=" * 25 + f" REFLECTION LOOP: ITERATION {i + 1} " + "=" * 25)

        # --- 1. GENERATE / REFINE STAGE ---
        if i == 0:
            print("\n>>> STAGE 1: GENERATING initial code...")
            response = llm.invoke(message_history)
            current_code = response.content
        else:
            print("\n>>> STAGE 1: REFINING code based on previous critique...")
            message_history.append(HumanMessage(content="Please refine the code using the critiques provided."))
            response = llm.invoke(message_history)
            current_code = response.content

        print("\n--- Generated Code (v" + str(i + 1) + ") ---\n" + current_code)
        message_history.append(response)

        # --- 2. REFLECT STAGE ---
        print("\n>>> STAGE 2: REFLECTING on the generated code...")
        reflector_prompt = [
            SystemMessage(content="""
                You are a senior software engineer and an expert in Python.
                Your role is to perform a meticulous code review.
                Critically evaluate the provided Python code based on the original task requirements.
                Look for bugs, style issues, missing edge cases, and areas for improvement.
                If the code is perfect and meets all requirements, respond with the single phrase 'CODE_IS_PERFECT'.
                Otherwise, provide a bulleted list of your critiques.
            """),
            HumanMessage(content=f"Original Task:\n{task_prompt}\n\nCode to Review:\n{current_code}")
        ]

        critique_response = llm.invoke(reflector_prompt)
        critique = critique_response.content

        if "CODE_IS_PERFECT" in critique:
            print("\n--- Critique ---\nNo further critiques found. The code is satisfactory.")
            break

        print("\n--- Critique ---\n" + critique)
        message_history.append(HumanMessage(content=f"Critique of the previous code:\n{critique}"))

    print("\n" + "=" * 30 + " FINAL RESULT " + "=" * 30)
    print("\nFinal refined code after the reflection process:\n")
    print(current_code)


if __name__ == "__main__":
    # Get a working LLM (tries candidates)
    try:
        llm, used_model = get_working_llm(MODEL_CANDIDATES, temperature=0.1)
        print(f"Using model: {used_model}")
    except RuntimeError as exc:
        # Helpful final message and exit
        print("\nERROR: Could not find a working model.\n")
        print(str(exc))
        raise SystemExit(1)

    # Run your loop
    run_reflection_loop(llm)
