#!/usr/bin/env python3
"""
Debug script for tool call handling in AI Collection Agent
This script provides detailed debugging information to help resolve LiteLLM tool call errors
"""

import asyncio
import logging
import traceback
from run_agent_chat import init_agent, ask_agent

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def debug_tool_call_flow():
    """Debug the complete tool call flow"""
    print("🔍 Debugging Tool Call Flow")
    print("=" * 50)
    
    try:
        # Initialize the agent
        print("1. Initializing agent...")
        await init_agent()
        print("✅ Agent initialized successfully")
        
        # Test queries that might trigger tool calls
        test_queries = [
            "Hello, how are you?",
            "Show me customer information",
            "Get customer data for John Doe",
            "Analyze customer database"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n📝 Test Query {i}: {query}")
            print("-" * 30)
            
            try:
                print("   Executing query...")
                response = await ask_agent(query)
                print(f"   ✅ Response received: {response[:100]}...")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                print(f"   📋 Error type: {type(e).__name__}")
                print(f"   🔍 Error details: {str(e)}")
                
                # Check if it's a LiteLLM tool call error
                if "tool_calls" in str(e) and "tool_call_id" in str(e):
                    print("   🚨 LITELLM TOOL CALL ERROR DETECTED!")
                    print("   This indicates the tool call handling is still not working properly.")
                    
                    # Extract tool call ID from error
                    import re
                    tool_call_match = re.search(r'call_[A-Za-z0-9]+', str(e))
                    if tool_call_match:
                        tool_call_id = tool_call_match.group(0)
                        print(f"   🔍 Problematic tool call ID: {tool_call_id}")
                        print(f"   💡 This tool call did not receive a proper response")
                
                print(f"   📚 Full traceback:")
                traceback.print_exc()
                
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        traceback.print_exc()

async def debug_session_management():
    """Debug session management and runner behavior"""
    print("\n🔍 Debugging Session Management")
    print("=" * 50)
    
    try:
        from run_agent_chat import session_service, runner, root_agent
        from google.adk.runners import Runner
        
        print(f"1. Session service: {type(session_service).__name__}")
        print(f"2. Runner: {type(runner).__name__}")
        print(f"3. Root agent: {type(root_agent).__name__}")
        print(f"4. Root agent tools: {len(root_agent.tools) if hasattr(root_agent, 'tools') else 'No tools'}")
        
        if hasattr(root_agent, 'tools'):
            for i, tool in enumerate(root_agent.tools):
                print(f"   Tool {i+1}: {tool.__name__}")
        
    except Exception as e:
        print(f"❌ Error in session debugging: {e}")
        traceback.print_exc()

async def debug_specific_tool_call():
    """Debug a specific tool call that's failing"""
    print("\n🔍 Debugging Specific Tool Call")
    print("=" * 50)
    
    try:
        # Try to trigger a specific tool call
        print("Attempting to trigger a tool call...")
        
        # This should trigger a tool call
        response = await ask_agent("Get customer information for John Doe")
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()

async def main():
    """Main debug function"""
    print("🚀 AI Collection Agent - Tool Call Debug Session")
    print("=" * 60)
    
    try:
        # Run all debug functions
        await debug_session_management()
        await debug_tool_call_flow()
        await debug_specific_tool_call()
        
        print("\n" + "=" * 60)
        print("✅ Debug session completed!")
        print("Check the output above for any issues or errors.")
        
    except Exception as e:
        print(f"\n❌ Debug session failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    # Run the debug session
    asyncio.run(main())


