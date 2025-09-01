# 🛠️ LiteLLM Tool Call Error Fix Guide

## 🚨 Problem Description
**Error**: `litellm.exceptions.BadRequestError: litellm.BadRequestError: OpenAIException - An assistant message with 'tool_calls' must be followed by tool messages responding to each 'tool_call_id'. The following tool_call_ids did not have response messages: call_Gx3aGEf5wW843xsAUl9u2MHi`

## 🔍 Root Cause
This error occurs when the AI agent makes tool calls but the system fails to properly respond to each tool call ID. The LiteLLM framework requires that every tool call receives a corresponding tool response message.

## ✅ Solutions Implemented

### 1. **Enhanced Tool Call Processing**
- **Sequential processing**: Tool calls are now processed one by one to ensure proper handling
- **Better error handling**: Each tool call gets a response, even if it's an error message
- **Timeout protection**: Tools are limited to 30 seconds execution time
- **Force completion**: Unprocessed tool calls are force-marked as completed

### 2. **Improved Error Handling**
- **Argument validation**: Tool arguments are cleaned and validated before execution
- **Type conversion**: String numbers are converted to actual numbers when needed
- **Fallback responses**: If a tool fails, a meaningful error message is sent back
- **Logging enhancement**: Better logging for debugging tool call issues

### 3. **Tool Call Lifecycle Management**
- **Collection phase**: All tool calls are collected before processing
- **Processing phase**: Each tool call is executed and responded to
- **Verification phase**: System ensures all tool calls have responses
- **Fallback phase**: Missing responses are handled gracefully

## 🚀 How the Fix Works

### **Before (Problematic)**
```python
# Tool calls were processed in the same loop as collection
for event in events:
    if event.tool_calls:
        for tool_call in event.tool_calls:
            # Process immediately - could miss some or fail
            result = await execute_tool(tool_func, **args)
```

### **After (Fixed)**
```python
# Phase 1: Collect all tool calls
tool_calls_to_process = []
for event in events:
    if event.tool_calls:
        for tool_call in event.tool_calls:
            tool_calls_to_process.append(tool_call)

# Phase 2: Process each tool call with proper error handling
for tool_call in tool_calls_to_process:
    try:
        result = await asyncio.wait_for(
            execute_tool(tool_func, **args), 
            timeout=30.0
        )
        await runner.send_tool_result(tool_call.id, result)
    except Exception as e:
        await runner.send_tool_result(tool_call.id, f"Error: {str(e)}")

# Phase 3: Verify all tool calls are processed
if len(tool_calls_processed) != len(tool_calls_to_process):
    # Force complete any missing tool calls
    for missing_tc in missing_tool_calls:
        await runner.send_tool_result(missing_tc.id, "Skipped due to error")
```

## 🔧 Key Improvements

### **1. Argument Validation**
```python
# Clean and validate tool arguments
cleaned_kwargs = {}
for key, value in kwargs.items():
    if value is not None and value != "":
        if isinstance(value, str):
            try:
                cleaned_kwargs[key] = int(value)  # Try int first
            except ValueError:
                try:
                    cleaned_kwargs[key] = float(value)  # Try float
                except ValueError:
                    cleaned_kwargs[key] = value  # Keep as string
```

### **2. Timeout Protection**
```python
# Execute tool with 30-second timeout
result = await asyncio.wait_for(
    execute_tool(tool_func, **tool_args), 
    timeout=30.0
)
```

### **3. Force Completion**
```python
# Ensure all tool calls get responses
for tool_call in tool_calls_to_process:
    if tool_call.id not in tool_calls_processed:
        await runner.send_tool_result(
            tool_call.id, 
            "Tool call was skipped due to processing error"
        )
```

## 🧪 Testing the Fix

### **1. Test Basic Tool Calls**
```bash
# Start the application
python3 start_app.py

# In the chat interface, try:
"Get customer information for John Doe"
```

### **2. Test Error Scenarios**
```bash
# Try invalid tool calls
"Get customer info with invalid parameters"
```

### **3. Monitor Logs**
```bash
# Watch for tool call processing logs
tail -f app.log  # or check console output
```

## 🚨 If You Still Get Errors

### **1. Check Tool Function Definitions**
Ensure all tools in `multi_agent_system.py` are properly defined:
```python
tools=[
    get_customer_info,
    call_customer_by_name,
    get_customers_to_call,
    # ... other tools
]
```

### **2. Verify Tool Function Signatures**
Tools should handle their arguments properly:
```python
def get_customer_info(customer_name: str, customer_id: str = None):
    # Handle both string and None values
    if customer_name is None:
        return "Error: Customer name is required"
    # ... rest of function
```

### **3. Check Environment Variables**
Ensure required API keys are set:
```bash
export OPENAI_API_KEY="your-api-key-here"
export TWILIO_ACCOUNT_SID="your-twilio-sid"
export TWILIO_AUTH_TOKEN="your-twilio-token"
```

## 📊 Monitoring and Debugging

### **Enable Debug Logging**
```python
# In run_agent_chat.py, change logging level
logging.basicConfig(level=logging.DEBUG)
```

### **Check Tool Call Flow**
The logs will now show:
1. Tool calls collected
2. Each tool execution
3. Tool results sent
4. Verification of completion

### **Common Log Messages**
```
INFO - Running tool: get_customer_info with args: {'customer_name': 'John'}
INFO - Tool get_customer_info executed successfully
INFO - Tool get_customer_info completed successfully for ID: call_abc123
INFO - Force-marked tool call call_xyz789 as processed
```

## 🎯 Expected Results

After applying these fixes:
- ✅ **No more tool call ID errors**
- ✅ **All tool calls get proper responses**
- ✅ **Better error messages for debugging**
- ✅ **Timeout protection for hanging tools**
- ✅ **Graceful fallback for failed tools**

## 🚀 Next Steps

1. **Restart your application** with the updated code
2. **Test basic functionality** to ensure tools work
3. **Monitor logs** for any remaining issues
4. **Report any new errors** with the enhanced logging

Your AI Collection Agent should now handle tool calls robustly without the LiteLLM errors! 🎉


