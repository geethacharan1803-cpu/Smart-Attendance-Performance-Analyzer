"""
Enhanced Synthetic Dataset Generator
Generates realistic student records for BOTH Semester 1-1 and Semester 1-2 
with subject-wise marks, attendance, backlogs, and faculty remarks.
"""

import os
import csv
import random

# Semester 1-1 Subjects (Aug 4, 2025 – Jan 21, 2026)
SEM_1_1_SUBJECTS = [
    "Linear Algebra & Calculus",
    "C Programming",
    "Engineering Physics",
    "Engineering Graphics",
    "BEEE"
]

# Semester 1-2 Subjects (Jan 26, 2026 – Jul 9, 2026)
SEM_1_2_SUBJECTS = [
    "Differential Equations & Vector Calculus",
    "Python Programming",
    "Applied Chemistry",
    "Data Structures",
    "IT Workshop"
]

def generate_students():
    random.seed(42)

    first_names_female = [
        "Aaradhya", "Ananya", "Bhavya", "Charitha", "Deepika", "Divya", "Geethika", "Harini",
        "Ishwarya", "Javna", "Kavya", "Keerthi", "Lakshmi", "Manasa", "Meghana", "Navya",
        "Niharika", "Pooja", "Pranavi", "Priya", "Ramya", "Sai Tejaswi", "Sravani", "Sruthi",
        "Swathi", "Tanvi", "Trisha", "Vyshnavi", "Yamini", "Yashaswini"
    ]

    first_names_male = [
        "Abhinav", "Aditya", "Akhil", "Anil", "Aravind", "Bharath", "Chaitanya", "Charan",
        "Dinesh", "Ganesh", "Gopi", "Gowtham", "Harsha", "Kalyan", "Karthik", "Kiran",
        "Lokesh", "Manish", "Manoj", "Nikhil", "Pavan", "Praneeth", "Rahul", "Rajesh",
        "Rakesh", "Rohit", "Sai Kumar", "Sai Ram", "Sanjay", "Satish", "Shiva", "Srikanth",
        "Srinivas", "Subhash", "Sudheer", "Suresh", "Surya", "Teja", "Tarun", "Varun",
        "Venkatesh", "Vidyadhar", "Vijay", "Vikram", "Vinay", "Vishnu", "Vivek", "Yashwanth",
        "Yogesh", "Vamsi"
    ]

    surnames = [
        "Kotta", "Chintala", "Gudivada", "Bandaru", "Nallamothu", "Vissamraju", "Kondapalli",
        "Tummala", "Penumaka", "Mylavarapu", "Grandhi", "Alluri", "Pothuri", "Dornala",
        "Mekala", "Venkata", "Jonnalagadda", "Kamineni", "Bobbili", "Addanki", "Gorantla",
        "Kovvuri", "Mandava", "Pamarthi", "Yalamanchili", "Dendukuri", "Rayapati", "Golla"
    ]

    remarks_good = [
        "Excellent participation in lab sessions.",
        "Consistent performer with strong fundamentals.",
        "Proactive in class discussions.",
        "High assignment submission rate.",
        "Attentive and punctual."
    ]
    remarks_average = [
        "Satisfactory performance, needs minor focus on labs.",
        "Good theoretical understanding, practical application expanding.",
        "Average attendance, regular submission of assignments.",
        "Needs consistent effort in Mid examinations.",
        "Active participant, occasionally absent in early morning lectures."
    ]
    remarks_at_risk = [
        "Frequent absentee, struggles with lab experiments.",
        "Needs immediate counseling regarding backlog clearance.",
        "Low mid exam scores; requires remedial classes.",
        "Irregular attendance and delayed assignments.",
        "High risk of shortage of attendance; warning letter issued."
    ]

    students = []

    def make_student(index, name, gender, archetype):
        """Generate one student record with BOTH semester data."""
        # --- Semester 1-1 Data ---
        if archetype == "high":
            att_11 = round(random.uniform(82.0, 98.0), 1)
            mid1_11 = round(random.uniform(22.0, 29.5), 1)
            mid2_11 = round(random.uniform(23.0, 30.0), 1)
            external_11 = round(random.uniform(52.0, 68.0), 1)
            backlog_11 = 0
            lab_11 = "Completed"
            remark_11 = random.choice(remarks_good)
        elif archetype == "avg":
            att_11 = round(random.uniform(70.0, 84.5), 1)
            mid1_11 = round(random.uniform(16.0, 23.0), 1)
            mid2_11 = round(random.uniform(17.0, 24.0), 1)
            external_11 = round(random.uniform(38.0, 54.0), 1)
            backlog_11 = random.choices([0, 1], weights=[0.8, 0.2])[0]
            lab_11 = "Satisfactory" if backlog_11 == 0 else "Pending Review"
            remark_11 = random.choice(remarks_average)
        else:
            att_11 = round(random.uniform(50.0, 67.5), 1)
            mid1_11 = round(random.uniform(8.0, 16.0), 1)
            mid2_11 = round(random.uniform(9.0, 15.5), 1)
            external_11 = round(random.uniform(22.0, 37.0), 1)
            backlog_11 = random.choices([1, 2, 3, 4], weights=[0.35, 0.35, 0.2, 0.1])[0]
            lab_11 = "Needs Remedial"
            remark_11 = random.choice(remarks_at_risk)

        # --- Semester 1-2 Data (projected with realistic drift from Sem 1-1) ---
        drift = random.uniform(-5.0, 8.0) if archetype != "risk" else random.uniform(-8.0, 3.0)
        att_12 = round(max(40.0, min(100.0, att_11 + drift)), 1)

        drift_mid = random.uniform(-3.0, 4.0) if archetype != "risk" else random.uniform(-5.0, 2.0)
        mid1_12 = round(max(5.0, min(30.0, mid1_11 + drift_mid)), 1)
        mid2_12 = round(max(5.0, min(30.0, mid2_11 + drift_mid)), 1)
        external_12 = round(max(15.0, min(70.0, external_11 + drift * 0.6)), 1)

        backlog_change = random.choices([-1, 0, 1], weights=[0.3, 0.5, 0.2])[0]
        backlog_12 = max(0, min(4, backlog_11 + backlog_change))

        if backlog_12 == 0:
            lab_12 = "Completed"
            remark_12 = random.choice(remarks_good) if att_12 >= 75 else random.choice(remarks_average)
        elif backlog_12 <= 2:
            lab_12 = "Pending Review"
            remark_12 = random.choice(remarks_average)
        else:
            lab_12 = "Needs Remedial"
            remark_12 = random.choice(remarks_at_risk)

        roll_no = f"25331A05{index:02d}"

        return {
            "roll_no": roll_no,
            "name": name,
            "gender": gender,
            # Semester 1-1 columns
            "sem1_1_attendance_pct": att_11,
            "sem1_1_mid1": mid1_11,
            "sem1_1_mid2": mid2_11,
            "sem1_1_external": external_11,
            "sem1_1_backlog_count": backlog_11,
            "sem1_1_lab_status": lab_11,
            "sem1_1_remarks": remark_11,
            # Semester 1-2 columns
            "sem1_2_attendance_pct": att_12,
            "sem1_2_mid1": mid1_12,
            "sem1_2_mid2": mid2_12,
            "sem1_2_external": external_12,
            "sem1_2_backlog_count": backlog_12,
            "sem1_2_lab_status": lab_12,
            "sem1_2_remarks": remark_12,
        }

    # 30 Female students: 25331A0501 – 25331A0530
    for i in range(1, 31):
        name = f"{random.choice(surnames)} {first_names_female[i - 1]}"
        archetype = random.choices(["high", "avg", "risk"], weights=[0.45, 0.40, 0.15])[0]
        students.append(make_student(i, name, "Female", archetype))

    # 50 Male students: 25331A0531 – 25331A0580
    for i in range(31, 81):
        name = f"{random.choice(surnames)} {first_names_male[i - 31]}"
        archetype = random.choices(["high", "avg", "risk"], weights=[0.40, 0.42, 0.18])[0]
        students.append(make_student(i, name, "Male", archetype))

    return students


def write_csv():
    os.makedirs("sample_data", exist_ok=True)
    file_path = os.path.join("sample_data", "student_records.csv")
    students = generate_students()

    fieldnames = list(students[0].keys())

    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)

    print(f"Generated {len(students)} student records ({sum(1 for s in students if s['gender']=='Female')}F / "
          f"{sum(1 for s in students if s['gender']=='Male')}M) -> {file_path}")


if __name__ == "__main__":
    write_csv()
