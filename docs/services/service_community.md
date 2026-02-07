# Backend Service: Community

## Overview
The **Community Service** facilitates collaborative intelligence and peer-to-peer engagement within the Sovereign OS ecosystem. It provides the infrastructure for structured financial discussion forums and a verified **Expert Q&A** system, enabling users to share insights, validate strategies, and access domain experts directly.

## Core Components

### 1. Expert Q&A System (`expert_qa_service.py`)
A high-integrity channel for direct consultation with financial specialists.
- **Intelligent Routing**: Automatically matches incoming user questions to verified experts based on category and specialty.
- **Answer Quality Lifecycle**:
    - **Open**: Question is active and awaiting expert input.
    - **Answered**: An expert has responded.
    - **Best Answer**: The user has selected a definitive response, which closes the question and updates the system's knowledge base.
- **Verification Logic**: Maintains registry of expert credentials and specialties to ensure high-signal responses.

### 2. Community Forum Service (`forum_service.py`)
The social architecture for collaborative investing.
- **Thread Management**: Supports multi-category discussion threads (e.g., "Macro," "Equities," "DeFi") with full title and content indexing.
- **Engagement Mechanics**:
    - **Nested Replies**: Enables structured, threaded conversations with parent/child relationships.
    - **Upvoting System**: Implements a popularity and quality discovery mechanism, allowing top-tier insights to surface to the community dashboard.
- **Activity Tracking**: Real-time monitoring of reply counts and "Last Active" timestamps to maintain forum vibrancy.

## Dependencies
- `pydantic`: Enforces schemas for `ForumThread`, `ThreadReply`, and `ExpertQuestion`.
- `services.system.cache_service`: Provides high-speed persistence for active discussions and Q&A threads.
- `services.communication.notification_service`: Triggers alerts for user mentions or expert responses.

## Usage Examples

### Creating a Category-Based Forum Thread
```python
from services.community.forum_service import get_forum_service

forum = get_forum_service()

thread = await forum.create_thread(
    user_id="user_vanguard_1",
    category="Macro",
    title="Impact of 2026 Yield Curve Inversion",
    content="How is the sovereign OS positioning for the upcoming rate hike cycle?"
)

print(f"Thread Live: {thread.thread_id} in {thread.category}")
```

### Routing a Question to an Expert
```python
from services.community.expert_qa_service import get_expert_qa_service

qa_service = get_expert_qa_service()

question = await qa_service.create_question(
    user_id="user_vanguard_1",
    title="Tax Implication of Tokenized Real Estate",
    content="What are the K-1 requirements for fractionalized REITS in the EU?",
    category="Tax_Law"
)

print(f"Question Routed to Expert: {question.expert_id}")
```
