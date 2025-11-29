import os
from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent, ParallelAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import FunctionTool, google_search
from google.genai import types
from pypdf import PdfReader

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("gemini-key")
GOOGLE_SEARCH_API_KEY = os.getenv("search_key")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")

# Retry configuration
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# ============================================================================
# PDF Search Tool
# ============================================================================
def search_pdf_tool(file_path: str, query: str) -> str:
    """
    Searches for keywords within a PDF file and returns relevant text snippets.
    If the file is not found, returns mock data for demonstration.
    """
    print(f"    🔎 [Tool] Searching PDF '{file_path}' for: '{query}'")
    
    if os.path.exists(file_path):
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            paragraphs = text.split('\n\n')
            results = [p for p in paragraphs if query.lower() in p.lower()]
            
            if results:
                return "\n---\n".join(results[:3])
            return "No specific matches found in the document."
        except Exception as e:
            return f"Error reading PDF: {e}"
    else:
        print(f"    ⚠️ [Tool] File not found. Using MOCK data for demonstration.")
        mock_content = {
            "quantum": "Quantum computing uses qubits to perform calculations exponentially faster than classical bits.",
            "ai": "Artificial Intelligence agents can perceive their environment and take actions to achieve goals.",
            "climate": "Climate change mitigation requires a transition to renewable energy sources."
        }
        for key, value in mock_content.items():
            if key in query.lower():
                return f"Found in mock PDF: {value}"
        return "No information found in the mock document."

# ============================================================================
# Agent Definitions
# ============================================================================

# 1. PDF Reader Agent
pdf_reader_agent = Agent(
    name="PDFReader",
    model=Gemini(model=MODEL_NAME, retry_options=retry_config),
    instruction="""You are an expert document researcher. 
    Your job is to use the `search_pdf_tool` to find specific information in a document based on the user's request.
    Always cite the specific text segments you found.""",
    tools=[FunctionTool(search_pdf_tool)],
    output_key="pdf_findings"
)

# 2. Summarizer Agent
summarizer_agent = Agent(
    name="Summarizer",
    model=Gemini(model=MODEL_NAME, retry_options=retry_config),
    instruction="""You are an expert scientific paper analyst. 
    Read the research paper content provided: {pdf_findings}
    
    Create a comprehensive summary that includes:
    1. **Main Topic**: What is the paper about?
    2. **Key Contributions**: What are the novel contributions and innovations?
    3. **Methodology**: What approaches or methods were used?
    4. **Results/Findings**: What were the main outcomes?
    
    Keep the summary clear, structured, and under 200 words.
    If the findings are empty, state that no information was found.""",
    output_key="final_summary"
)

# 3. Tech Researcher Agent
tech_researcher = Agent(
    name="Tech_Researcher",
    model=Gemini(model=MODEL_NAME, retry_options=retry_config),
    instruction="""You are a senior research analyst.
Input: {pdf_findings}

1. Extract the paper's **main technical focus**, research problem, and method.
2. Evaluate the paper technically:
   - What is innovative?
   - What is weak or missing?
   - What assumptions does it make?
   - Possible real-world applications?
3. Perform a web search using the search tool:
   - Find the latest (2024–2025) work, breakthroughs, or criticisms related to the same topic.
   - Prefer scholarly or technical sources.
4. Produce a concise synthesis (max 100 words):
   - Technical evaluation of the paper
   - How the latest research trends compare or validate/challenge it
   - Missing gaps or future directions

Your output must be factual, technical, and short.""",
    tools=[google_search],
    output_key="tech_research"
)

# Parallel Research Team
parallel_research_team = ParallelAgent(
    name="ParallelResearchTeam",
    sub_agents=[summarizer_agent, tech_researcher],
)

# 4. Research Aggregator Agent
research_aggregator = Agent(
    name="ResearchAggregator",
    model=Gemini(model=MODEL_NAME, retry_options=retry_config),
    instruction="""You are a research synthesis expert.
Input:
1. Summary from Summarizer Agent: {final_summary}
2. Technical research from Tech Researcher Agent: {tech_research}
Your task is to combine these inputs into a single, coherent research report that addresses the user's original question. Ensure the report is clear, concise, and well-structured.""",
    output_key="research_report"
)

# Sequential Research Workflow Agent
Research_workflow_Agent = SequentialAgent(
    name="ResearchWorkflowAgent",
    sub_agents=[pdf_reader_agent, parallel_research_team, research_aggregator],
)

# Export main components
__all__ = [
    "search_pdf_tool",
    "pdf_reader_agent",
    "summarizer_agent",
    "tech_researcher",
    "parallel_research_team",
    "research_aggregator",
    "Research_workflow_Agent",
]
