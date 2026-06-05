# Copepod Live Test Map

Use this checklist to validate live sessions in `IDEA` against the expected agent behavior.

## How to use

For each live session:

1. Record the `session_id`.
2. Pick the scenario you are testing.
3. Check each item below from the live logs:
   - `events.jsonl`
   - `turns.log`
   - `session_summary.json`
4. Mark each row `yes` or `no`.
5. If a row is `no`, capture the exact log line that proves it.

## Checklist

| Check | What to verify | yes/no | Evidence |
|---|---|---|---|
| `new_file_inspected` | `inspect_and_report` appears on the first turn for a newly uploaded file. |  |  |
| `report_rendered_cleanly` | The visible report is clean markdown, not a raw Python dict or console noise. |  |  |
| `already_inspected_silent` | A file that is already inspected does not trigger `already inspected` / `déjà inspecté` noise. |  |  |
| `uses_session_summary` | The agent reuses the session summary / working-set facts for already inspected files. |  |  |
| `graph_readiness_called` | `graph_readiness` is called before any graph or graph-derived table. |  |  |
| `tool_order_correct` | The tool order matches the expected flow for the scenario. |  |  |
| `last_tool_calls_filled` | `last_tool_calls` is populated when a tool actually ran. |  |  |
| `turn_index_correct` | Tool events are logged under the correct `turn_index`. |  |  |
| `turns_log_readable` | `turns.log` shows readable blocks such as `[CALL]`, `[ARGS]`, `[RESULT]`, `[ERROR]`. |  |  |
| `no_internal_bruit` | No user-visible leak of `pending`, `retry`, `already inspected`, or `do not narrate` wording. |  |  |

## Suggested scenarios

| Scenario | Goal |
|---|---|
| `upload_and_inspect` | Validate the first inspection path for a new file. |
| `readback_after_inspection` | Validate clean readback after a file is already inspected. |
| `graph_after_inspection` | Validate `graph_readiness` and tool order for graph requests. |

## Pass rule

A session is considered good only if every check required by the scenario is `yes`.

