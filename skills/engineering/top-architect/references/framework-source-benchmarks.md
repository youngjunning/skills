# Open-source framework architecture benchmarks

Use this reference for a framework-level decision or evolution review. It
distills ownership and delivery lessons from upstream source; it does not
prescribe their language, package manager, or release tooling.

## Review baseline

Reviewed on 2026-08-23. Re-pin revisions before relying on source details in a
later architecture decision.

| Project | Revision | Source boundary observed | Engineering observation | Transferable lesson |
| --- | --- | --- | --- | --- |
| React | `77ed3f545226ac9a834db7490a616b650c2a87a8` | `packages/` owns package surfaces; `scripts/release/` separates build, prerelease, and stable promotion. | A private workspace root owns one package-manager command surface; package manifests remain beside their source, while build, test, and release automation live under `scripts/`. | Test artifacts before promotion; source success is not release acceptance. |
| React Native | `091ac613cebafde540d9c1e56284d782029d3d35` | Shared packages isolate codegen, platform integration, dev middleware, and compatibility work. | Workspace globs deliberately distinguish `packages/` from `private/`; root commands expose build, formatting, API/type checks, and local-release tests as separate gates. | Consolidate cross-platform contracts in a shared core; migrate legacy paths through explicit compatibility boundaries. |
| Vite | `a98c8d95d552c6fa98ab66fb810f5b39ad5abf49` | Plugin hooks provide an ordered dev/build seam; a plugin can stay local until reuse is proven. | `pnpm-workspace.yaml` declares package, playground, test, and docs scopes separately; dependency overrides, patches, and install policy are auditable at the workspace root. | Expose a small lifecycle seam, keep ordering visible, and avoid promoting one-off integrations into packages. |
| Mastra | `7e8b78ae1cff7d26fde092ade94ddec9e68d4cb3` | CLI composition, commands, and services remain separate. | Package families use named directories by responsibility; shared dependency versions, patches, and install policy are explicit workspace configuration rather than implicit hoisting. | Keep command schema, orchestration, and domain services independently testable. |
| Deno | `98f9507affc905f088124891add3a8dd63b91f77` | Rust crates separate CLI, runtime, permissions, and support tooling. | Cargo workspace membership and root-level shared dependency policy make the build graph inspectable, while individual crates retain narrow ownership. | Make runtime authority and policy boundaries explicit; do not let convenience APIs bypass them. |

Primary sources: [React release scripts](https://github.com/react/react/tree/main/scripts/release), [React Native packages](https://github.com/react/react-native/tree/main/packages), [Vite plugin API](https://vite.dev/guide/api-plugin), [Mastra packages](https://github.com/mastra-ai/mastra/tree/main/packages), and [Deno CLI](https://github.com/denoland/deno/tree/main/cli).

## Framework decision matrix

For every proposed optimization, fill the smallest useful subset of this
matrix. Do not declare a project a reference merely because it uses the same
language or monorepo tool.

| Field | Evidence required |
| --- | --- |
| Local outcome | User or maintainer problem, affected workflow, and measurable completion condition. |
| Stable contract | Public package export, CLI command, schema, protocol, or lifecycle hook that consumers may rely on. |
| Private implementation | Code that may change without consumer migration, including generated source and build-only helpers. |
| Extension seam | Why a second implementation exists, its lifecycle/order, input/output contract, failure behavior, and ownership. |
| Delivery boundary | Source, build output, published artifact, installation, and target-client acceptance stated separately. |
| Adopted | Upstream ownership rule retained locally. |
| Adapted | Deliberate local deviation required by runtime, security, or delivery constraints. |
| Rejected | Tempting upstream pattern not used, with the concrete complexity or risk avoided. |
| Proof | Smallest test, build, tarball, contract, or native acceptance check that protects the risky assumption. |

## Engineering baseline

Use these rules to review framework engineering. They are intentionally
language-neutral; choose the local package manager and toolchain rather than
copying an upstream file tree.

| Concern | Decision to make | Minimum enforceable evidence |
| --- | --- | --- |
| Names | Product, repository, package, binary, config, and generated-file names are each owned and compatibility-sensitive names are recorded. | A name inventory plus a search/check for retired public names. |
| Workspace map | Every workspace is classified as public, private, tooling, fixture, example, docs, or evaluation; non-glob paths are explicit. | Manifest check rejects an unclassified or publishable auxiliary workspace. |
| Package manager | One manager owns install, lockfile, overrides, scripts, and publish policy for the repository boundary. | Pinned `packageManager`, committed lockfile, and no competing lockfile or unsupported installer path. |
| Dependencies | Shared versions, patches, overrides, and exceptions exist only for a concrete compatibility, security, or reproducibility reason. | Root policy documents the reason; package checks reject unpublished runtime dependencies and loose internal versions. |
| Layout | Public entrypoints, implementation, tests, fixtures, generated output, scripts, docs, and release automation have distinct homes. | Package allowlist/tarball check proves only intentional files ship. |
| Generated code | Generated source declares its generator, input, output, and regeneration check. Hand edits are either prohibited or explicitly owned. | Fresh generation or drift check passes in CI. |
| Commands | Bootstrap and local verification are discoverable; focused commands compose into CI/release gates. | A new contributor can run documented setup, lint, typecheck, targeted test, and package check without hidden CI-only steps. |
| Test taxonomy | Unit, contract, integration, end-to-end/native, and release checks state the boundary each proves. | CI report identifies the failing layer; a passing lower layer cannot substitute for a higher acceptance gate. |
| Release | Versioning, changelog, artifact construction, provenance, publish, install, and consumer acceptance are separate lifecycle states. | A release dry run or artifact install test validates the published surface. |

## pnpm workspace + Changesets release architecture

Use this combination when a pnpm monorepo needs an explicit package graph and a
reviewable release-intent workflow. The tools have different ownership; neither
one should silently absorb the repository's artifact or production-release
policy.

| Owner | Owns | Must not be treated as proof of |
| --- | --- | --- |
| pnpm workspace | Workspace discovery, local dependency resolution, one authoritative lockfile, install policy, and recursive command scope. | Which packages should change version, what belongs in a Changelog, or whether a package was published. |
| Changesets | Per-change release intent, SemVer bump calculation, internal dependency version updates, and package Changelog generation. | Tarball safety, registry credentials, successful upload, or consumer adoption. |
| Repository release command | Workspace/catalog completeness checks, build and package gates, publish order, registry adapter, immutable readback, retry behavior, and release evidence. | A Browser/Application artifact being signed, activated, installed, or accepted by a real client. |
| Consumer repository | Exact dependency adoption, lock update, compatibility checks, target build, and installed-client acceptance. | Upstream source or registry availability alone. |

The pnpm workspace is the package graph source of truth. If the repository also
keeps a workspace catalog for roles such as public, private, tooling, fixture,
or evaluation, validate that catalog against the actual workspace manifests.
A new package must fail release verification when it is unclassified; a
hand-maintained publish list must not silently omit it.

Choose the Changesets versioning mode from the product contract:

- Use a `fixed` group when the package set is one platform release unit. A
  change to one member advances every member to the same version, including
  unchanged members. Enable private-package versioning only when private
  workspaces must stay aligned without being published.
- Use independent versions when packages have genuinely separate compatibility
  and adoption cycles. Do not choose this merely to avoid publishing unchanged
  bytes.
- Use `linked` only when packages should share a version ceiling while retaining
  independent publication behavior. It is not a substitute for `fixed` when
  every package must be bumped and released together.

Keep the contributor and release commands distinct:

```bash
pnpm changeset
pnpm run release:packages
```

The first command records what changed, why it changed, and the required SemVer
bump in a commit-reviewable file. The root release command consumes pending
changesets, runs `changeset version`, refreshes the pnpm lock, verifies that all
fixed members and exact internal dependencies agree, then invokes the
repository's own package/security/registry pipeline. If an internal registry
requires a nonstandard client, signing, obfuscation, provenance, or cache
refresh, keep that adapter behind the root command instead of replacing the
version-and-Changelog workflow or bypassing it with direct per-package publish
commands.

Parallelize only stages whose outputs are independent. Package build, security
transformation, tarball construction, and local tarball verification may use a
bounded worker pool with one isolated output directory per package. Preserve the
release plan's stable result order, fail the whole gate when any worker fails,
and clean all temporary outputs. Registry upload, exact-version readback, cache
refresh, and dependent publication remain topologically ordered when a package
can depend on another package in the same release set.

For retryable publication, compare an existing registry object's exact version
and tarball integrity with the locally prepared artifact before skipping it.
An existing version with different bytes is a hard conflict. After registry
readback, still require clean consumer installation and target acceptance; a
fixed monorepo version identifies one package release set, not downstream
deployment or user adoption.

Primary references: [pnpm Workspaces](https://pnpm.io/workspaces),
[Changesets configuration](https://changesets.dev/guide/config), and
[Changesets add workflow](https://changesets.dev/faq#how-do-i-add-a-changeset).

## Complete framework engineering model

Use this model to avoid mistaking a tidy monorepo for a mature framework. A
dimension is actionable only when it has an owner, a supported promise, a
failure signal, and a proportionate check.

| Dimension | Framework question | Evidence or guardrail |
| --- | --- | --- |
| Product and naming | Which names are stable for users, code, packages, binaries, configuration, and generated output? Which legacy names remain compatibility-only? | Name inventory, deprecation/migration rule, and automated retired-name check. |
| Public API and compatibility | What is public, experimental, internal, or generated? How do exports, CLI flags, schemas, config, and errors evolve? | API surface test/snapshot, compatibility matrix, and documented removal policy. |
| Versioning and migration | What changes require a major/minor/patch release? Who owns migration data and rollback? | Version policy, migration fixture, upgrade and downgrade test where compatibility promises require it. |
| Workspace and package manager | Which workspaces are public/private/tooling/evaluation, and which resolver/lockfile is authoritative at each install boundary? | Manifest/lockfile policy and clean-install verification. |
| Dependency supply chain | Which dependency exceptions are permitted and why? How are integrity, age, patches, licenses, and vulnerabilities handled? | Auditable overrides/patches, SBOM or license gate where required, and dependency-update policy. |
| Source, generated code, and artifacts | Which files are authored, generated, vendored, or shipped? Can a fresh checkout reproduce them? | Generator ownership plus drift/tarball/provenance check. |
| Build and CI reproducibility | Does CI invoke the same focused commands as contributors, on pinned toolchains and relevant platforms? | Hermetic or documented-enough build inputs, cache-safe commands, CI matrix, and clean checkout run. |
| Test and quality strategy | Which unit, contract, integration, compatibility, end-to-end/native, fuzz, and release tests protect which risk? | Layered test map, deterministic fixtures, failure attribution, and no lower-layer claim substituted for consumer acceptance. |
| Diagnostics and observability | Can maintainers and consumers locate failures without source spelunking? | Stable errors/exit codes, structured logs/traces/metrics where runtime warrants them, redaction and support bundle policy. |
| Performance and resource budgets | Which startup, latency, binary size, memory, build time, and cost budgets are promised? | Representative benchmark, regression threshold, and profiling path tied to a user journey. |
| Platform and environment support | Which OS, architecture, runtime, shell, package manager, and deployment versions are supported or intentionally excluded? | Support matrix, automated target checks, and native acceptance on the target host. |
| Security and trust | Where are permissions, secrets, code execution, plugins, network access, artifact signing, and update trust anchored? | Threat model for risky boundaries, least-privilege defaults, secret scanning, signing/provenance and revocation/rotation procedure. |
| Documentation, examples, and migration UX | Can a new user choose, install, extend, diagnose, and upgrade without reading internals? | Executable quickstart/example, CLI help/API reference validation, and migration guide tested against a fixture. |
| Extensibility and ecosystem | Who can extend what, at which lifecycle, with which compatibility and security contract? | Small explicit SPI, extension conformance test, ownership/review policy, and deprecation path. |
| Governance and maintainer economics | Who owns modules, decisions, reviews, incident response, and backlog pruning? | CODEOWNERS/maintainer map or equivalent, ADR/review triggers, contribution policy, and dependency/module health signal. |
| License, compliance, and distribution | What can be redistributed, where, and under which notices, export, privacy, or internal-policy constraints? | License inventory, NOTICE/privacy review, and release eligibility gate. |
| Release, rollback, and consumer acceptance | How do source, build, artifact, registry, signing, rollout, rollback, and actual user upgrades progress? | Promotion record, rollback rehearsal where risk warrants it, and installed-consumer acceptance evidence. |

### Assessment rule

For a framework evolution, first score each dimension as **unproven risk**,
**known debt**, **adequate for current support promise**, or **out of scope**.
Improve only the highest-risk dimension that blocks the stated outcome. This
keeps the model a prioritization tool instead of a mandate to install every
enterprise process.

## FiaOS application order

For FiaOS or another framework with CLI, SDK, generated protocol code, and a
native consumer, optimize in this order:

1. Classify workspaces and protect public package/runtime dependency boundaries.
2. Verify published entrypoints and tarball contents before reorganizing code.
3. Make generated-protocol ownership and regeneration deterministic.
4. Consolidate contributor commands into focused, composable checks.
5. Only then reshape source directories or extension seams, backed by a real
   second consumer or a measured maintenance failure.

This order avoids a cosmetic reorganization that leaves installability,
provenance, or native-consumer acceptance unresolved.

## Rules of thumb

- A public package may consume another public package only through an exact,
  acyclic runtime dependency. It must not require an unpublished workspace at
  install time.
- Generated or private workspace code may support a public package only when
  the package build explicitly bundles it. Keep this exception narrow and
  machine-checked.
- Keep platform-neutral contracts in the framework. Product branding, release
  credentials, profiles, and acceptance remain with the consuming product.
- Add a plugin system only after at least two independently owned
  implementations need the same seam. Before that, a declared interface or a
  private adapter is usually cheaper and safer.
- Treat a framework change as incomplete until its boundary test proves both
  the intended path and the forbidden dependency or ownership path.
