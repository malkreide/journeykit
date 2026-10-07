# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `python -m journeykit` entry point for environments where the console script is not on PATH (Windows user installs)
- `tests/test_examples.py`: contract for every example under `examples/*/` – schema-valid, `meta.synthetic: true`, no lint errors, `journey.json` without warnings, every quote atom verbatim in its source file, no contact data in raw inputs. New examples are picked up without extra code
- Second worked example `examples/baubewilligung/`: building permit for a heat pump, applicant and neighbour as two personas, synthetic raw inputs (3 interviews, 30 inquiries, case statistics, web analytics, process document, workshop notes); README documents seven transferability hypotheses and what the example showed

### Changed
- `journeykit lint` text output prints each rule's hint only once per run
- CI validates and lints every example directory instead of a hard-coded path

### Fixed
- Viewer: the persona badge in the header wraps instead of overflowing; long persona names pushed the page to 481 px at a 390 px viewport

### Security
- `/eval/` is git-ignored: raw material and ground truth for the evaluation stay local; only the comparison report (under `docs/evaluation/`) is committed

## [0.1.0] - 2026-10-05

### Added
- Journey model as JSON Schema 2020-12 (`schema_version` 1.0): persona, scenario, phases, steps, pain points (friction/breakdown), edge cases, recovery paths, KPIs, opportunities with stories, sources with PII status, evidence atoms with evidence class, open questions, changelog
- Methodological lints L001–L102 for the five journey-mapping pitfalls plus blueprint smell, privacy, KPI translation and evidence quality
- Self-contained interactive viewer with five layers (journey, process and failure paths, evidence heatmap, opportunities matrix, audit), evidence drill-down, primary-evidence filter, multi-persona overlay, light/dark, print
- CLI `journeykit`: validate, lint, render, export (storymap, actions, opportunities, audit), diff, new, schema
- Claude skill `user-journey` with modes Synthesis, Workshop and Audit, and references on diagnosis, evidence, methodology, KPI translation and review questions
- Worked synthetic example «Kindergarteneintritt aus Elternsicht» with raw inputs, two personas and a workshop-hypothesis version for diffing
- Concept paper and ADRs 0001–0004
