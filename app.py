import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import re

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="🔧 Code Review Pro", layout="wide")
st.title("🔧 AI-Powered Code Review Assistant")

# -------------------------------
# Custom CSS for Modern UI
# -------------------------------
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stTextInput input, .stSelectbox select {
        border-radius: 8px;
    }
    .suggestion-box {
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid #4CAF50;
        background-color: #f1f8e9;
        color: black;
    }
    .critical {
        border-left-color: #EF5350;
        background-color: #ffebee;
    }
    .moderate {
        border-left-color: #FFA726;
        background-color: #fff3e0;
    }
    footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        color: gray;
        box-shadow: 0px -1px 5px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Sidebar Info
# -------------------------------
with st.sidebar:
    st.header("🧾 About This Tool")
    st.write("This tool analyzes your code, gives actionable suggestions, generates a better version, and helps you share insights.")
    st.info("Supported Languages: Python, JavaScript, C, C++, Java, Other")

    st.markdown("### 🧠 System Architecture")
    st.markdown("- **Knowledge Base**: Rules and best practices from coding standards.")
    st.markdown("- **Inference Engine**: Analyzes code using rules and heuristics.")
    st.markdown("- **Working Memory**: Stores current analysis state and findings.")

    st.markdown("---")
    st.markdown("### 💼 Developed By:")
    st.markdown("**Muhammad Shoban and Group**")

# -------------------------------
# Footer
# -------------------------------
st.markdown('<footer>Developed By: Muhammad Shoban and Group</footer>', unsafe_allow_html=True)

# -------------------------------
# Step 1: Organization Info
# -------------------------------
col1, col2 = st.columns(2)
with col1:
    org_name = st.text_input("🏢 Organization Name:")
with col2:
    client_range = st.slider("👥 Estimated Number of Clients:", 1, 10000)

# -------------------------------
# Step 2: Problem Description
# -------------------------------
problem_desc = st.text_area("📌 Describe the problem this code solves:", height=100)

# -------------------------------
# Step 3: Language Selection
# -------------------------------
language = st.selectbox("🌐 Select Programming Language", ["Python", "JavaScript", "C", "C++", "Java", "Other"])

# -------------------------------
# Step 4: Paste Code
# -------------------------------
code = st.text_area("📄 Paste your code here:", height=300)

# -------------------------------
# Analyze Button
# -------------------------------
if st.button("🔍 Analyze Code"):
    if not code.strip():
        st.warning("⚠️ Please paste some code to analyze.")
    else:
        with st.spinner("🧠 Analyzing your code..."):

            # Sample placeholders for dynamic data
            suggestions = []
            categories = []
            statuses = []
            better_code = ""
            total_issues = 0

            # Simple logic to detect potential issues in Python code
            if language == "Python":
                total_vars = len(re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\s*=", code))
                has_docstring = '"""' in code or "'''" in code
                has_main_guard = "if __name__ == '__main__':" in code
                uses_try = "try:" in code or "except" in code

                # Build suggestions dynamically
                if total_vars > 5 and not re.search(r"def\s", code):
                    suggestions.append("Refactor logic into functions for modularity.")
                    categories.append("Modularity")
                    statuses.append("Critical")
                else:
                    categories.append("Modularity")
                    statuses.append("Good")

                if not has_docstring:
                    suggestions.append("Add docstrings for clarity and documentation.")
                    categories.append("Documentation")
                    statuses.append("Moderate")
                else:
                    categories.append("Documentation")
                    statuses.append("Good")

                if not uses_try:
                    suggestions.append("Wrap critical sections in try-except blocks.")
                    categories.append("Error Handling")
                    statuses.append("Critical")

                if len(suggestions) < 3:
                    suggestions += [
                        "Use meaningful variable names instead of single letters.",
                        "Consider adding type hints for better readability.",
                        "Avoid hardcoded values; use constants or config files."
                    ]
                    categories += ["Naming", "Type Safety", "Hardcoding"]
                    statuses += ["Moderate", "Critical", "Critical"]

                # Improved Python function example
                better_code = '''def calculate_sum(num1: float, num2: float) -> float:
    """
    Calculate the sum of two numbers with validation.
    
    Args:
        num1 (float): First number
        num2 (float): Second number
    
    Returns:
        float: Sum of inputs
    """
    if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
        raise ValueError("Inputs must be numeric.")
    return num1 + num2

if __name__ == "__main__":
    try:
        result = calculate_sum(10, 20)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error occurred: {e}")
'''

            else:
                # Generic suggestions for other languages
                suggestions = [
                    "Improve naming conventions for variables/functions.",
                    "Break down large functions into reusable modules.",
                    "Add error handling for robustness.",
                ]
                categories = ["Naming", "Function Size", "Error Handling"]
                statuses = ["Moderate", "Critical", "Critical"]
                better_code = "// Refactored version would go here depending on language"

            # Store analysis results
            st.session_state['better_code'] = better_code
            st.session_state['suggestions'] = list(zip(categories, statuses, suggestions))

            # Pie chart logic
            labels = ['Good', 'Needs Improvement', 'Critical']
            good_count = statuses.count("Good")
            moderate_count = statuses.count("Moderate")
            critical_count = statuses.count("Critical")

            sizes = [good_count, moderate_count, critical_count]
            colors = ['#4CAF50', '#FFA726', '#EF5350']
            explode = (0, 0.1, 0.2)

            fig, ax = plt.subplots()
            ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                   autopct='%1.1f%%', shadow=True, startangle=140)
            ax.axis('equal')
            ax.set_title('Code Quality Breakdown')
            plt.savefig("pie_chart.png")
            plt.close()

            # Create DataFrame for CSV
            df = pd.DataFrame({
                "Category": [s[0] for s in st.session_state['suggestions']],
                "Severity": [s[1] for s in st.session_state['suggestions']],
                "Suggestion": [s[2] for s in st.session_state['suggestions']]
            })
            df.to_csv("code_analysis.csv", index=False)

            st.success("✅ Analysis Complete!")

# -------------------------------
# Display Results
# -------------------------------
if 'better_code' in st.session_state:
    st.markdown("### 📝 Code Suggestions")
    for i, (cat, level, sugg) in enumerate(st.session_state.suggestions, 1):
        box_class = "suggestion-box"
        if level == "Critical":
            box_class += " critical"
        elif level == "Moderate":
            box_class += " moderate"
        st.markdown(f'<div class="{box_class}"><strong>{i}. [{level}]</strong> {sugg}</div>', unsafe_allow_html=True)

    st.markdown("### 💡 Suggested Improved Code")
    st.code(st.session_state.better_code)

    st.markdown("### 📊 Code Quality Breakdown")
    st.image("pie_chart.png")

    col1, col2 = st.columns(2)
    with col1:
        with open("code_analysis.csv", "rb") as f:
            st.download_button("📥 Download CSV Report", f.read(), file_name="code_analysis.csv")
    with col2:
        with open("pie_chart.png", "rb") as f:
            st.download_button("📷 Download Pie Chart", f.read(), file_name="pie_chart.png")