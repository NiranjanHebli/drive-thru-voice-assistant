# Architectural Decision Record: Auto-Bundling Combos

## Context
Customers in drive-thrus order disjointed items (e.g., "A burger, fries, and a coke"). Charging them individually results in overcharging.

## Decision
Combo recognition is strictly handled by deterministic backend Python logic (`app/services/optimizer.py`), not by the Llama 3 AI model.

1. **LLM Math Hallucinations:** Even highly tuned models like Llama 3 8B struggle with deterministic math and state tracking across long conversations. Asking the AI to apply bundle pricing risks hallucinated totals.
2. **Deterministic Rules:** Combo bundling is strict mathematical logic. The `optimize_cart()` function scans the session cart array in Valkey, groups matching trigger items with required sides, and applies the bundle price safely.
3. **Separation of Concerns:** The AI's only job is natural language understanding (NLU) and triggering `add_to_cart`. The FastAPI backend handles the financial calculation.