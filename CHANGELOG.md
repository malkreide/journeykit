# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `python -m journeykit` entry point for environments where the console script is not on PATH (Windows user installs)

## [0.1.0] - 2026-10-05

### Added
- Journey model as JSON Schema 2020-12 (`schema_version` 1.0): persona, scenario, phases, steps, pain points (friction/breakdown), edge cases, recovery paths, KPIs, opportunities with stories, sources with PII status, evidence atoms with evidence class, open questions, changelog
- Methodological lints L001–L102 for the five journey-mapping pitfalls plus blueprint smell, privacy, KPI translation and evidence quality
- Self-contained interactive viewer with five layers (journey, process and failure paths, evidence heatmap, opportunities matrix, audit), evidence drill-down, primary-evidence filter, multi-persona overlay, light/dark, print
- CLI `journeykit`: validate, lint, render, export (storymap, actions, opportunities, audit), diff, new, schema
- Claude skill `user-journey` with modes Synthesis, Workshop and Audit, and references on diagnosis, evidence, methodology, KPI translation and review questions
- Worked synthetic example «Kindergarteneintritt aus Elternsicht» with raw inputs, two personas and a workshop-hypothesis version for diffing
- Concept paper and ADRs 0001–0004
