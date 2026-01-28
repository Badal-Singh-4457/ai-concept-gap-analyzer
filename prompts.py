GAP_ANALYSIS_PROMPT = """
You are an expert AI instructor.

Topic:
{topic}

Core concepts required for deep understanding:
{concepts}

User explanation:
{explanation}

Analyze the explanation and do the following:

1. List missing or weakly explained concepts
2. Detect shallow reasoning patterns (definition-only answers, buzzwords, lack of causal explanation)
3. Give a conceptual coverage score out of 100
4. Suggest how the explanation can be improved

Respond clearly using bullet points.
"""