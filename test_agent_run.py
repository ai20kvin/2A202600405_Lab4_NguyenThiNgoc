#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from agent import graph

user_input = "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!"

print("=" * 60)
print("TravelBuddy – Trợ lý Du lịch Thông minh")
print("=" * 60)

print(f"\nBạn: {user_input}")
print("\nTravelBuddy đang suy nghĩ...")

result = graph.invoke({"messages": [("human", user_input)]})

# Print all messages to show tool calls
for i, msg in enumerate(result["messages"]):
    msg_type = getattr(msg, "type", "unknown")
    content = getattr(msg, "content", "")
    tool_calls = getattr(msg, "tool_calls", [])
    
    if tool_calls:
        print(f"\n[Message {i}] Type: {msg_type}")
        print(f"Tool calls: {tool_calls}")
    
final = result["messages"][-1]
print(f"\n\nTravelBuddy: {final.content}")
