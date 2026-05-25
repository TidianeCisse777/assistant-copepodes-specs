# Reuse the IDEA Runtime Prompt for the Copepod Agent

The copepod system prompt will start from the existing IDEA runtime prompt because it already contains the required OpenInterpreter mechanics for code execution, file handling, plotting, security, persistence, and artifact export. The domain layer will be rewritten: sea-level, tide-gauge, UHSLC station, datum, climate-index, and generic geoscience instructions are removed and replaced with the copepod plotting domain: EcoTaxa, EcoPart, Amundsen CTD, lab data, OGSL, Bio-ORACLE, and the copepod RAG documents.

This keeps the proven runtime behavior while making the agent's business identity a plotting assistant for marine copepod data. The agent must produce reproducible graphs and technical deliverables, but must not provide scientific or biological interpretation.
