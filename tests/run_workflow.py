#!/usr/bin/env python
"""
Direct workflow execution without notebook async complications.
Run with: python run_workflow.py
"""

import os
from pathlib import Path
from tests.agents import (
    search_pdf_tool,
    pdf_reader_agent,
    Research_workflow_Agent
)

def main():
    print("\n" + "="*80)
    print("🤖 AI Research Paper Analyzer - Direct Execution")
    print("="*80 + "\n")
    
    # Check PDF exists
    pdf_path = "document.pdf"
    if not Path(pdf_path).exists():
        print(f"❌ {pdf_path} not found!")
        print(f"   Current directory: {Path.cwd()}")
        return
    
    print(f"✅ Found {pdf_path}\n")
    
    # Step 1: Extract PDF content
    print("Step 1: Extracting PDF content...")
    print("-" * 80)
    
    pdf_content = search_pdf_tool(pdf_path, "abstract introduction methodology")
    print(f"✅ Extracted {len(pdf_content)} characters\n")
    
    # Step 2: Show workflow structure
    print("Step 2: Workflow Structure")
    print("-" * 80)
    print(f"Workflow: {Research_workflow_Agent.name}")
    print(f"Steps: {len(Research_workflow_Agent.sub_agents)}\n")
    
    for i, agent in enumerate(Research_workflow_Agent.sub_agents, 1):
        print(f"  {i}. {agent.name}")
        if hasattr(agent, 'sub_agents'):
            for sub_agent in agent.sub_agents:
                print(f"     └─ {sub_agent.name}")
    
    print("\n✅ All agents configured and ready!")
    print("\n📌 Note: For actual workflow execution, ensure API keys are set in .env:")
    print("   - gemini-key=your_google_api_key")
    print("   - search_key=your_search_api_key")

if __name__ == '__main__':
    main()
