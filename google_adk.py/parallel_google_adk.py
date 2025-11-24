import os
import asyncio
import uuid
from dotenv import load_dotenv
from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent
from google.adk.tools import google_search
from google.adk.runners import InMemoryRunner
from google.genai import types

# Load environment variables
load_dotenv()
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY', '')

GEMINI_MODEL = "gemini-2.0-flash"

# --- 1. Define Researcher Sub-Agents ---
researcher_agent_1 = LlmAgent(
    name="RenewableEnergyResearcher",
    model=GEMINI_MODEL,
    instruction="""You are an AI Research Assistant specializing in energy.
Research the latest advancements in 'renewable energy sources'.
Use the Google Search tool provided.
Summarize your key findings concisely (1-2 sentences).
Output *only* the summary.""",
    description="Researches renewable energy sources.",
    tools=[google_search],
    output_key="renewable_energy_result"
)

researcher_agent_2 = LlmAgent(
    name="EVResearcher",
    model=GEMINI_MODEL,
    instruction="""You are an AI Research Assistant specializing in transportation.
Research the latest developments in 'electric vehicle technology'.
Use the Google Search tool provided.
Summarize your key findings concisely (1-2 sentences).
Output *only* the summary.""",
    description="Researches electric vehicle technology.",
    tools=[google_search],
    output_key="ev_technology_result"
)

researcher_agent_3 = LlmAgent(
    name="CarbonCaptureResearcher",
    model=GEMINI_MODEL,
    instruction="""You are an AI Research Assistant specializing in climate solutions.
Research the current state of 'carbon capture methods'.
Use the Google Search tool provided.
Summarize your key findings concisely (1-2 sentences).
Output *only* the summary.""",
    description="Researches carbon capture methods.",
    tools=[google_search],
    output_key="carbon_capture_result"
)

# --- 2. Create ParallelAgent ---
parallel_research_agent = ParallelAgent(
    name="ParallelWebResearchAgent",
    sub_agents=[researcher_agent_1, researcher_agent_2, researcher_agent_3],
    description="Runs multiple research agents in parallel to gather information."
)

# --- 3. Define Merger Agent ---
merger_agent = LlmAgent(
    name="SynthesisAgent",
    model=GEMINI_MODEL,
    instruction="""You are an AI Assistant responsible for combining research findings into a structured report.

**Input Summaries:**
*   **Renewable Energy:** {renewable_energy_result}
*   **Electric Vehicles:** {ev_technology_result}
*   **Carbon Capture:** {carbon_capture_result}

**Output Format:**
## Summary of Recent Sustainable Technology Advancements

### Renewable Energy Findings
{renewable_energy_result}

### Electric Vehicle Findings
{ev_technology_result}

### Carbon Capture Findings
{carbon_capture_result}

### Overall Conclusion
[Brief concluding statement connecting the findings above.]""",
    description="Combines research findings into a structured report."
)

# --- 4. Create SequentialAgent ---
root_agent = SequentialAgent(
    name="ResearchAndSynthesisPipeline",
    sub_agents=[parallel_research_agent, merger_agent],
    description="Coordinates parallel research and synthesizes results."
)

# --- 5. Run Function ---
async def run_research_pipeline():
    print("--- Google ADK Parallel Research Pipeline ---")
    runner = InMemoryRunner(root_agent)
    
    try:
        user_id = "researcher_123"
        session_id = str(uuid.uuid4())
        
        await runner.session_service.create_session(
            app_name=runner.app_name, user_id=user_id, session_id=session_id
        )
        
        print("\n🔍 Starting parallel research...")
        
        for event in runner.run(
            user_id=user_id,
            session_id=session_id,
            new_message=types.Content(
                role='user',
                parts=[types.Part(text="Start the research pipeline")]
            ),
        ):
            if event.is_final_response() and event.content:
                if hasattr(event.content, 'text') and event.content.text:
                    final_result = event.content.text
                elif event.content.parts:
                    text_parts = [part.text for part in event.content.parts if part.text]
                    final_result = "".join(text_parts)
                
                print("\n📊 Final Research Report:")
                print("=" * 50)
                print(final_result)
                
                # Force exit to avoid cleanup errors
                import sys
                sys.exit(0)
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    import nest_asyncio
    import warnings
    
    # Suppress asyncio cleanup warnings
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    
    nest_asyncio.apply()
    
    try:
        asyncio.run(run_research_pipeline())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")