import streamlit as st
from transformers import pipeline

# ✅ Cache model so it loads only once
@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="google/flan-t5-small")

generator = load_model()

# ✅ Field-to-skills map
FIELD_SKILLS = {
    "Data Science": ["Python", "Machine Learning", "SQL", "Statistics", "Pandas", "Deep Learning", "Scikit-learn", "NLP", "Data Visualization", "TensorFlow"],
    "UI/UX": ["Figma", "Wireframing", "User Research", "Prototyping", "Adobe XD", "Interaction Design", "Design Systems", "Accessibility", "Usability Testing", "Visual Design"],
    "Marketing": ["SEO", "Email Marketing", "Copywriting", "Social Media", "Google Ads", "Analytics", "Branding", "Content Strategy", "Market Research", "A/B Testing"],
    "Software Engineering": ["Java", "Python", "C++", "React", "Node.js", "Git", "APIs", "Docker", "Kubernetes", "Databases"],
    "Finance": ["Excel", "Financial Modeling", "Budgeting", "Forecasting", "Valuation", "Accounting", "Risk Analysis", "Investment Analysis", "QuickBooks", "Taxation"]
}

# ✅ UI layout
st.set_page_config(page_title="AI LinkedIn Message Generator", page_icon="✉️")
st.title("🤖 AI LinkedIn Message Generator")
st.markdown("Generate short, personalized messages using your name, skills, and tone.")

name = st.text_input("Your Name", placeholder="e.g. John Doe")
recipient = st.text_input("Recipient's Name (Optional)", placeholder="e.g. Sarah")
tone = st.radio("Select Tone", ["Casual", "Professional"])
field = st.selectbox("Your Field", list(FIELD_SKILLS.keys()))
skills = st.multiselect("Select 3 Skills", FIELD_SKILLS[field], max_selections=3)
job_desc = st.text_area("Optional Job Description / Context", placeholder="Mention job or reason for reaching out")

# ✅ Generate message
if st.button("✉️ Generate Message"):
    if not name or len(skills) != 3:
        st.warning("Please enter your name and select exactly 3 skills.")
    else:
        with st.spinner("Generating message..."):
            # Prompt for flan-t5-base
            prompt = f"""
Write a short LinkedIn message to {recipient or 'a professional'} from {name}, a {field} expert skilled in {', '.join(skills)}.
Tone: {"friendly and informal" if tone == "Casual" else "professional and polite"}.
{("The message is about: " + job_desc) if job_desc else ""}

Guidelines:
- Use a personalized greeting
- Mention something specific
- Be under 100 words
- End warmly
"""
            output = generator(prompt, max_length=150, temperature=0.7)
            message = output[0]["generated_text"]

            # ✅ Display
            st.subheader("📬 Generated Message")
            st.success(message.strip())
