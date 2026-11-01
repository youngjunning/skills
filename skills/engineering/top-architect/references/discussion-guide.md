# Architecture discussion guide

Use this guide when the user wants to think together before choosing a design. The goal is to improve the model and the decision quality, not to win an argument or prolong the conversation.

## Opening turn

Start with a compact frame:

```text
【当前理解】我认为要解决的是……，最终可能需要决定……
【关键不确定性】目前最可能改变方向的是……
【暂定判断】在现有信息下，我倾向于……，但它依赖……
【反向检查】如果……成立，这个判断会失效
【下一问】为了继续判断，我只需要确认……
```

Do not ask for every requirement up front. Ask the smallest question that separates the plausible paths.

## Each discussion turn

1. Update the shared model with new facts, constraints, or user intent.
2. Mark each important statement as fact, assumption, hypothesis, preference, or open question.
3. Advance one decision axis: value, boundary, data, runtime, people, economics, risk, or change.
4. Present a concrete alternative, counterexample, or failure mode when it improves the discussion.
5. State what evidence would resolve the disagreement.
6. End with one next question, experiment, artifact to inspect, or provisional checkpoint.

Use this compact form when the conversation is moving quickly:

```text
【新增信息】
【模型变化】这会让……变得更重要 / 不再重要
【两个方向】A……；B……
【我的判断】暂时偏向……，因为……
【仍未解决】……
【下一步】确认…… / 验证…… / 查看……
```

## Productive disagreement

- Attack assumptions and consequences, not the people who hold them.
- Make the strongest case for the alternative before rejecting it.
- Separate “can be built” from “should be built” and “can be operated safely”.
- If the disagreement is about taste, expose the measurable consequence or label it as preference.
- If the disagreement cannot be resolved with current information, preserve both options and design the cheapest experiment that distinguishes them.

## Signals to converge

Move to decision mode when:

- the desired outcome and hard constraints are stable;
- the main alternatives and their tradeoffs are understood;
- the riskiest assumption has evidence or an explicitly accepted risk;
- the user asks to choose, write the ADR, or start implementation;
- further discussion would repeat known arguments without changing the decision.

Before closing, summarize the alternatives considered, the chosen boundary, unresolved risks, validation plan, owner, and review trigger. A provisional decision is valid when it names the evidence that can overturn it.
