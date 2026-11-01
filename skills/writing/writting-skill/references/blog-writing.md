# Blog writing

Use Blog mode for a persistent, reader-facing single piece: a blog post, technical article, ATA, tutorial, opinion essay, project introduction, product article, or public long-form post. Use [book-writing.md](book-writing.md) instead when the work has a book contract, chapter system, or cross-chapter continuity.

Proposals, reports, product copy, speeches, and short transactional text can use the shared workflow in `SKILL.md` without being forced into Blog mode. They are utility deliverables, not a third publishing branch.

## Blog contract

Before drafting, establish:

- the intended reader and what they should understand, decide, or do;
- the central judgment or useful outcome;
- the publication surface, expected length, format, frontmatter, and asset constraints;
- the available facts, firsthand evidence, code, screenshots, measurements, and sources;
- the author position and selected voice profile;
- whether the task ends at a draft, repository change, build, or publication.

If a missing choice does not materially alter the result, make a reasonable assumption and proceed. Keep editorial workflow out of reader-facing prose unless it changes what the reader must know.

Before drafting or approving a Blog-mode artifact, run the mandatory [publication-value gate](publication-value.md). A polished article is not useful merely because its statements are correct: it must contribute a defensible judgment, evidence-bearing process, reusable mechanism, verified result, or clearly bounded lesson that the intended reader can take away.

### ATA Markdown title convention

For an ATA article stored as `<article title>.md`, treat the filename (without the `.md` suffix) as the article title. Start the file body with the opening paragraph or other first body content; do not add a duplicate `# <article title>` heading inside the file. Preserve or add an H1 only when the target ATA surface or repository explicitly requires one.

### ATA image publication

For an internal ATA under an approved work workspace, local cover and inline image references are intermediate authoring inputs, not a finished delivery state. After visual QA, automatically use the available `publish-internal-ata-assets` Skill to upload every local image reference, atomically replace the Markdown links with immutable CDN URLs, and perform HTTP readback of each uploaded object. Keep the local source assets and generation metadata. If the publisher, credentials, or HTTP verification is unavailable, report the ATA image delivery as blocked; do not describe local files or upload responses alone as a completed ATA handoff.

### ATA headline packaging

When the user asks to select topics, write, revise, audit or reverse-engineer an article specifically for the `ATA 头条` module, load [ata-headline.md](ata-headline.md). Apply its AI-and-business topic assessment before the headline-semantic and promise-parity gates, without extending these preferences to the separate `推荐`、`最新` or `最热` feeds or to other publications. Treat inferred selection signals as time-bound hypotheses rather than facts about ATA's internal algorithm.

## Article shapes

Choose the smallest shape that earns the article's conclusion.

### Technical analysis

Start from a real engineering problem or observed constraint, state the judgment early, explain the mechanism and evidence, then close with boundaries, tradeoffs, and a decision framework.

### Practice-led engineering explainer

Start from something the author actually built, configured, compared, broke, repaired, or changed their mind about. Extract the decision criteria hidden inside that experience before widening to a product category, architecture or industry trend. Pair each abstraction with an artifact or failure detail, separate firsthand observation from external evidence, and end with selective adoption guidance rather than asking the reader to copy the author's setup wholesale.

For a tool or product comparison, define what “good” means before listing candidates. Explain why rejected alternatives failed the stated criteria, provide a usable configuration or next step for the chosen path, and name the reader or scenario for which another option would still be better.

### Tutorial or how-to

State the end state and prerequisites, provide a reproducible path, explain only the mechanisms needed to make correct decisions, include verification and failure recovery, and separate version-specific behavior from durable principles.

### Comic article

Use [comic-articles.md](comic-articles.md) when scenes, recurring characters, and dialogue explain a mechanism or practical task. Keep the complete article and factual argument readable alongside the comic; plan panels from that argument. Use better-imagegen for scene artwork and the configured character roster for identity. This is a Blog article shape, not Book production or an image-only deliverable.

### Product or project introduction

Show the current user, visible product surface, representative task, and observable result before project history or architecture. Use the product-facing reality gate below.

For an annual review or multi-project portfolio, open with the business constraint and the small number of operating goals that connect the work. Select representative initiatives along a meaningful progression such as simple to complex, narrow to broad, or experiment to scaled operation. For each initiative, preserve the same proof loop: **why this problem -> constraints and options -> decision -> delivered capability -> scoped result -> remaining boundary**. Use the overview as a navigation hub and link detailed articles instead of compressing every implementation into one piece.

### Opinion or personal essay

Anchor the piece in an observed scene, decision, friction, failed approach, or changed judgment. Let the conclusion emerge from concrete experience and reasoning instead of generic significance claims.

## Product-facing reality gate

Apply this gate when the title or assignment promises to explain what a product is, what it looks like, how it works, or what it does for a user. Do not force it onto a history, architecture, ADR, or personal essay whose stated promise is different.

- Answer the product promise before giving the full history or conceptual model. In the opening, identify the current user, the visible product surface, and the first useful action they can take.
- Walk through one representative task from the user's action to the observable result. Introduce architecture and terminology only when they explain something the reader has already seen in that walkthrough.
- Verify current UI and behavior from actual screenshots, running product state, source, or maintained product documentation. Keep shipped, gray, disabled, planned, and illustrative states distinct. Label a concept image or mockup instead of presenting it as the live interface.
- If the reader still cannot picture the product or explain one normal use after the first section, treat the structure as concept-first and rebuild it.
- Split the piece when product introduction, project history, architecture, and personal reflection compete for the same opening. Keep the product article focused on surface, workflow, control, and current evidence; move the longer origin story or reflection into a companion article and link the two.
- After a split, retitle each piece to match its remaining promise.

Human voice comes from observed scenes, decisions, friction, failed approaches, and changed judgment. Adding first person, colloquial particles, or emotional adjectives to an abstract structure does not make it human. In Chinese exposition, reduce recoverable `我 / 我们 / 你 / 他 / 她 / 他们` and name the exact role or system when ownership matters. Keep natural pronouns inside prompts, dialogue, quotations, and UI copy; make the surrounding explanation more precise rather than equally conversational.

## Evidence and publication checks

- Verify load-bearing product, technical, historical, and quantitative claims from current sources or label them as inference.
- Keep shipped, tested, committed, pushed, deployed, and publicly available states distinct.
- For technical claims that may drift, record the version or verification date.
- Treat copied code, screenshots, diagrams, quotations, and third-party prose according to their licenses and permissions. A link or attribution does not replace permission.
- Remove private names, credentials, internal domains, account identifiers, unpublished metrics, and repository-only details from public prose unless explicitly approved.
- Validate frontmatter, links, assets, code blocks, and the rendered artifact when the publication system provides checks.
- Apply [article-cover.md](article-cover.md): every persistent article needs one explicit cover, and explanatory diagrams remain inline figures rather than cover substitutes.

### Local Markdown asset gate

When an article links local images, diagrams, downloads, or other files:

1. resolve each relative link from the article's final directory, not from the repository root or its previous location;
2. verify every target exists, is a regular readable file, and matches the expected file type;
3. check file permissions when previews, builders, or uploaders may run in another process or account; an asset readable only by its owner can still appear broken;
4. render or preview the final article when that path is available, and distinguish a stale preview from a broken current file;
5. repeat the check after any document or asset move, even when the literal relative link did not change.

Text inspection proves only that a link is present. Filesystem resolution proves the target is reachable from the source file. A successful render or publication smoke test is the evidence that the reader-facing path works.

## Blog delivery record

At handoff, state:

- article type, reader, and central judgment;
- facts verified and claims intentionally qualified;
- selected voice profile and whether the author's original voice was preserved;
- structural, logic, and AI-flavor changes;
- artifact path and actual publication state;
- unresolved facts, assets, permissions, or author decisions.
