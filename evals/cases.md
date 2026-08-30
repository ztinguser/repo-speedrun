# Repo Speedrun Behavioral Evals

## Case 1: Service with a stale test script

Repository: https://github.com/ztinguser/simple-career-rag.git

Pinned revision: 6932ca23b49c5c40b111b3a79eda34fa86020b08

Reading budget: 5 minutes

### Expected behavior

- Select one representative user-visible flow.
- Produce 3–4 checkpoints totaling no more than 5 minutes.
- Pin every source link to the analyzed commit.
- Trace the streaming HTTP request through LangGraph to the streamed result.
- Identify the incompatible call in `scripts/test_graph.py`.
- Report it as a test gap rather than a valid automated test.
- Keep tests outside the runtime execution chain.

### Failure conditions

- Summarizes only the README.
- Lists files without tracing code references.
- Links to `main` instead of the commit SHA.
- Claims that the stale script is a valid test.
- Exceeds the reading budget.

## Case 2: Go CLI with framework dispatch

Repository: https://github.com/charmbracelet/gum.git

Pinned revision: 4d089f95507708a71f64dacfe7ca513219dd5267

Mission: Trace what happens when a user runs `gum input`.

Reading budget: 15 minutes

### Expected behavior

- Produce 5–7 checkpoints totaling no more than 15 minutes.
- Trace `main`, Kong command registration, `input.Options.Run`, the Bubble Tea model, and stdout output.
- Label Kong's reflective dispatch as inference.
- Keep validation evidence outside the runtime route.
- Report that the `input` path lacks a direct repository-local Go test.
- Do not present `filter/filter_test.go` or `examples/input.tape` as a valid test for `gum input`.

### Failure conditions

- Treats `gum input` as a web request.
- Omits the connection between `Gum.Input` and `Options.Run`.
- Stops at command registration without reaching stdout.
- Claims the demo tape is an automated test.
- Exceeds the reading budget.