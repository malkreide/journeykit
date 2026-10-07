# Security Policy

## Supported versions

| Version | Supported |
|---|---|
| 0.1.x | yes |

## Reporting a vulnerability

Please do not open a public issue for security problems. Use GitHub's private
vulnerability reporting on this repository («Security» → «Report a
vulnerability»). You will get an acknowledgement within a week.

## Scope and data protection

JourneyKit processes journey files that may contain quotes from real people.
The tool itself makes no network requests, stores nothing outside the files
you give it, and the rendered HTML contains no external resources. The data
protection responsibility stays with the person creating the journey:

- Set `sources[].pii_status` truthfully. Files with `contains_pii` fail lint L080 and must not be shared.
- Anonymise transcripts before extracting evidence; keep raw material out of the repository.
- The example in `examples/` is entirely synthetic.

If you find that the viewer or an export leaks data it should not (for example
through unescaped content), report it as a vulnerability.
