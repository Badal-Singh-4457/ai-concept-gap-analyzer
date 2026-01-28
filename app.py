import streamlit as st
from analyzer import analyze_explanation
from concept_maps import CONCEPT_MAPS

st.set_page_config(page_title="Concept Gap Analyzer")

st.title("🧠 Conceptual Gap Analyzer")
st.write("This tool evaluates how deeply you understand a concept.")

topic = st.selectbox(
    "Select a topic",
    list(CONCEPT_MAPS.keys())
)

explanation = st.text_area(
    "Explain the concept in your own words:",
    height=200
)

if st.button("Analyze Understanding"):
    if explanation.strip() == "":
        st.warning("Please enter an explanation.")
    else:
        with st.spinner("Analyzing conceptual depth..."):
            result = analyze_explanation(topic, explanation)

        st.subheader("📊 Analysis Result")
        st.write(result)