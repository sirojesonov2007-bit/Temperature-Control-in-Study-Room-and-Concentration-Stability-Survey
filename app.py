import streamlit as st
import json
from datetime import datetime

# ---------------- DATA ----------------
version_float = 1.1

questions = [
    {"q": "1. How often does the temperature of your study environment reduce your overall mental efficiency?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "2. How would you rate your thinking clarity in a warm room?",
     "opts": [("Very clear",0),("Clear",1),("Slightly unclear",2),("Unclear",3),("Very unclear",4)]},
    {"q": "3. How does a cooler study environment affect your alertness and focus?",
     "opts": [("Greatly improves alertness",0),("Slightly improves",1),("No change",2),("Slightly reduces",3),("Strongly reduces",4)]},
    {"q": "4. How often do sudden temperature changes interrupt your concentration?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "5. How sensitive are you to temperature when performing mentally demanding tasks?",
     "opts": [("Not sensitive",0),("Slightly sensitive",1),("Moderately sensitive",2),("Highly sensitive",3),("Extremely sensitive",4)]},
    {"q": "6. How often does room temperature affect your ability to finish tasks on time?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "7. How stable is your attention span when the temperature is uncomfortable?",
     "opts": [("Very stable",0),("Stable",1),("Slightly unstable",2),("Unstable",3),("Very unstable",4)]},
    {"q": "8. How frequently do you feel physical discomfort (heat, cold, sweating, shivering) while studying?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "9. How does temperature affect your reaction speed when thinking or answering questions?",
     "opts": [("Improves it",0),("Slightly improves",1),("No effect",2),("Slightly slows",3),("Strongly slows",4)]},
    {"q": "10. How often do you experience fatigue due to an uncomfortable study temperature?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "11. How effective are you at maintaining focus in a warm environment?",
     "opts": [("Very effective",0),("Effective",1),("Neutral",2),("Ineffective",3),("Very ineffective",4)]},
    {"q": "12. How frequently do you adjust your study environment (fan, AC, window, clothing) to improve focus?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    {"q": "13. How much does the study room temperature influence your overall learning productivity?",
     "opts": [("No influence",0),("Slight influence",1),("Moderate influence",2),("Strong influence",3),("Extreme influence",4)]},
    {"q": "14. How well can you adapt to uncomfortable temperatures while studying?",
     "opts": [("Very well",0),("Well",1),("Moderately",2),("Poorly",3),("Very poorly",4)]},
    {"q": "15. How would you describe your overall cognitive performance in your usual study environment?",
     "opts": [("Excellent",0),("Good",1),("Average",2),("Below average",3),("Poor",4)]}
]

psych_states = {
    "Optimal Cognitive Condition": (0, 12),
    "Slight Thermal Influence": (13, 24),
    "Moderate Cognitive Impact": (25, 36),
    "Reduced Performance State": (37, 48),
    "Severe Environmental Impact": (49, 60)
}

# ---------------- HELPERS ----------------
def validate_name(name: str) -> bool:
    return len(name.strip()) > 0 and not any(c.isdigit() for c in name)

def validate_dob(dob: str) -> bool:
    try:
        datetime.strptime(dob, "%Y-%m-%d")
        return True
    except:
        return False

def interpret_score(score: int) -> str:
    for state, (low, high) in psych_states.items():
        if low <= score <= high:
            return state
    return "Unknown"

def save_json(filename: str, data: dict):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ---------------- STREAMLIT APP ----------------
st.set_page_config(page_title="Temperature Effect Survey")
st.title("📝 Temperature Effect Survey")
st.info("Please fill out your details and answer all questions honestly.")

# --- User Info ---
if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(questions)
if "total_score" not in st.session_state:
    st.session_state.total_score = None
if "submitted" not in st.session_state:
    st.session_state.submitted = False

name = st.text_input("Given Name", key="name")
surname = st.text_input("Surname", key="surname")
dob = st.text_input("Date of Birth (YYYY-MM-DD)", key="dob")
sid = st.text_input("Student ID (digits only)", key="sid")

# --- Start Survey ---
if st.button("Start Survey") and not st.session_state.submitted:

    errors = []
    if not validate_name(name):
        errors.append("Invalid given name.")
    if not validate_name(surname):
        errors.append("Invalid surname.")
    if not validate_dob(dob):
        errors.append("Invalid date of birth format. Use YYYY-MM-DD.")
    if not sid.isdigit():
        errors.append("Student ID must be digits only.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        st.success("All inputs are valid. Proceed to answer the questions below.")

        # --- Display Questions ---
        for idx, q in enumerate(questions):
            opt_labels = [opt[0] for opt in q["opts"]]
            choice = st.selectbox(f"Q{idx+1}. {q['q']}", opt_labels, key=f"q{idx}")
            st.session_state.answers[idx] = choice

        # --- Compute total score ---
        total_score = sum(next(score for label, score in q["opts"] if label == st.session_state.answers[i])
                          for i, q in enumerate(questions))
        st.session_state.total_score = total_score
        st.session_state.submitted = True

# --- Show Results ---
if st.session_state.submitted:
    status = interpret_score(st.session_state.total_score)
    st.markdown(f"## ✅ Your Result: {status}")
    st.markdown(f"**Total Score:** {st.session_state.total_score}")

    record = {
        "name": name,
        "surname": surname,
        "dob": dob,
        "student_id": sid,
        "total_score": st.session_state.total_score,
        "result": status,
        "answers": [{"question": q["q"], "selected_option": st.session_state.answers[i],
                     "score": next(score for label, score in q["opts"] if label == st.session_state.answers[i])}
                    for i, q in enumerate(questions)],
        "version": version_float
    }

    json_filename = f"{sid}_result.json"
    save_json(json_filename, record)
    st.success(f"Your results are saved as {json_filename}")
    st.download_button("Download your result JSON", json.dumps(record, indent=2), file_name=json_filename)
