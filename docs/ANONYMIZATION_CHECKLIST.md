# Anonymization Checklist

Complete before pushing to GitHub and configuring Anonymous GitHub.

## Content to remove or redact

- [ ] Author names in any file (README, docs, comments, PDF metadata)
- [ ] Co-author names
- [ ] University, department, lab, or company names
- [ ] Email addresses and ORCID
- [ ] GitHub username in URLs, badges, or clone instructions
- [ ] Local filesystem paths (`C:\Users\...`, `/home/username/...`)
- [ ] API keys (OpenAI, Anthropic, Cursor)
- [ ] Acknowledgments with identifying grants tied to individuals
- [ ] Screenshots showing IDE username or machine hostname

## Git hygiene

- [ ] `git log` does not reveal author identity (squash or fresh repo if needed)
- [ ] `.git/config` not committed
- [ ] `config/anonymization-terms.txt` listed in `.gitignore` (personal terms file)

## Files safe to include

- [x] Apache Commons project versions (public)
- [x] Standardized prompt (Appendix A)
- [x] Maven scripts without local paths
- [ ] Paper manuscript PDF (not included in replication package)

## Anonymous GitHub terms file

1. Copy `config/anonymization-terms.example.txt` to `config/anonymization-terms.txt` (local only)
2. Fill all identifying terms
3. Paste into Anonymous GitHub "Terms to redact" field
4. Re-scan anonymous mirror after saving

## Manuscript text (before anonymization)

Use a placeholder in the README until the mirror is configured. After Anonymous GitHub setup, add the link to the README and paper using:

```
https://anonymous.4open.science/r/SAST26-UnitTest-LLM/
```

See `docs/manuscript-artifact-text.md` for the full snippet.

## Post-review

- [ ] Publish non-anonymous repository
- [ ] Update paper with permanent link
- [ ] Revoke or extend Anonymous GitHub mirror
