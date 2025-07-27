import streamlit as st
from transformers import pipeline

# Load model once (cache)
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="tiiuae/falcon-7b-instruct", trust_remote_code=True)

generator = load_model()

# Field-to-skills map
FIELD_SKILLS = {
    "Data Science": ["Python", "Machine Learning", "SQL", "Statistics", "Pandas", "Deep Learning", "Scikit-learn", "NLP", "Data Visualization", "TensorFlow"],
    "UI/UX": ["Figma", "Wireframing", "User Research", "Prototyping", "Adobe XD", "Interaction Design", "Design Systems", "Accessibility", "Usability Testing", "Visual Design"],
    "Marketing": ["SEO", "Email Marketing", "Copywriting", "Social Media", "Google Ads", "Analytics", "Branding", "Content Strategy", "Market Research", "A/B Testing"],
    "Software Engineering": ["Java", "Python", "C++", "React", "Node.js", "Git", "APIs", "Docker", "Kubernetes", "Databases"],
    "Finance": ["Excel", "Financial Modeling", "Budgeting", "Forecasting", "Valuation", "Accounting", "Risk Analysis", "Investment Analysis", "QuickBooks", "Taxation"]
}

# --- Streamlit UI ---
st.title("🤖 AI LinkedIn Message Generator")

name = st.text_input("Your Name", placeholder="e.g. John Doe")
recipient = st.text_input("Recipient's Name (Optional)", placeholder="e.g. Sarah")
tone = st.radio("Select Tone", ["Casual", "Professional"])
field = st.selectbox("Your Field", list(FIELD_SKILLS.keys()))

# Show skills dynamically based on field
skills = st.multiselect("Select 3 Skills", FIELD_SKILLS[field], max_selections=3)

job_desc = st.text_area("Optional Job Description / Context", placeholder="Mention job context if reaching out for a role")

# Button to generate message
if st.button("✉️ Generate Message"):
    if not name or len(skills) != 3:
        st.warning("Please enter your name and select exactly 3 skills.")
    else:
        with st.spinner("Generating message..."):
            prompt = f"""
Write a LinkedIn message to {recipient or 'them'} from {name}, a {field} expert skilled in {', '.join(skills)}.
Tone: {"friendly and conversational" if tone == "Casual" else "professional and respectful"}.
{("Job context: " + job_desc) if job_desc else ""}

Guidelines:
- Begin with a personalized greeting
- Mention something specific or relevant
- Keep it under 100 words
- Close with a warm note
"""
            result = generator(prompt, max_length=200, temperature=0.7)
            st.subheader("📬 Generated Message")
            st.success(result[0]["generated_text"])
