# AI technical book writing

Use this reference for books about AI, machine learning, deep learning, LLM applications, Agents, evaluation, ML systems, or AI Infra. Load it after [book-writing.md](book-writing.md). When research, examples, figures, datasets, prompts, or third-party code are involved, [copyright-gate.md](copyright-gate.md) remains blocking.

This mode is for a technical book that should still be useful after a model release, API rename, or benchmark leaderboard changes. It combines teaching design, executable artifacts, empirical discipline, and an explicit maintenance horizon. It does not turn every book into a notebook collection or every chapter into the same template.

## Establish the AI book contract

Extend the ordinary book contract with:

- **Minimally qualified reader:** role, current knowledge, required mathematics and programming, production experience, and what the book must teach rather than assume.
- **Outcome ladder:** what the reader can explain, implement, evaluate, debug, and decide after each part.
- **System layer:** foundations, model internals, application engineering, Agents, evaluation, ML systems, AI Infra, or a named combination.
- **Durability horizon:** which ideas should remain useful for years and which instructions are a dated implementation snapshot.
- **Primary stack:** language, framework, model or provider class, local or hosted execution, and the policy for optional variants.
- **Resource envelope:** supported operating systems, hardware, memory, network, credentials, time, and expected monetary cost.
- **Evidence standard:** what requires a primary source, an independently run experiment, a dated product check, or an explicit author inference.
- **Safety and rights boundary:** privacy, security, model or dataset terms, code and media licenses, permitted quotation, and excluded uses.

State scope and non-scope early. A reader should know whether the book teaches transferable mechanisms, one working stack, production operations, research implementation, or a survey. Do not imply all of them when the book delivers only one.

## Design on two axes

### Learning progression

Prefer a progression the reader can execute:

1. build an intuition for the problem and its constraints;
2. expose the smallest mechanism that explains the behavior;
3. produce a runnable artifact with visible output;
4. measure the artifact against a baseline or acceptance criterion;
5. expand it into a system and explain the new tradeoffs;
6. identify failure modes, operational limits, and decisions the reader must still own.

Not every chapter needs all six stages, but the book as a whole must cover them. Do not jump from a friendly metaphor directly to a production recommendation.

### Content role

Give each chapter or major section a dominant role:

| Role | Reader need | Required result |
| --- | --- | --- |
| Tutorial | Learn by completing a guided path | A successful first implementation and a mental model |
| How-to | Accomplish a known task | A bounded procedure with prerequisites and verification |
| Explanation | Understand why a mechanism or tradeoff exists | A causal or conceptual model that supports decisions |
| Reference | Look up exact facts while working | Stable terminology, interfaces, parameters, and edge cases |

These roles may coexist in a book, but do not mix them invisibly inside one section. A tutorial should not become an exhaustive API catalogue; reference material should not pretend to be a learning path.

## Build a chapter contract

For a technical chapter, record only the fields that materially constrain it:

- entering reader question and required prior knowledge;
- observable outcome or decision the chapter enables;
- dominant content role and why it belongs at this point;
- mental model, mechanism, and terms introduced;
- runnable artifact, expected output, and verification method;
- evidence, experiment, diagram, or case study that earns the claims;
- failure modes, safety concerns, costs, and scope limits;
- dependencies on volatile APIs, models, datasets, prices, or policies;
- chapter snapshot date, last verification date, and rights-sensitive material.

A useful default rhythm is **problem → mechanism → artifact → evidence → tradeoff → decision**. Vary it when the subject demands a different path. Do not mechanically open every chapter with a story, close every chapter with a summary, or repeat the same list of rhetorical questions.

## Keep concept, code, mathematics, and output synchronized

### Concepts

- Introduce a term when the reader needs it, define it once, and use one name consistently.
- Explain the mechanism before presenting a taxonomy or framework comparison.
- Distinguish the model, the training or inference procedure, the application system, and the surrounding product. Do not use “AI” as an actor when a specific component acts.
- Use analogies to enter a concept, not to prove it. State where the analogy breaks.

### Code

- Make examples solve a meaningful reader task and progress from the smallest useful case to the system case.
- Run examples in a clean, documented environment. Pin material dependencies and identify exact model, dataset, API, and tool versions.
- Include prerequisites, setup, command, expected output, and a way to tell success from plausible-looking failure.
- Keep secrets, private data, unsafe defaults, and paid-resource assumptions out of copy-paste paths. Use explicit placeholders.
- Prefer code that can be copied or downloaded over screenshots of code. Explain only the lines that carry the idea.
- Test maintained examples. If an example is intentionally partial, pseudocode, expensive, nondeterministic, or unsupported on a platform, label that before the reader tries it.
- Preserve compatibility across a continuous project spine or provide explicit checkpoints and migration notes.

### Mathematics

An equation earns its place only when it improves explanation, implementation, or evaluation:

1. name the question it answers;
2. define every symbol and its shape, unit, or domain when relevant;
3. explain the intuition and assumptions;
4. connect it to code or a worked example;
5. test a boundary case or failure condition.

Do not hide a missing explanation behind notation, and do not remove useful mathematics merely to make the book appear accessible.

### Figures and outputs

- Give each diagram one main question to answer and a caption that states the takeaway.
- Follow [publishing-requirements.md](publishing-requirements.md) for the governing figure, table, equation, example, caption, callout, cross-reference, source-credit, and production-file rules.
- Use original or properly licensed figures. Record provenance and modification rights before drafting around them.
- Generate tables, charts, and computed values from the same executable source when practical.
- Show enough output to verify behavior, not pages of unexamined logs.
- Add alt text and avoid color-only distinctions.

When a technical方案, comparison, or example refers to an open-source project, load [open-source-book-sources.md](open-source-book-sources.md). Cite the project and relevant version, using an inspected commit only for implementation-specific claims. Treat code, documentation, screenshots, generated output, datasets, models, and project marks as separate rights scopes only when those materials are actually reused or distributed.

## Apply an evidence ladder

Classify load-bearing statements before polishing them:

| Statement | Minimum treatment |
| --- | --- |
| Durable mechanism or mathematical result | Primary or canonical source; define assumptions |
| Implementation fact | Current official documentation or inspected source code; record version |
| Empirical result | Reproducible experiment record, metric, baseline, and limitations |
| Provider or vendor claim | Attribute to the provider and keep it separate from independent evidence |
| Author observation | Name the environment and observation scope |
| Author inference | Show the evidence and reasoning; label the inference |
| Recommendation | State the workload, constraints, alternatives, and tradeoff that justify it |

Use precise verbs in the manuscript and review record:

- `documented`: an authoritative source states it;
- `observed`: the author saw it in a named environment;
- `reproduced`: an independent run matched the stated acceptance condition;
- `inferred`: evidence supports a conclusion but does not directly establish it;
- `recommended`: a decision under explicit constraints.

Never turn `documented` into `reproduced`, a single run into a general benchmark, or a current product limit into a timeless property.

## Record AI experiments

For any benchmark, model comparison, quality claim, latency claim, cost claim, or production recommendation, keep an experiment record with the relevant fields:

```yaml
question: ""
hypothesis: ""
snapshot_date: YYYY-MM-DD
model_and_version: ""
provider_or_runtime: ""
prompt_system_tools: ""
dataset_split_and_license: ""
environment_and_hardware: ""
parameters_seed_repeats: ""
metric_scorer_and_stopping_rule: ""
baseline: ""
raw_results: ""
variance_or_uncertainty: ""
latency_and_cost: ""
limitations_and_known_failures: ""
reproduction_command: ""
```

Not every field applies to every experiment. Mark non-applicable fields instead of silently omitting conditions that could change the result. Keep raw artifacts separate from narrative interpretation. A polished chart is not the underlying evidence.

## Design for version drift

Separate the manuscript into two maintenance speeds:

- **Durable core:** principles, mechanisms, tradeoffs, protocols, evaluation design, and decision frameworks. Write these without unnecessary product coupling.
- **Volatile edge:** model names, API shapes, SDK calls, UI steps, pricing, quotas, benchmark rankings, policy, and provider behavior. Date and version these explicitly.

Apply these controls:

- attach an “as of” date to price, quota, leaderboard, provider capability, and policy claims;
- record exact dependency versions, model identifiers, dataset revisions, hardware, and region where they affect behavior;
- avoid unnecessary version branches; when versions truly differ, tell the reader which path applies and verify each rendered path;
- keep a version matrix, errata path, last-verified marker, and runnable companion repository for volatile material when the project supports them;
- freeze released editions. Publish corrections as a named revision rather than silently changing the evidence behind an edition;
- never write “the best model” or “production-ready” without a dated workload, acceptance criteria, and comparison boundary.

The printed or frozen manuscript must still make sense if its companion service disappears. The companion may keep code current; it must not contain the missing reasoning that the book promised.

## Use 紫升风格 for the author's AI books

Load [style-zisheng.md](style-zisheng.md) and preserve its broader voice rules. For AI technical books specifically:

- lead with the engineering judgment the chapter will help the reader make;
- write peer-to-peer from a builder's perspective, without inventing first-hand use or production evidence;
- prefer one real system or project spine over disconnected toy snippets;
- follow explanations with inspectable artifacts: code, config, traces, evaluation records, diagrams, or decision tables;
- explain mechanisms before naming fashionable abstractions;
- keep established technical terms in English and explain them in natural Chinese at first use;
- distinguish verified fact, reproduced result, observation, inference, and personal recommendation in the prose itself;
- state operational costs and boundaries: latency, token use, compute, failure recovery, security, privacy, and maintenance;
- end substantial sections with a reusable judgment or next engineering action, not motivational filler.

Avoid:

- generic histories of AI that do not serve the reader's task;
- model leaderboard tourism and tool-name accumulation;
- API documentation rewritten as a chapter;
- anthropomorphism that obscures the actual component or control path;
- fake production stories, invented benchmarks, or implied access to systems the author did not inspect;
- copying a recognizable author's phrasing, chapter sequence, metaphors, exercises, or examples in order to “match the style.”

## AI technical review gates

Run these in addition to the ordinary book-level and copyright reviews:

| Gate | Pass condition |
| --- | --- |
| Reader | The minimally qualified reader, prerequisites, non-scope, and outcome ladder are explicit and consistent |
| Concept | Terms, mechanisms, abstractions, and mathematics agree across prose, code, diagrams, and glossary |
| Code | Maintained examples run from a clean documented environment or carry an explicit unsupported status |
| Evaluation | Claims name workload, baseline, metric, conditions, uncertainty, and limitations at the strength required |
| Drift | Volatile claims have snapshot dates and exact versions; durable explanations avoid unnecessary product coupling |
| Operations | Cost, latency, failure recovery, security, privacy, and resource assumptions are covered where relevant |
| Rights | Text, code, prompts, outputs, datasets, figures, and exercises have provenance and permitted use |
| Voice | The manuscript carries the author's judgments and cadence without copied expression or AI-generated filler |

`NEEDS_REVIEW` in Code, Evaluation, Drift, or Rights prevents an unconditional “publish-ready” claim. A book may be editorially complete while technical verification or rights clearance remains blocked; report those states separately.

## Publish-ready evidence

For an AI technical book, record:

- manuscript edition and technical snapshot date;
- clean-environment code or notebook result and the tested platform matrix;
- experiment records for load-bearing empirical claims;
- link, citation, figure, dataset, code-license, and copyright results;
- independent technical review scope, especially the critical reader path;
- known unsupported examples, stale sections, errata, and companion-repository status.

Add these fields to the book delivery record:

- 技术快照：edition, snapshot date, dependency/model matrix, and last verification
- 可执行性：tested scope, clean-environment result, and unsupported examples
- 实验复现：reproduced claims, unreproduced claims, and limitation count
- 技术审阅：reviewer or review method, sampled paths, and unresolved findings

Do not collapse manuscript completion, code execution, empirical reproduction, copyright clearance, publication, and live availability into one status.
