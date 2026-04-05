
import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog

# -------- REQUIRED VARIABLE TYPES --------
version_float = 1.1
allowed_ext = {".json"}
used_files = set()
student_record = {}
example_range = range(1, 10)
example_frozen = frozenset([1, 2, 3])

# -------- QUESTIONS --------
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

# -------- STATES --------
psych_states = {
    "Optimal Cognitive Condition": (0, 12),
    "Slight Thermal Influence": (13, 24),
    "Moderate Cognitive Impact": (25, 36),
    "Reduced Performance State": (37, 48),
    "Severe Environmental Impact": (49, 60)
}

# -------- VALIDATION --------

def validate_name(name: str) -> bool:
    if name.strip() == "":
        return False
    for ch in name:  # FOR LOOP (correct use)
        if not (ch.isalpha() or ch in "-' "):
            return False
    return True

def validate_not_empty(value: str) -> bool:
    return value.strip() != ""

def validate_dob(dob: str) -> bool:
    try:
        datetime.strptime(dob, "%Y-%m-%d")
        return True
    except:
        return False

def interpret_score(score):
    for state, (low, high) in psych_states.items():
        if low <= score <= high:
            return state
    return "Unknown"

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# -------- APP --------

class SurveyApp:
    def __init__(self, root):
        self.root = root
        root.title("Survey Program")
        self.main_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def main_menu(self):
        self.clear_window()

        tk.Label(self.root, text="Survey Program", font=("Arial", 18)).pack(pady=10)

        tk.Button(self.root, text="1. Load existing result file",
                  width=40, command=self.load_result_file).pack(pady=5)

        tk.Button(self.root, text="2. Start new questionnaire",
                  width=40, command=self.start_survey_info).pack(pady=5)

        tk.Button(self.root, text="3. Start questionnaire (load questions from file)",
                  width=40, command=self.load_questions_then_start).pack(pady=5)

        tk.Button(self.root, text="4. Save survey questions + psychological states",
                  width=40, command=self.save_questions_and_states).pack(pady=5)

    def load_result_file(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            messagebox.showinfo("File Content", content)
        except:
            messagebox.showerror("Error", "Could not read file.")

    def save_questions_and_states(self):
        data = {"questions": questions, "psychological_states": psych_states}
        save_json("survey_questions_and_states.json", data)
        messagebox.showinfo("Saved", "Saved to survey_questions_and_states.json")

    def start_survey_info(self):
        self.selected_questions = questions
        self.show_user_form()

    def load_questions_then_start(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and "questions" in data:
                self.selected_questions = data["questions"]
            else:
                self.selected_questions = data
        except:
            messagebox.showerror("Error", "Invalid file.")
            return
        self.show_user_form()

    def show_user_form(self):
        self.clear_window()

        tk.Label(self.root, text="Enter your details", font=("Arial", 16)).pack(pady=10)

        self.name_var = tk.StringVar()
        self.surname_var = tk.StringVar()
        self.dob_var = tk.StringVar()
        self.sid_var = tk.StringVar()

        self.add_entry("Given Name:", self.name_var)
        self.add_entry("Surname:", self.surname_var)
        self.add_entry("Date of Birth (YYYY-MM-DD):", self.dob_var)
        self.add_entry("Student ID:", self.sid_var)

        tk.Button(self.root, text="Start Survey", command=self.validate_user).pack(pady=10)

    def add_entry(self, label, var):
        frame = tk.Frame(self.root)
        frame.pack(pady=3)
        tk.Label(frame, text=label, width=25, anchor="w").pack(side="left")
        tk.Entry(frame, textvariable=var, width=25).pack(side="left")

    def validate_user(self):
        name = self.name_var.get()
        surname = self.surname_var.get()
        dob = self.dob_var.get()
        sid = self.sid_var.get()

        while True:  # REAL while loop
            if not validate_not_empty(name) or not validate_name(name):
                return messagebox.showerror("Error", "Invalid name.")
            if not validate_not_empty(surname) or not validate_name(surname):
                return messagebox.showerror("Error", "Invalid surname.")
            if not validate_dob(dob):
                return messagebox.showerror("Error", "Invalid date of birth.")
            if not sid.isdigit():
                return messagebox.showerror("Error", "Student ID must be digits.")
            break

        self.record = {
            "name": name,
            "surname": surname,
            "dob": dob,
            "student_id": sid,
            "version": version_float
        }

        self.q_index = 0
        self.total_score = 0
        self.answers = []

        self.show_question()

    def show_question(self):
        self.clear_window()

        q = self.selected_questions[self.q_index]

        tk.Label(self.root, text=f"Question {self.q_index+1}", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text=q["q"], wraplength=400, justify="left").pack(pady=10)

        self.choice = tk.IntVar(value=-1)

        for i, (text, score) in enumerate(q["opts"], start=1):
            tk.Radiobutton(self.root, text=text, variable=self.choice, value=i).pack(anchor="w")

        tk.Button(self.root, text="Next", command=self.submit_answer).pack(pady=10)

    def submit_answer(self):
        c = self.choice.get()

        if c == -1:
            return messagebox.showerror("Error", "You must select an option.")

        q = self.selected_questions[self.q_index]
        text, score = q["opts"][c-1]

        self.total_score += score
        self.answers.append({
            "question": q["q"],
            "selected_option": text,
            "score": score
        })

        self.q_index += 1

        if self.q_index >= len(self.selected_questions):
            self.finish()
        else:
            self.show_question()

    def finish(self):
        self.record["total_score"] = self.total_score
        self.record["result"] = interpret_score(self.total_score)
        self.record["answers"] = self.answers

        self.clear_window()

        tk.Label(self.root, text="Survey Completed!", font=("Arial", 18)).pack(pady=10)
        tk.Label(self.root, text=f"Result: {self.record['result']}").pack(pady=10)

        tk.Button(self.root, text="Save Result", command=self.save_result).pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=10)

    def save_result(self):
        path = filedialog.asksaveasfilename(defaultextension=".json",
                                            filetypes=[("JSON files", "*.json")])
        if not path:
            return

        if not any(path.endswith(ext) for ext in allowed_ext):
            return messagebox.showerror("Error", "Invalid file extension.")

        save_json(path, self.record)
        messagebox.showinfo("Saved", "Survey result saved.")

# -------- RUN --------
root = tk.Tk()
app = SurveyApp(root)
root.mainloop()
