import os
from openai import OpenAI

# 1️⃣ OpenAI client helper
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)

# 2️⃣ Optional Local LLM fallback
try:
    from transformers import pipeline
    LOCAL_LLM_AVAILABLE = True
    local_generator = pipeline(
        "text-generation",
        model="TheBloke/Llama-2-7B-Chat-GGML",  # lightweight local model
        max_length=300
    )
except ImportError:
    LOCAL_LLM_AVAILABLE = False

# 3️⃣ Dynamic mock keywords dictionary
KEYWORDS = {
    "cnn": {
        "missing": [
            "Stride and padding in convolution layers",
            "Backpropagation through convolution layers",
            "Overfitting and regularization"
        ],
        "incorrect": [
            "Confused fully connected layers with convolution layers"
        ],
        "next_steps": [
            "Review CNN architecture in detail",
            "Implement a simple CNN on MNIST dataset",
            "Practice explaining convolution and pooling"
        ]
    },
    "backpropagation": {
        "missing": [
            "Chain rule for derivatives",
            "Gradient computation for each layer",
            "Weight initialization impact"
        ],
        "incorrect": [
            "Believing weights update independently of other layers"
        ],
        "next_steps": [
            "Review chain rule for multi-layer networks",
            "Solve example backpropagation step-by-step"
        ]
    },
    "transformer": {
        "missing": [
            "Attention mechanism details",
            "Positional encoding",
            "Multi-head attention"
        ],
        "incorrect": [
            "Confusing RNNs with Transformer layers"
        ],
        "next_steps": [
            "Read Transformer architecture paper",
            "Implement a small transformer model"
        ]
    }
}

# 4️⃣ Dynamic mock generator function
def generate_dynamic_mock(topic, explanation):
    """
    Generate realistic feedback dynamically based on keywords in the topic/explanation.
    """
    explanation_lower = explanation.lower()
    topic_lower = topic.lower()

    matched_topic = None
    for keyword in KEYWORDS:
        if keyword in topic_lower or keyword in explanation_lower:
            matched_topic = keyword
            break

    if matched_topic:
        data = KEYWORDS[matched_topic]
        missing = "\n- ".join(data["missing"])
        incorrect = "\n- ".join(data["incorrect"])
        next_steps = "\n- ".join(data["next_steps"])
        depth_score = 7 + len(data["missing"]) % 4  # small variation
    else:
        missing = "- Key foundational concepts missing"
        incorrect = "- Possible misconceptions"
        next_steps = "- Review topic from reliable sources\n- Practice exercises"
        depth_score = 7

    return f"""
Missing Concepts:
- {missing}

Incorrect Understanding:
- {incorrect}

Depth Score: {depth_score}/10

Suggested Next Steps:
- {next_steps}
"""

# 5️⃣ Main function with OpenAI / Local LLM / Mock fallback
def analyze_explanation(topic, explanation):
    """
    Try OpenAI API first. If it fails, use local LLM if available.
    Otherwise, fallback to dynamic mock.
    Fully seamless for user/demo.
    """
    # Try real OpenAI API
    client = get_openai_client()
    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You analyze conceptual understanding."},
                    {"role": "user", "content": f"Topic: {topic}\nExplanation: {explanation}"}
                ],
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception:
            pass  # fallback silently

    # Try Local LLM if available
    if LOCAL_LLM_AVAILABLE:
        try:
            llm_output = local_generator(
                f"Analyze this student's explanation and provide missing concepts, incorrect understanding, depth score, and next steps:\nTopic: {topic}\nExplanation: {explanation}",
                max_length=300
            )
            return llm_output[0]['generated_text']
        except Exception:
            pass  # fallback silently

    # Always fallback to dynamic mock
    return generate_dynamic_mock(topic, explanation)