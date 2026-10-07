# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `python -m journeykit` entry point for environments where the console script is not on PATH (Windows user installs)
- `tests/test_examples.py`: contract for every example under `examples/*/` – schema-valid, `meta.synthetic: true`, no lint errors, `journey.json` without warnings, every quote atom verbatim in its source file, no contact data in raw inputs. New examples are picked up without extra code
- Second worked example `examples/baubewilligung/`: building permit for a heat pump, applicant and neighbour as two personas, synthetic raw inputs (3 interviews, 30 inquiries, case statistics, web analytics, process document, workshop notes); README documents seven transferability hypotheses and what the example showed
- ADR-0005 (accepted): optional `step.performed_by` (`kind` persona/shared/intermediary, `role`, `mandate` formal/informal) for steps carried out by intermediaries on the persona's behalf – finding H1 from the building-permit example. Schema stays 1.0 (additive)
- Schema: channel `publication` (official publication, notice board, building profile) and source kind `case_records` (case-management statistics, counted as a user source for L011) – findings H7 and «missing source kind» from the building-permit example
- Lint L073 (INFO): more than half of the steps carried out by intermediaries – check the diagnosis
- Viewer: chip «mit …» / «durch …» for steps with `performed_by`, in the journey and process layers

### Changed
- Skill: review question «breakdown or a legal remedy that works?» (Einsprache, Rekurs), with a note in the synthesis step and the public-administration context of `methodik.md` – finding H4 (#14)
- `journeykit lint` text output prints each rule's hint only once per run
- CI validates and lints every example directory instead of a hard-coded path

### Fixed
- Viewer: the persona overlay in the emotion curve no longer drops data silently – phases without data or without emotion evidence of the other persona are labelled, phases without a matching ID are listed, and the legend notes that positions within a phase are approximate (#9)
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
