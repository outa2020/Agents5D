import unittest
from pathlib import Path
from tests.agents import (
    search_pdf_tool, 
    pdf_reader_agent, 
    summarizer_agent, 
    tech_researcher, 
    Research_workflow_Agent,
    parallel_research_team,
    research_aggregator
)

class TestAgentModule(unittest.TestCase):
    def test_pdf_reader_agent_exists(self):
        """Test that PDF Reader Agent is properly initialized"""
        self.assertIsNotNone(pdf_reader_agent, "pdf_reader_agent is None")
        self.assertEqual(pdf_reader_agent.name, "PDFReader", "PDF Reader agent name mismatch")
        print(f"✅ PDF Reader Agent initialized: {pdf_reader_agent.name}")
    
    def test_pdf_reader_can_read_document(self):
        """Test if PDF reader can read document.pdf"""
        pdf_path = "document.pdf"
        
        result = search_pdf_tool(pdf_path, "abstract")
        self.assertIsNotNone(result, "search_pdf_tool returned None")
        self.assertTrue(len(result) > 0, "search_pdf_tool returned empty result")
        print(f"✅ PDF reader test passed. Found content.")
    
    def test_pdf_search_with_different_queries(self):
        """Test PDF search with multiple query types"""
        pdf_path = "document.pdf"
        queries = ["abstract", "methodology", "results", "conclusion"]
        
        for query in queries:
            result = search_pdf_tool(pdf_path, query)
            self.assertIsNotNone(result, f"search_pdf_tool returned None for query: {query}")
            print(f"✅ Query '{query}' returned results")
    
    def test_summarizer_agent_exists(self):
        """Test that Summarizer Agent is properly initialized"""
        self.assertIsNotNone(summarizer_agent, "summarizer_agent is None")
        self.assertEqual(summarizer_agent.name, "Summarizer", "Summarizer agent name mismatch")
        print(f"✅ Summarizer Agent initialized: {summarizer_agent.name}")
    
    def test_tech_researcher_agent_exists(self):
        """Test that Tech Researcher Agent is properly initialized"""
        self.assertIsNotNone(tech_researcher, "tech_researcher is None")
        self.assertEqual(tech_researcher.name, "Tech_Researcher", "Tech Researcher agent name mismatch")
        print(f"✅ Tech Researcher Agent initialized: {tech_researcher.name}")
    
    def test_parallel_research_team_exists(self):
        """Test that Parallel Research Team is properly initialized"""
        self.assertIsNotNone(parallel_research_team, "parallel_research_team is None")
        self.assertEqual(parallel_research_team.name, "ParallelResearchTeam", "Parallel team name mismatch")
        print(f"✅ Parallel Research Team initialized: {parallel_research_team.name}")
    
    def test_research_aggregator_exists(self):
        """Test that Research Aggregator Agent is properly initialized"""
        self.assertIsNotNone(research_aggregator, "research_aggregator is None")
        self.assertEqual(research_aggregator.name, "ResearchAggregator", "Aggregator agent name mismatch")
        print(f"✅ Research Aggregator Agent initialized: {research_aggregator.name}")
    
    def test_workflow_agent_exists(self):
        """Test that Research Workflow Agent is properly initialized"""
        self.assertIsNotNone(Research_workflow_Agent, "Research_workflow_Agent is None")
        self.assertEqual(Research_workflow_Agent.name, "ResearchWorkflowAgent", "Workflow agent name mismatch")
        print(f"✅ Research Workflow Agent initialized: {Research_workflow_Agent.name}")
    
    def test_pdf_search_mock_data_fallback(self):
        """Test PDF search fallback to mock data when file doesn't exist"""
        non_existent_path = "non_existent.pdf"
        
        # Test with a keyword that exists in mock data
        result = search_pdf_tool(non_existent_path, "quantum")
        self.assertIsNotNone(result, "search_pdf_tool returned None for mock data")
        self.assertIn("quantum", result.lower(), "Mock data should contain 'quantum'")
        print(f"✅ Mock data fallback working correctly")
    
    def test_all_agents_have_output_keys(self):
        """Verify all agents have output_key defined"""
        agents_to_check = [
            (pdf_reader_agent, "pdf_findings"),
            (summarizer_agent, "final_summary"),
            (tech_researcher, "tech_research"),
            (research_aggregator, "research_report"),
        ]
        
        for agent, expected_key in agents_to_check:
            self.assertEqual(agent.output_key, expected_key, f"{agent.name} output_key mismatch")
            print(f"✅ {agent.name} has correct output_key: {expected_key}")

class TestPDFSearchTool(unittest.TestCase):
    """Test the PDF search tool functionality"""
    
    def test_search_pdf_with_existing_file(self):
        """Test searching in document.pdf"""
        result = search_pdf_tool("document.pdf", "abstract")
        self.assertIsNotNone(result)
        self.assertTrue(len(result) > 0)
        print(f"✅ PDF search successful: {result[:100]}...")
    
    def test_search_pdf_with_multiple_keywords(self):
        """Test searching with different keywords"""
        keywords = ["introduction", "method", "result", "conclusion"]
        for keyword in keywords:
            result = search_pdf_tool("document.pdf", keyword)
            self.assertIsNotNone(result)
            print(f"✅ Search for '{keyword}' returned: {len(result)} chars")
    
    def test_search_pdf_fallback_to_mock(self):
        """Test fallback to mock data when file doesn't exist"""
        result = search_pdf_tool("fake.pdf", "quantum")
        self.assertIn("quantum", result.lower())
        print(f"✅ Mock fallback works: {result}")
    
    def test_search_pdf_returns_string(self):
        """Verify search_pdf_tool returns string type"""
        result = search_pdf_tool("document.pdf", "test")
        self.assertIsInstance(result, str)
        print(f"✅ search_pdf_tool returns string type")

class TestPDFReaderAgent(unittest.TestCase):
    """Test PDF Reader Agent initialization and properties"""
    
    def test_agent_initialization(self):
        """Verify PDF Reader Agent is properly initialized"""
        self.assertIsNotNone(pdf_reader_agent)
        self.assertEqual(pdf_reader_agent.name, "PDFReader")
        print(f"✅ PDF Reader Agent name: {pdf_reader_agent.name}")
    
    def test_agent_has_model(self):
        """Verify agent has Gemini model configured"""
        self.assertIsNotNone(pdf_reader_agent.model)
        print(f"✅ PDF Reader Agent has model: {type(pdf_reader_agent.model)}")
    
    def test_agent_has_tools(self):
        """Verify agent has search_pdf_tool configured"""
        self.assertIsNotNone(pdf_reader_agent.tools)
        self.assertTrue(len(pdf_reader_agent.tools) > 0)
        print(f"✅ PDF Reader Agent has {len(pdf_reader_agent.tools)} tool(s)")
    
    def test_agent_output_key(self):
        """Verify agent has correct output_key"""
        self.assertEqual(pdf_reader_agent.output_key, "pdf_findings")
        print(f"✅ PDF Reader Agent output_key: {pdf_reader_agent.output_key}")
    
    def test_agent_instruction_present(self):
        """Verify agent has instruction defined"""
        self.assertIsNotNone(pdf_reader_agent.instruction)
        self.assertIn("document researcher", pdf_reader_agent.instruction.lower())
        print(f"✅ PDF Reader Agent has instruction defined")

class TestSummarizerAgent(unittest.TestCase):
    """Test Summarizer Agent initialization and properties"""
    
    def test_agent_initialization(self):
        """Verify Summarizer Agent is properly initialized"""
        self.assertIsNotNone(summarizer_agent)
        self.assertEqual(summarizer_agent.name, "Summarizer")
        print(f"✅ Summarizer Agent name: {summarizer_agent.name}")
    
    def test_agent_has_model(self):
        """Verify agent has Gemini model configured"""
        self.assertIsNotNone(summarizer_agent.model)
        print(f"✅ Summarizer Agent has model: {type(summarizer_agent.model)}")
    
    def test_agent_output_key(self):
        """Verify agent has correct output_key"""
        self.assertEqual(summarizer_agent.output_key, "final_summary")
        print(f"✅ Summarizer Agent output_key: {summarizer_agent.output_key}")
    
    def test_agent_instruction_includes_requirements(self):
        """Verify agent instruction includes summary requirements"""
        self.assertIsNotNone(summarizer_agent.instruction)
        instruction = summarizer_agent.instruction.lower()
        self.assertIn("topic", instruction)
        self.assertIn("contribution", instruction)
        print(f"✅ Summarizer Agent instruction includes all requirements")

class TestTechResearcherAgent(unittest.TestCase):
    """Test Tech Researcher Agent initialization and properties"""
    
    def test_agent_initialization(self):
        """Verify Tech Researcher Agent is properly initialized"""
        self.assertIsNotNone(tech_researcher)
        self.assertEqual(tech_researcher.name, "Tech_Researcher")
        print(f"✅ Tech Researcher Agent name: {tech_researcher.name}")
    
    def test_agent_has_model(self):
        """Verify agent has Gemini model configured"""
        self.assertIsNotNone(tech_researcher.model)
        print(f"✅ Tech Researcher Agent has model: {type(tech_researcher.model)}")
    
    def test_agent_has_search_tool(self):
        """Verify agent has google_search tool"""
        self.assertIsNotNone(tech_researcher.tools)
        self.assertTrue(len(tech_researcher.tools) > 0)
        print(f"✅ Tech Researcher Agent has {len(tech_researcher.tools)} tool(s)")
    
    def test_agent_output_key(self):
        """Verify agent has correct output_key"""
        self.assertEqual(tech_researcher.output_key, "tech_research")
        print(f"✅ Tech Researcher Agent output_key: {tech_researcher.output_key}")
    
    def test_agent_instruction_includes_analysis(self):
        """Verify agent instruction includes technical evaluation"""
        self.assertIsNotNone(tech_researcher.instruction)
        instruction = tech_researcher.instruction.lower()
        self.assertIn("technical", instruction)
        self.assertIn("innovative", instruction)
        print(f"✅ Tech Researcher Agent instruction includes technical evaluation")

class TestResearchAggregator(unittest.TestCase):
    """Test Research Aggregator Agent initialization and properties"""
    
    def test_agent_initialization(self):
        """Verify Research Aggregator Agent is properly initialized"""
        self.assertIsNotNone(research_aggregator)
        self.assertEqual(research_aggregator.name, "ResearchAggregator")
        print(f"✅ Research Aggregator Agent name: {research_aggregator.name}")
    
    def test_agent_has_model(self):
        """Verify agent has Gemini model configured"""
        self.assertIsNotNone(research_aggregator.model)
        print(f"✅ Research Aggregator Agent has model: {type(research_aggregator.model)}")
    
    def test_agent_output_key(self):
        """Verify agent has correct output_key"""
        self.assertEqual(research_aggregator.output_key, "research_report")
        print(f"✅ Research Aggregator Agent output_key: {research_aggregator.output_key}")
    
    def test_agent_instruction_includes_synthesis(self):
        """Verify agent instruction includes synthesis requirements"""
        self.assertIsNotNone(research_aggregator.instruction)
        instruction = research_aggregator.instruction.lower()
        self.assertIn("synthesis", instruction)
        self.assertIn("coherent", instruction)
        print(f"✅ Research Aggregator Agent instruction includes synthesis requirements")

class TestParallelResearchTeam(unittest.TestCase):
    """Test Parallel Research Team"""
    
    def test_team_initialization(self):
        """Verify Parallel Research Team is properly initialized"""
        self.assertIsNotNone(parallel_research_team)
        self.assertEqual(parallel_research_team.name, "ParallelResearchTeam")
        print(f"✅ Parallel Research Team name: {parallel_research_team.name}")
    
    def test_team_has_sub_agents(self):
        """Verify team has sub-agents"""
        self.assertIsNotNone(parallel_research_team.sub_agents)
        self.assertEqual(len(parallel_research_team.sub_agents), 2)
        print(f"✅ Parallel Research Team has {len(parallel_research_team.sub_agents)} sub-agents")
    
    def test_team_includes_summarizer(self):
        """Verify team includes Summarizer Agent"""
        agent_names = [agent.name for agent in parallel_research_team.sub_agents]
        self.assertIn("Summarizer", agent_names)
        print(f"✅ Parallel Research Team includes Summarizer")
    
    def test_team_includes_tech_researcher(self):
        """Verify team includes Tech Researcher Agent"""
        agent_names = [agent.name for agent in parallel_research_team.sub_agents]
        self.assertIn("Tech_Researcher", agent_names)
        print(f"✅ Parallel Research Team includes Tech Researcher")

class TestResearchWorkflowAgent(unittest.TestCase):
    """Test Research Workflow Agent (Sequential)"""
    
    def test_workflow_initialization(self):
        """Verify Research Workflow Agent is properly initialized"""
        self.assertIsNotNone(Research_workflow_Agent)
        self.assertEqual(Research_workflow_Agent.name, "ResearchWorkflowAgent")
        print(f"✅ Research Workflow Agent name: {Research_workflow_Agent.name}")
    
    def test_workflow_has_sub_agents(self):
        """Verify workflow has sub-agents in correct order"""
        self.assertIsNotNone(Research_workflow_Agent.sub_agents)
        self.assertEqual(len(Research_workflow_Agent.sub_agents), 3)
        print(f"✅ Research Workflow Agent has {len(Research_workflow_Agent.sub_agents)} sub-agents")
    
    def test_workflow_first_agent_is_pdf_reader(self):
        """Verify first agent in sequence is PDF Reader"""
        first_agent = Research_workflow_Agent.sub_agents[0]
        self.assertEqual(first_agent.name, "PDFReader")
        print(f"✅ Workflow first step: {first_agent.name}")
    
    def test_workflow_second_agent_is_parallel_team(self):
        """Verify second agent in sequence is Parallel Research Team"""
        second_agent = Research_workflow_Agent.sub_agents[1]
        self.assertEqual(second_agent.name, "ParallelResearchTeam")
        print(f"✅ Workflow second step: {second_agent.name}")
    
    def test_workflow_third_agent_is_aggregator(self):
        """Verify third agent in sequence is Research Aggregator"""
        third_agent = Research_workflow_Agent.sub_agents[2]
        self.assertEqual(third_agent.name, "ResearchAggregator")
        print(f"✅ Workflow third step: {third_agent.name}")
    
    def test_workflow_execution_order(self):
        """Verify correct workflow execution order"""
        expected_order = ["PDFReader", "ParallelResearchTeam", "ResearchAggregator"]
        actual_order = [agent.name for agent in Research_workflow_Agent.sub_agents]
        self.assertEqual(actual_order, expected_order)
        print(f"✅ Workflow execution order: {' → '.join(expected_order)}")

if __name__ == '__main__':
    unittest.main()
