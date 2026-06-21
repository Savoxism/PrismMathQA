# Opening
+ Introduce PrismMathQA as an agentic math tutor: it combines grounded examples, learner memory, exact symbolic verification, and an AVSD-trained reasoning model.
+ Main message: fluent explanations are not enough for math tutoring; the system needs correctness, step-by-step guidance, adaptation to the learner, and reliability checks.
+ Core principle: the LLM coordinates specialized support instead of solving every subproblem alone.

# Overall Framework
+ Explain the two-stage design from the framework slide.
+ Offline stage: AVSD trains the reasoning model using MetaMathQA-style math data and four privileged views: full solution, partial rationale, final answer, and concise hint.
+ Online stage: each tutoring turn uses RAG for grounding, memory for personalization, and tools for exact verification.
+ The final answer is still written by the reasoning model, but it is supported by retrieved examples, learner context, and tool outputs.
+ Speaking order: first describe the runtime tutor framework, then explain why fine-tuning is needed, then introduce AVSD as the training method.

# RAG Component
+ RAG is useful because math is pattern-sensitive: similar problems often share a strategy even when the wording is different.
+ Retrieved examples act as demonstrations, not answer lookups; the model still has to solve the student's exact question.
+ RAG helps especially on medium and hard problems where choosing the right representation is the hardest first step.

# Memory Component
+ Memory supports personalization: a student who wants step-by-step guidance should not receive the same answer as a student asking for quick verification.
+ Memory supports continuity: follow-up questions like "why did you divide by this term?" require the previous turn.
+ Memory supports accountability because the system can audit what context it used.
+ This is especially important in math because student mistakes are often systematic, such as sign errors, confusion between factoring and distribution, or misuse of rules.

# Tool Component
+ A reasoning LLM can explain a method correctly but still make a small arithmetic or symbolic error.
+ Tool calls create an audit trail, which helps distinguish model-only reasoning from answers supported by exact computation.
+ This audit trail is useful for debugging, evaluation, prompt design, and deciding whether future failures need better tools or better model training.

# Why Fine-Tuning Matters
+ RAG, memory, and tools improve grounding and reliability at runtime, but they do not automatically make the base model a better mathematical reasoner.
+ The model still needs to produce coherent reasoning trajectories before external support is applied.
+ Math errors are often local: one wrong sign, one invalid simplification, or one bad algebraic step can ruin the final answer.
+ A good training method should provide dense feedback at the token or step level, not only a final correct or incorrect signal.
+ This motivates self-distillation-style training, where the model learns from teacher distributions on its own generated prefixes.

# Why SFT Is Not Enough
+ SFT learns from static reference traces, but those traces may not match the model's own rollout distribution --> Training inference mismatch.
+ Static traces can overfit the model to one derivation path instead of teaching flexible mathematical behavior.

# Why Single-View Self-Distillation Is Not Enough
+ If the single teacher view contains privileged information unavailable at inference time, the model may learn tokens that depend on leakage rather than reasoning.

# AVSD Core Idea
+ Teacher mode then evaluates the same student prefixes under four privileged contexts: full solution, partial rationale, final answer, and concise hint.
+ AVSD does not trust any single view unconditionally.
+ It separates the shared signal across views from view-specific residual information.
+ The shared signal is treated as safer because multiple teacher contexts agree on it.
+ The view-specific residual can still help, but only when a gate decides it is aligned and not too large.
+ This gives dense token-level supervision while reducing the risk of one privileged view dominating.

# Consensus Target
+ Intuition: a token gets high consensus support only when it is supported across views.
+ This is conservative and represents intersection support.
+ If most views agree that a token should be suppressed, the consensus advantage is negative.
+ If most views agree that a token should be promoted, the consensus advantage is positive.
+ Presenter phrase: "Consensus is the safest part of the teacher signal because it is not tied to one annotation format."

# Arithmetic Target
+ Intuition: arithmetic mean captures union support, so a token can be helped by one strongly supportive view.
+ This can be useful because different views carry complementary information.
+ The risk is that arithmetic averaging can preserve artifacts from one privileged view.
+ A token might be promoted because one view saw information the student would not have at inference time.

# Alignment Component
+ The alignment component checks whether the per-view advantages point in the same direction.
+ It is high when teacher views mostly agree to promote or suppress the same token.
+ It is low when some views promote the token while others suppress it.
+ This prevents AVSD from treating direct teacher disagreement as reliable extra evidence.
+ Presenter phrase: "Alignment asks whether the teachers are telling the student to move in the same direction."

# Magnitude Component
+ The magnitude component checks whether residual support is proportionate to the consensus.
+ It is low when the residual is too large relative to the shared consensus signal.
+ This protects the update from being dominated by one privileged view.
+ Presenter phrase: "Magnitude asks whether the extra view-specific support is reasonable, or whether it is trying to overpower consensus."

# Closing
+ PrismMathQA turns a stateless answer generator into a tutoring framework that can ground, personalize, and verify mathematical reasoning.
+ RAG grounds answers in relevant solved examples.
+ Memory adapts the tutor across turns.
+ Tools provide exact computation when reliability matters.
+ AVSD strengthens the reasoning model before runtime support is applied.
+ The unifying idea is controlled support: use extra context, examples, and tools, but control how they influence the final answer.
