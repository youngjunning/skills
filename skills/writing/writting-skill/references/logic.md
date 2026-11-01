# Logic and argumentation

Use this reference to make prose defensible without making it sound like a proof exercise. Apply the smallest amount of explicit logic the reader needs.

## 1. Build the argument unit

Treat every load-bearing passage as five possible parts:

| Part | Question |
| --- | --- |
| Claim | What exactly should the reader accept? |
| Premises and evidence | What observations, facts, definitions, or assumptions support it? |
| Warrant | Why do those premises count in favor of this conclusion? |
| Qualifier | How far does the conclusion reach, and with what confidence? |
| Counterpressure | What counterexample, tradeoff, objection, or alternative explanation survives? |

Not every paragraph needs all five parts. Every important conclusion must still have enough support for its strength.

Use this compact argument map before drafting or when a section feels persuasive but vague:

```text
Claim:
Claim type: descriptive | causal | predictive | evaluative | prescriptive
Premises/evidence:
Warrant:
Inference type:
Scope and confidence:
Strongest alternative or counterexample:
Result: keep | qualify | support | remove
```

## 2. Make propositions testable

- Keep key terms stable. If “quality” means visual polish in one paragraph and delivery reliability in another, split or define the term.
- Name scope and population. Replace “users prefer” with who, under what conditions, and based on what evidence.
- Expose quantifiers: all, none, most, many, some, one. Do not generalize beyond the observed set.
- Expose modality: must, will, likely, may, can. Match confidence to the evidence.
- Separate description from evaluation. “Usage increased” does not by itself mean the change was good.
- Separate evaluation from prescription. “X performs better” does not by itself prove “we should choose X”; cost, risk, timing, and objectives may change the decision.
- Distinguish necessary from sufficient conditions:
  - If A is necessary for B, B cannot occur without A; A alone may not produce B.
  - If A is sufficient for B, A guarantees B under the stated conditions; B may also arise another way.

## 3. Match the inference to the claim

### Deduction

The conclusion must follow if the premises are true. Check both validity and premise truth.

```text
If the release gate fails, publishing stops.
The release gate failed.
Therefore publishing stops.
```

Do not affirm the consequent: “If A, then B; B; therefore A.” B may have another cause. Do not deny the antecedent: “If A, then B; not A; therefore not B.” B may still occur another way.

### Induction

Observed cases support a broader conclusion with uncertainty. Check sample size, selection, representativeness, base rates, and exceptions. Use “suggests”, “in this sample”, or an explicit confidence level when universal language is not earned.

### Abduction

Infer the best current explanation from incomplete evidence. Compare plausible alternatives and state what new observation would distinguish them. Do not present the preferred hypothesis as an established cause.

### Analogy

Transfer a conclusion only when the compared cases share the properties that matter to that conclusion. Name the relevant similarity and the strongest disanalogy. Surface resemblance is not a warrant.

### Causal reasoning

Require more than sequence or correlation. Look for:

- temporal order;
- a plausible mechanism;
- dose, intervention, or repeated-pattern evidence when available;
- confounders and selection effects;
- reverse causality;
- competing explanations;
- evidence about what happens without the proposed cause.

If these are missing, describe an association or hypothesis rather than a proven cause.

## 4. Audit common failures

| Failure | Diagnostic question | Repair |
| --- | --- | --- |
| Unsupported premise | What source or agreed assumption establishes this? | Verify, cite, mark as assumption, or remove |
| Circular reasoning | Does the support merely restate the conclusion? | Add independent evidence or narrow the claim |
| Equivocation | Does a key word change meaning mid-argument? | Define or rename each sense |
| Hasty generalization | How many and which cases support the general claim? | Narrow scope or improve the sample |
| Cherry-picking | What relevant contrary evidence was excluded? | Include it and update confidence |
| False dilemma | Are there hybrids, delays, or third options? | Restore the real option set |
| Straw man | Would a serious opponent accept this summary? | State the strongest fair objection |
| Appeal to authority | Is the source relevant, current, and supplying evidence? | Cite the underlying evidence and scope |
| Correlation as causation | Could a confounder or reverse direction explain the result? | Use causal evidence or weaken the verb |
| Base-rate neglect | How common is the outcome before this evidence? | Include the prior rate or say it is unknown |
| Composition/division | Does a property of one part really transfer to the whole, or vice versa? | Supply the missing aggregation rule |
| Is–ought leap | Which value or objective connects the fact to the recommendation? | State the decision criterion explicitly |

Do not label a fallacy as a rhetorical win. Explain the exact inference failure and repair the passage.

## 5. Use logic by genre

- **Technical documentation:** express preconditions, action, observable result, failure condition, and recovery. Do not infer runtime behavior from source or build success alone.
- **Proposal or decision memo:** state objective, constraints, alternatives, criteria, evidence, tradeoffs, recommendation, and reversal conditions.
- **Analytical article:** separate observation, interpretation, causal claim, forecast, value judgment, and recommendation.
- **Product copy:** connect feature to user mechanism and benefit; do not turn capability into guaranteed outcome.
- **Personal essay:** personal experience can stand as experience. General claims about other people, markets, or causes still need support and scope.
- **Speech or narrative:** keep the argument structurally sound but allow evidence and warrants to appear through scenes, examples, and sequence rather than labels.

## 6. Preserve readable prose

- Keep formal notation in notes unless the audience needs it.
- Prefer one strong warrant over several weak reasons.
- Place qualifications next to the claim they limit, not in a distant disclaimer.
- Use a counterargument to change the conclusion, confidence, conditions, or decision—not as decorative balance.
- Do not flatten judgment into false neutrality. After testing the alternatives, make the strongest conclusion the evidence permits.

## Fast logic gate

- Is the central claim precise enough to be false?
- Are its premises factual, sourced, or explicitly assumed?
- Does the inference type match the wording of the conclusion?
- Are quantifiers, modality, and causal verbs earned?
- Are necessary and sufficient conditions distinguished?
- Has the strongest plausible alternative been tested?
- Did the counterargument change anything material?
- Would the conclusion survive without rhetorical emphasis?
