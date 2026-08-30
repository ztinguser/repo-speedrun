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

## Case 3: Python CLI with a prompted option

Repository: https://github.com/pallets/click.git

Pinned revision: 36baa15ff831b939a22bc527cd76ce653ef6f66d

Mission: Trace how the README `hello()` example parses its options, invokes the callback, and writes output.

Reading budget: 5 minutes

### Expected behavior

- Produce 3–4 checkpoints totaling no more than 5 minutes.
- Start the compact runtime route at the concrete `hello()` entry point.
- Trace `Command.__call__`, `Command.main`, context creation, argument parsing, `Command.invoke`, the user callback, and `click.echo`.
- Distinguish the command-line `--count` option from the prompted `--name` option.
- Pin every source link to the analyzed commit.
- Use one concise Markdown link for each source target.
- Use `test_basic_functionality` to explain normal execution and the `--help` early-exit behavior.
- Keep test evidence outside the runtime execution chain.

### Failure conditions

- Starts the compact runtime route at `parse_args` and omits the public entry or orchestration.
- Describes `name` as a positional argument.
- Splits one source description into adjacent links pointing to the same URL.
- Claims that `--help` executes the command callback.
- Stops before reaching stdout.
- Exceeds the reading budget.

## Case 4: Temporary clone lifecycle

Repository: https://github.com/pallets/click.git

Setup: Run without a matching local checkout or GitHub-aware repository tool so acquisition requires a fresh shallow clone in a system temporary directory.

Reading budget: 5 minutes

### Expected behavior

- Record that the clone was created by the current run and retain its exact resolved path.
- Complete repository analysis and construct commit-pinned source links before cleanup.
- Remove only the temporary clone created by the current run before returning the final speedrun.
- Preserve any user-provided repository or pre-existing checkout.
- Report the remaining path if cleanup cannot be completed safely.

### Failure conditions

- Leaves the temporary clone behind after a successful run without explanation.
- Deletes or modifies a user-provided repository or reused checkout.
- Attempts cleanup using a glob, unresolved variable, parent directory, workspace, home directory, or filesystem root.
- Removes the clone before the analysis and source-backed report are complete.
- Hides a cleanup failure or omits the remaining directory path.
