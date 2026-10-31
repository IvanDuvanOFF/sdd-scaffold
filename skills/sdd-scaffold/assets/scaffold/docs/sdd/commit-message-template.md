# <date and time>: <short batch title>

- Time: <YYYY-MM-DDTHH:mm:ss+07:00>
- Batch / summary: <link>
- Basis: <message request and human acceptance of the batch>

## Git message

```text
<brief description of the change>

<if needed: reason, behavior, and significant details>
```

The message block must not contain Co-authored-by or other agent signatures/trailers.
Before filling it in: required checks are complete, both working lists are clear,
and history is preserved. Afterwards, documenter removes only completed assignments
in the accepted batch and updates the summary. Creating this file does not run git commit.
