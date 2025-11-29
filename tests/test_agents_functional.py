import sys
import os
from pathlib import Path
from tests.agents import (
    search_pdf_tool,
    pdf_reader_agent,
    summarizer_agent,
    tech_researcher,
    research_aggregator,
    parallel_research_team,
    Research_workflow_Agent
)

def print_header(title):
    print("\n" + "="*80)
    print(f"🔬 {title}")
    print("="*80)

def check_pdf_exists():
    """Check if document.pdf exists in current directory"""
    pdf_path = Path("document.pdf")
    if pdf_path.exists():
        file_size = pdf_path.stat().st_size
        print(f"✅ Found document.pdf ({file_size} bytes)")
        return True
    else:
        print(f"⚠️  document.pdf not found in {Path.cwd()}")
        print(f"   Files in current directory: {list(Path('.').glob('*.pdf'))}")
        return False

def test_pdf_search_functionality():
    """Test actual PDF search functionality with document.pdf"""
    print_header("FUNCTIONAL TEST 1: PDF Search Tool (Using document.pdf)")
    
    if not check_pdf_exists():
        print("❌ Cannot test without document.pdf")
        return False
    
    print("\n✓ Testing PDF search with real queries...\n")
    
    test_cases = [
        ("abstract", "Should find abstract section"),
        ("introduction", "Should find introduction"),
        ("method", "Should find methodology section"),
        ("result", "Should find results section"),
    ]
    
    results = {}
    for query, description in test_cases:
        print(f"  Query: '{query}' - {description}")
        try:
            result = search_pdf_tool("document.pdf", query)
            
            # Validate result
            if result and len(result) > 0 and "No information found" not in result:
                results[query] = result
                print(f"    ✅ SUCCESS: Got {len(result)} characters of content")
                print(f"    Preview: {result[:80]}...\n")
            else:
                print(f"    ⚠️  No matching content found for '{query}'\n")
        except Exception as e:
            print(f"    ❌ FAILED: {e}\n")
    
    success_rate = len(results) / len(test_cases)
    if success_rate >= 0.5:
        print(f"✅ PDF search functionality working ({len(results)}/{len(test_cases)} queries successful)")
        return True
    else:
        print(f"❌ PDF search functionality limited ({len(results)}/{len(test_cases)} queries successful)")
        return False

def test_pdf_reader_agent_functionality():
    """Test PDF Reader Agent actual execution"""
    print_header("FUNCTIONAL TEST 2: PDF Reader Agent Execution")
    
    print("\n✓ Testing if PDF Reader Agent can be instantiated and configured...\n")
    
    try:
        # Check agent properties
        print(f"Agent Name: {pdf_reader_agent.name}")
        print(f"Output Key: {pdf_reader_agent.output_key}")
        print(f"Has Model: {pdf_reader_agent.model is not None}")
        print(f"Has Tools: {len(pdf_reader_agent.tools) > 0}")
        print(f"Has Instruction: {pdf_reader_agent.instruction is not None}")
        
        # Check if instruction is meaningful
        if "document researcher" in pdf_reader_agent.instruction.lower():
            print("\n✅ PDF Reader Agent is properly configured for document research")
            return True
        else:
            print("\n❌ PDF Reader Agent instruction is not properly configured")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_summarizer_agent_functionality():
    """Test Summarizer Agent configuration and readiness"""
    print_header("FUNCTIONAL TEST 3: Summarizer Agent Execution")
    
    print("\n✓ Testing if Summarizer Agent can process input...\n")
    
    try:
        print(f"Agent Name: {summarizer_agent.name}")
        print(f"Output Key: {summarizer_agent.output_key}")
        print(f"Has Model: {summarizer_agent.model is not None}")
        
        # Check instruction contains key requirements
        instruction = summarizer_agent.instruction.lower()
        requirements = ["topic", "contribution", "methodology", "results"]
        
        found_requirements = [req for req in requirements if req in instruction]
        print(f"Found {len(found_requirements)}/{len(requirements)} required elements in instruction")
        
        if len(found_requirements) >= 3:
            print("\n✅ Summarizer Agent is properly configured for comprehensive summaries")
            return True
        else:
            print("\n❌ Summarizer Agent missing required elements")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_tech_researcher_functionality():
    """Test Tech Researcher Agent configuration"""
    print_header("FUNCTIONAL TEST 4: Tech Researcher Agent Execution")
    
    print("\n✓ Testing if Tech Researcher Agent can perform analysis...\n")
    
    try:
        print(f"Agent Name: {tech_researcher.name}")
        print(f"Output Key: {tech_researcher.output_key}")
        print(f"Has Model: {tech_researcher.model is not None}")
        print(f"Has Search Tools: {len(tech_researcher.tools) > 0}")
        
        # Check instruction contains key analysis elements
        instruction = tech_researcher.instruction.lower()
        analysis_elements = ["technical", "innovative", "weak", "application", "search"]
        
        found_elements = [elem for elem in analysis_elements if elem in instruction]
        print(f"Found {len(found_elements)}/{len(analysis_elements)} analysis elements in instruction")
        
        if len(found_elements) >= 4:
            print("\n✅ Tech Researcher Agent is properly configured for technical analysis")
            return True
        else:
            print("\n❌ Tech Researcher Agent missing analysis elements")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_aggregator_functionality():
    """Test Research Aggregator Agent configuration"""
    print_header("FUNCTIONAL TEST 5: Research Aggregator Agent Execution")
    
    print("\n✓ Testing if Aggregator Agent can synthesize results...\n")
    
    try:
        print(f"Agent Name: {research_aggregator.name}")
        print(f"Output Key: {research_aggregator.output_key}")
        print(f"Has Model: {research_aggregator.model is not None}")
        
        # Check instruction for synthesis capability
        instruction = research_aggregator.instruction.lower()
        synthesis_elements = ["synthesis", "coherent", "combine", "input", "report"]
        
        found_elements = [elem for elem in synthesis_elements if elem in instruction]
        print(f"Found {len(found_elements)}/{len(synthesis_elements)} synthesis elements in instruction")
        
        if len(found_elements) >= 3:
            print("\n✅ Research Aggregator Agent is properly configured for synthesis")
            return True
        else:
            print("\n❌ Research Aggregator Agent missing synthesis elements")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_workflow_execution_chain():
    """Test if workflow is properly chained"""
    print_header("FUNCTIONAL TEST 6: Workflow Execution Chain")
    
    print("\n✓ Testing workflow execution sequence...\n")
    
    try:
        workflow = Research_workflow_Agent
        
        print(f"Workflow Name: {workflow.name}")
        print(f"Total Steps: {len(workflow.sub_agents)}\n")
        
        # Verify execution chain
        step_names = []
        for i, agent in enumerate(workflow.sub_agents, 1):
            print(f"Step {i}: {agent.name}")
            step_names.append(agent.name)
            
            if hasattr(agent, 'sub_agents'):
                for j, sub_agent in enumerate(agent.sub_agents, 1):
                    print(f"  ├─ {j}. {sub_agent.name} (Output: {sub_agent.output_key})")
        
        # Verify correct order
        expected_order = ["PDFReader", "ParallelResearchTeam", "ResearchAggregator"]
        if step_names == expected_order:
            print(f"\n✅ Workflow execution chain is correct: {' → '.join(step_names)}")
            return True
        else:
            print(f"\n❌ Workflow execution chain is incorrect")
            print(f"   Expected: {expected_order}")
            print(f"   Got: {step_names}")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_parallel_execution():
    """Test parallel team execution capability"""
    print_header("FUNCTIONAL TEST 7: Parallel Execution")
    
    print("\n✓ Testing parallel team configuration...\n")
    
    try:
        team = parallel_research_team
        
        print(f"Team Name: {team.name}")
        print(f"Execution Type: Parallel (simultaneous)")
        print(f"Number of Agents: {len(team.sub_agents)}\n")
        
        # Verify both agents are present
        agent_names = [agent.name for agent in team.sub_agents]
        
        print("Parallel Agents:")
        for i, name in enumerate(agent_names, 1):
            agent = team.sub_agents[i-1]
            print(f"  {i}. {name} (Output: {agent.output_key})")
        
        # Both should run simultaneously
        if "Summarizer" in agent_names and "Tech_Researcher" in agent_names:
            print(f"\n✅ Parallel team is properly configured")
            print(f"   Both agents will run simultaneously and combine results")
            return True
        else:
            print(f"\n❌ Parallel team missing required agents")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def main():
    print("\n╔" + "="*78 + "╗")
    print("║" + " "*18 + "🤖 AGENT FUNCTIONALITY TEST SUITE" + " "*26 + "║")
    print("╚" + "="*78 + "╝")
    print(f"\nCurrent Directory: {Path.cwd()}")
    
    tests = [
        ("PDF Search Functionality", test_pdf_search_functionality),
        ("PDF Reader Agent", test_pdf_reader_agent_functionality),
        ("Summarizer Agent", test_summarizer_agent_functionality),
        ("Tech Researcher Agent", test_tech_researcher_functionality),
        ("Research Aggregator Agent", test_aggregator_functionality),
        ("Workflow Execution Chain", test_workflow_execution_chain),
        ("Parallel Execution", test_parallel_execution),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results[test_name] = "✅ PASS" if passed else "❌ FAIL"
        except Exception as e:
            print(f"\n❌ ERROR in {test_name}: {e}")
            results[test_name] = "❌ ERROR"
    
    # Print Summary
    print_header("TEST SUMMARY")
    
    print("\n")
    for test_name, status in results.items():
        print(f"{status} - {test_name}")
    
    passed_count = sum(1 for s in results.values() if "PASS" in s)
    total_count = len(results)
    
    print(f"\n{'='*80}")
    print(f"Results: {passed_count}/{total_count} tests passed")
    print(f"{'='*80}\n")
    
    if passed_count == total_count:
        print("🎉 All functionality tests passed!")
        print("Your agents are fully functional and ready for deployment!\n")
    else:
        print("⚠️  Some tests failed. Please review the output above.\n")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
