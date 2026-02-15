# Journal Entry Agent (Agent 15.1)

## ID: `journal_entry_agent`

## Role & Objective
The 'Librarian'. Manages the Vector DB and ensures that all system documentation, research, and conversational history are correctly indexed and searchable for the entire agent workforce.

## Logic & Algorithm
- **Embedding Generation**: Converts text snippets into vector embeddings (using OpenAI or local models) for the Neo4j or Pinecone index.
- **Context Injection**: Provides the Orchestrator with relevant historical "Knowledge Snippets" based on the current user query.
- **Knowledge Pruning**: Identifies redundant or contradictory research and prompts for consolidation.

## Inputs & Outputs
- **Inputs**:
  - `raw_text_corpus` (List): Research papers, logs, and user messages.
- **Outputs**:
  - `vector_index_status` (Success/Fail).
  - `retrieved_context` (List): The top-K most relevant historical snippets.

## Acceptance Criteria
- Achieve a retrieval latency of < 100ms for a corpus of 100,000+ entries.
- Ensure 100% data residency by storing the private vector index in the encrypted Docker subnet.
