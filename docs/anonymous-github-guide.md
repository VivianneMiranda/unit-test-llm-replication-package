# Anonymous GitHub — Submission Guide

Steps to publish this replication package for **double-blind review** at SAST 2026.

## Prerequisites

- GitHub account
- This repository pushed to a **private** GitHub repo with a neutral name (e.g., `sast26-unit-test-llm-replication`)
- No identifying information in commits, README, or file paths

## Phase A — Prepare the repository

1. **Review identifying content** using [`ANONYMIZATION_CHECKLIST.md`](ANONYMIZATION_CHECKLIST.md).
2. Create a fresh private repo or squash history to remove author-identifying commits.
3. Ensure `README.md` does not contain author names, affiliations, or institutional URLs.
4. Push `main` branch with the full replication package.

## Phase B — Configure Anonymous GitHub

1. Open [https://anonymous.4open.science/](https://anonymous.4open.science/)
2. Sign in with GitHub
3. Click **Anonymize**
4. Paste repository URL: `https://github.com/<username>/<repo>`
5. Set anonymized ID: `SAST26-UnitTest-LLM` (or similar neutral slug)
6. Add **terms to redact** (one per line). Copy from `config/anonymization-terms.example.txt` and fill locally — do not commit real terms.
   - Author names and co-authors
   - University / company names
   - Email addresses
   - GitHub usernames
   - Local paths (`C:\Users\...`)
7. Set expiration date after the review cycle
8. Save and copy the link: `https://anonymous.4open.science/r/SAST26-UnitTest-LLM/`

## Phase C — Verify anonymization

1. Open the anonymous link in a **private/incognito** browser window
2. Browse README, scripts, and config — confirm no leaked identities
3. Download the anonymized zip and spot-check file contents
4. Test that setup scripts still reference correct relative paths

## Phase D — Cite in the manuscript

Add to the paper (artifact availability section or footnote):

> *Replication package (anonymized for review):* https://anonymous.4open.science/r/SAST26-UnitTest-LLM/

## After acceptance

1. Publish the real GitHub repository (public)
2. Optionally archive on Zenodo for a DOI
3. Update camera-ready with the permanent URL
4. Remove or extend the Anonymous GitHub expiration

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Empty mirror | Ensure repo is accessible to the GitHub OAuth app; check branch name |
| Terms not redacted | Add variants (with/without accents, email domains) |
| Filename leaks identity | Anonymous GitHub anonymizes filenames; rename before push if needed |
| Large files rejected | Use Git LFS or host raw PIT reports externally with URL in README |

## References

- Anonymous GitHub: [https://anonymous.4open.science/](https://anonymous.4open.science/)
- Project documentation: [https://github.com/tdurieux/anonymous_github](https://github.com/tdurieux/anonymous_github)
