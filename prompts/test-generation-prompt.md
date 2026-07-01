# Prompt Used for Unit Test Generation

**Source:** Paper Appendix A (Section 4.4)

This is the exact standardized prompt used for all LLMs and all projects. Do not modify when replicating the study.

## Prompt text

```
You are a senior Java developer writing unit tests for a real-world codebase.

Given the source code of a Java project, identify all production classes that meet the following criteria:
- Located under src/main/java
- Are concrete classes (not abstract)
- Are not interfaces
- Are not enums
- Declare at least one public method

For each eligible class, generate JUnit 5 unit tests following these rules:
- Tests must compile successfully
- Use realistic and idiomatic test structures
- Include meaningful assertions reflecting real developer intent
- Cover common use cases and a small number of relevant edge cases
- Use clear and natural test method and variable names
- Avoid exhaustive or artificial edge cases
- Avoid mocks unless strictly necessary
- Do not include any comments in the test code

Important constraints:
- Generate one test class per production class
- Place tests under src/test/java, mirroring the package structure
- Do not generate tests for classes that do not meet the eligibility criteria
- Do not modify the production code
```

## How the prompt was applied (Cursor)

1. Open the target Apache Commons project in **Cursor Pro 2.1.39**.
2. Select the LLM model (Opus 4.5, GPT-5.1 Codex Max, or Sonnet 4.5).
3. Paste the prompt above into the AI chat with full project context enabled.
4. Allow the model to generate tests for all eligible production classes.
5. Do **not** modify production code under `src/main/java`.
6. Compile and run tests; remove failing tests iteratively until the suite is green (required for PIT).
7. Record removed tests in `logs/removed-tests.csv`.

## Notes

- The same prompt was used for every model–project pair.
- Only one generation was performed per pair (no multiple independent runs).
- Generated tests must be placed under `src/test/java` mirroring package structure.
