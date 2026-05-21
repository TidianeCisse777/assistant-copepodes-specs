# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project context

Research data exploration repository for the NeoLab copepod assistant project (Université Laval). The goal is to understand, export, and join data from EcoTaxa, EcoPart, and Amundsen Science (CTD), as a foundation for an AI/RAG agent that answers scientific questions about zooplankton.

Key domain concepts are defined in `CONTEXT.md`. The data dictionary is in `DATA_DICTIONARY.md`. The plan for converting scripts into agent tools is in `TOOLS_AGENT_PLAN.md`.

## Running scripts

Each probe is a self-contained subdirectory with its own `requirements.txt`. Scripts require a `.env` file (see `.env.example` in `ecotaxa_loki_probe/`) with EcoTaxa credentials.

```bash
# LOKI EcoTaxa project 2331
cd ecotaxa_loki_probe
pip install -r requirements.txt
python src/export_loki_authenticated.py
python src/inspect_loki_export.py

# EcoPart 105 ↔ EcoTaxa 1165 join
cd ecopart_1165_link_probe
python src/probe_ecopart_1165_link.py
python src/test_minimal_join.py
python src/build_depth_enriched_table.py
python src/export_ecopart_105_authenticated.py

# Amundsen Science CTD data
cd amundsen_data_probe
python src/search_catalog.py
python src/inspect_resources.py
python src/compare_ecopart_amundsen_ctd.py
```

There are no automated tests or linters configured.

## Architecture

### Data sources and their IDs

| Source | ID | Content |
|---|---|---|
| EcoTaxa project LOKI | `2331` | Copepod lipids, annotated taxonomy, TSV export |
| EcoTaxa project UVP | `1165` | UVP5 Amundsen 2018, individual objects + morphometry |
| EcoPart dataset | `105` | UVP5 Amundsen 2018, CTD profiles + aggregated particles |
| Amundsen CTD | `ca-cioos_ccin-12713` | Full CTD-Rosette via ERDDAP |

### Join key

EcoTaxa objects join to EcoPart profiles via:
```
obj_orig_id (e.g. ips_007_899) → profile_id (ips_007) → EcoPart profile_id
```
The next join level adds `profile_id + depth` to attach CTD/particle data per object.

### Directory layout

- `ecotaxa_loki_probe/` — LOKI export scripts and report
- `ecopart_1165_link_probe/` — EcoPart/EcoTaxa join scripts and reports
- `amundsen_data_probe/` — Amundsen Science CKAN/ERDDAP exploration
- `examples_tsv/` — Lightweight TSV samples covering each data source (safe to commit)
- `visualization/` — Static HTML+JS functional view of the assistant architecture (open `index.html` in a browser, no build step)
- `STAGE ULAVAL/` — Stage documents and elicitation analysis (French)

### Probe pattern

Each probe follows the same pattern: `src/` scripts write results to `outputs/report*.md`. Scripts are standalone (no shared library yet); the plan is to stabilize them into reusable Python tools before any MCP server.

### Sensitive data

`.env` files hold EcoTaxa/EcoPart credentials and are never committed. Full exports are regenerated locally from scripts. Only TSV samples in `examples_tsv/` are committed.
