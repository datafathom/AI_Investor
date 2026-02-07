# Backend Service: AI Assistant

## Overview
The **AI Assistant Service** provides a conversational interface for users to interact with the AI Investor platform. It combines natural language understanding with a personalized learning system to offer context-aware advice, answer investment questions, and adapt to individual user preferences over time.

## Core Components

### Assistant Service (`assistant_service.py`)
The primary orchestrator for user-AI conversations.
- **Role**: Manages the lifecycle of a conversation and coordinates with the LLM and the learning engine.
- **Key Features**:
    - **Session Management**: Creates and stores unique conversation IDs.
    - **Context Aggregation**: Pulls user preferences and portfolio data to ground the AI's responses.
    - **Interaction Loop**: processes incoming user messages and generates structured AI responses.

### Learning Service (`learning_service.py`)
The personalization and recommendation engine.
- **Role**: Tracks user behavior and preferences to ensure the assistant becomes more relevant over time.
- **Key Features**:
    - **Preference Tracking**: Learns and stores investment parameters like risk tolerance and style (e.g., Growth vs. Value).
    - **Recommendation Engine**: Generates proactive investment suggestions (e.g., "Consider diversifying your portfolio") based on user state and preferences.
    - **Interactive Learning**: Analyzes conversation transcripts to refine its understanding of the user.

## Dependencies
- `services.ai`: Used for the underlying LLM completions.
- `services.system.cache_service`: Used for fast retrieval of conversation history and learned preferences.
- `schemas.ai_assistant`: Defines the data models for conversations and messages.

## Usage Example

### Starting a Conversation
```python
from services.ai_assistant.assistant_service import get_assistant_service

assistant = get_assistant_service()
conv = await assistant.create_conversation(user_id="USR-001", title="Retirement Planning")
print(f"Conversation {conv.conversation_id} created.")
```

### Getting Recommendations
```python
from services.ai_assistant.learning_service import get_learning_service

learning = get_learning_service()
recs = await learning.get_recommendations(user_id="USR-001")
for r in recs:
    print(f"Suggestion [{r.confidence*100}% Confidence]: {r.title} - {r.description}")
```
