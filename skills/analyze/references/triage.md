# The 7-section triage — suggested questions

For each section: fill it from the intake, README, glossary and Explore first; it becomes a question only when the consequence is large or irreversible.

| Section | Must answer | Suggested question | Sign it is still missing |
|---|---|---|---|
| Goal | Why do it, value for whom, measured by what | "What is lost if we do not do this?" | Only a solution, no problem |
| Users | Who uses it, in what situation, how many people | "Who presses this button, and when?" | A generic "the user" |
| Scope in/out | What is in, what is NOT in (non-goals) | "Which similar piece of work is deliberately left out?" | No non-goal line |
| Data | Entities, fields, volume, sensitive data, retention | "Does this delete or change existing data?" | Nothing said about existing data |
| Interfaces / integrations | Screens, APIs, external systems, formats | "Who or which system calls this?" | Input/output format unclear |
| NFR | Performance, security, availability, accessibility, regulation | "How slow is unacceptable?" | Adjectives without numbers |
| Acceptance criteria | One criterion per behavior, a check command/step, the expected output | "How will you check it before you accept it?" | A criterion with no way to check it |

## Turn adjectives into numbers
| Adjective | Rewritten sentence | How to check |
|---|---|---|
| fast | p95 < N ms for operation X with M records | measurement command in the test plan |
| secure | only role Y can read field Z; another role gets a 403 error | access test |
| easy to use | task X completes in ≤ N steps | check step with a screenshot |
| correct | output matches the sample `<sample file>` byte for byte | comparison in a test |

## Format of one question (questions.md)
```
1. <question> — why it is needed: <the part of the work that changes with the answer>
   - a) <option> — consequence: <...>
   - b) <option> — consequence: <...>
   - Recommendation: b, because <...>
   - Checked: <path of the file/doc that does not answer it>
```

## The four fields of a decision (decide / Assumptions)
`chosen: … | why: … | alternative: … | correct if wrong: …`
