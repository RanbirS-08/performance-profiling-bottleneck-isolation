# Performance Profiling and Bottleneck Isolation

This repository contains the technical documentation and supporting files for a Minecraft Forge server performance investigation.

The work focused on server-thread lag, slow chunk loading, delayed entity response, and repeated overload warnings. The retained evidence includes runtime logs, Spark profiler captures, configuration files, screenshots, generated figures, and CSV summaries.

## Main results

| Metric | Initial | Post-change |
|---|---:|---:|
| Overload warning rate | 1.52 warnings/min | 0.14 warnings/min |
| Total tick-delay rate | 11,504.6 ms/min | 427.7 ms/min |
| Maximum tick delay | 48,576 ms | 3,978 ms |

The documentation treats the results as retrospective troubleshooting evidence. It does not claim a fully controlled benchmark or exact causality for every mod.

## Files

```text
Performance_Profiling_and_Bottleneck_Isolation.pdf
configs/                    Baseline and optimized Lycanites Mobs configurations
data/                       Runtime, Spark, configuration, and subsystem summaries
evidence/figures/           Figures used to summarize the results
evidence/screenshots/       Full retained screenshot set and screenshot index
evidence/profiler/          Representative raw Spark profiler exports
logs/                       Four sanitized runtime logs used in the comparison
scripts/analyze_logs.py     Python log parser
```

## Run the log parser

The parser uses only the Python standard library.

```bash
python scripts/analyze_logs.py logs --out data/generated
```

It creates:

```text
data/generated/log_summary.csv
data/generated/overload_events.csv
```

## Key data files

- `data/runtime_metrics.csv` - normalized warning and delay rates
- `data/runtime_sequence.csv` - the four retained test states
- `data/spark_metrics.csv` - TPS and MSPT values read from retained Spark screenshots
- `data/configuration_changes.csv` - baseline and optimized configuration values
- `data/subsystem_evidence.csv` - subsystem-level interpretation
- `data/log_summary.csv` - extracted counts from the retained logs
- `data/overload_events.csv` - individual server overload events

## Notes

- The logs are sanitized.
- The retained Spark screenshots used one player.
- Configuration percentages describe parameter changes, not direct CPU-time reductions.
- Three representative raw Spark exports are included instead of the full set of eighteen exports.
- The screenshot folder contains all 45 retained evidence images from the original project archive.
