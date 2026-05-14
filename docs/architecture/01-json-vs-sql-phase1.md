# Architectural Decision Record: JSON vs SQL for Phase 1

## Context
The system requires a highly relational menu structure to handle complex QSR pricing logic, including modifiers, combos, and conditional time-based offers. 

## Decision
For Phase 1 (Prototyping & System Design), we are using a static, normalized JSON file (`order_details.json`) instead of a relational database (PostgreSQL).

1. **Native LLM Tool Calling:** Open-source models like Llama 3 8B Instruct natively support JSON schema parsing for function calling. Keeping the menu in JSON creates a 1:1 mapping with the AI's expected tool formats.
2. **Schema Agility:** QSR menu logic changes rapidly during prototyping. JSON allows us to alter schema structure instantly via the Streamlit Admin dashboard without writing database migrations.
3. **Performance:** The JSON file is loaded directly into RAM when the FastAPI server starts, eliminating database I/O latency. This is crucial when the local LLM needs to query the menu in under 50 milliseconds to maintain fluid conversation.

## Future Path 
Once the schema is stabilized, this JSON structure will be migrated to PostgreSQL to handle live inventory tracking.