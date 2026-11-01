# Publication-value gate

Use this gate for every Blog-mode artifact, including ATA, technical articles, tutorials, product or project introductions, opinion essays, and persistent reader-facing posts. Run it before polishing and repeat it before delivery. This gate asks whether the piece contains a contribution worth publishing; `deslop.md` separately checks whether that contribution is expressed without generated-looking padding.

The gate is blocking. Do not rescue a low-value draft by expanding it, adding formatting, increasing technical vocabulary, or polishing its tone. Narrow the promise, obtain the missing evidence, convert it to a more appropriate format, or stop at an outline that names what is still missing.

## Establish the contribution

State in one sentence what the reader gains that is not already available from a generic search result, tool transcript, slide deck, or product announcement. A publishable article should contribute at least one of these:

- a firsthand problem, constraint, failed path, or decision trail;
- a mechanism explained clearly enough to apply or challenge;
- a reproducible method, artifact, configuration, or verification path;
- a measured or observed result with its baseline, scope, actor, time window, and caveat;
- a comparison whose criteria explain both the choice and the rejected alternatives;
- a synthesis or judgment that names its premises, evidence, limits, and consequence.

A topic, tool name, generated output, screenshot collection, or broad conclusion is not a contribution by itself.

## AI-relevance counterfactual

For an article that foregrounds AI, Agent, MCP, RAG, model names, or another current trend, mentally remove the trend terms from the title and thesis.

- If the argument remains unchanged, the trend label is probably decorative. Retitle the piece around its actual subject or add the missing AI-specific mechanism and evidence.
- If the article collapses to “the tool can do this,” it still lacks a contribution. Add what was hard, what changed, how the result was verified, where it failed, and what another practitioner can reuse.
- If the technology materially changes the constraints, decision, workflow, failure mode, economics, or result, make that causal role explicit rather than relying on terminology density.

Do not force a legitimate non-AI topic into an AI frame. Do not reject an article merely because it does not discuss AI.

## Four low-value patterns

### Concept transport

The draft rearranges definitions, acronyms, public documentation, or fashionable concepts without a new model, comparison, example, decision, or application boundary.

Repair it by anchoring the explanation in a question the source material does not already answer, then add a worked mechanism, counterexample, decision framework, or independently verified synthesis. If no such contribution exists, use a short reference note instead of an article.

### Wrapper demo

The draft runs an existing tool through a familiar task, pastes prompts or screenshots, and declares that efficiency or quality improved.

Require the original workflow, comparison baseline, affected role, measurement method, observed result, failure cases, and verification source. A successful model answer, tool call, demo, or screenshot proves only that the example occurred; it does not prove adoption, reliability, business impact, or scale.

### Slide expansion

The draft turns a presentation, workshop, meeting record, or feature inventory into paragraphs without adding reasoning. Each sentence may be true while the whole article gives the reader no process, evidence, or decision.

Rebuild around one load-bearing question. Keep only material that supplies context, evidence, mechanism, tradeoff, or consequence. If the slides already carry the full value, publish or annotate the slides instead of manufacturing article length.

### Trend forcing

The title or opening attaches a fashionable technology to a subject whose actual problem, method, and conclusion do not depend on it.

Retitle and retag the piece around the real subject. Keep the technology only where it changes a verified fact or a decision. Never add trend language merely to improve discoverability, perceived novelty, or organizational relevance.

## Evidence loop

For a practice, project, product, or engineering article, the smallest credible loop is:

1. **Problem:** who encountered what concrete friction, in which scope;
2. **Constraint:** what made the obvious path insufficient;
3. **Decision or action:** what the author or team actually tried, chose, changed, or rejected;
4. **Evidence:** what artifact, observation, baseline comparison, or source supports the result;
5. **Boundary:** what remains unverified, local, gray, planned, costly, or scenario-specific;
6. **Transfer:** what another reader can decide, reproduce, avoid, or inspect next.

Not every article needs these as headings, but the reasoning must be recoverable from the prose. Tutorials may express the loop as prerequisites, steps, verification, failure recovery, and version boundary. Opinion essays may use an observed case, premises, counterpressure, judgment, and implication.

## Signals that do not prove value

Do not use these as substitutes for content evidence:

- article length, heading count, table count, screenshot count, or Markdown density;
- likes, praise, team-internal comments, or circulation inside the author's own group;
- a dense list of metrics without definitions, comparable baselines, or a decision they support;
- a popular blog post, social-media screenshot, or vendor claim presented as established fact;
- “initial validation,” “significant improvement,” or similar language without the tested scope and actual observation;
- novelty that comes only from combining fashionable terms.

Engagement data may describe distribution or reader response when its population and limitations are clear. It does not establish technical correctness or practical usefulness.

## Final test

Before delivery, answer:

- What exact sentence states the article's contribution?
- Which section shows firsthand process, independent reasoning, reusable mechanism, or decision-bearing evidence?
- Can the reader distinguish observed facts, external claims, inference, and recommendation?
- Does every impact claim include the affected actor, baseline or prior state, measured or observable change, and scope?
- Does each section add a fact, mechanism, comparison, boundary, or decision rather than restating the thesis?
- After removing formatting and trend vocabulary, does the contribution remain?
- Can the intended reader name one thing to apply, verify, avoid, or decide after reading?

Classify the result:

- `pass`: the article has a clear contribution and an evidence-bearing path to it;
- `revise`: the contribution is plausible but missing process, evidence, boundaries, or transfer value;
- `wrong format`: the material belongs as a slide deck, reference note, changelog, demo, discussion post, or internal update rather than a long article;
- `block`: the title or conclusion claims value that the available material cannot support.

Keep the disposition as an internal gate. Report `revise`, `wrong format`, or `block` only when it changes the requested delivery; do not append a default process summary or invent a numeric value score.
