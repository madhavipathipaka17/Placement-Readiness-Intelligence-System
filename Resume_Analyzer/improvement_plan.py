# improvement_plan.py

def generate_improvement_plan(skill_gap):

    matched_skills = skill_gap.get("matched_skills", [])
    missing_skills = skill_gap.get("missing_skills", [])
    critical_missing = skill_gap.get("critical_missing_skills", [])
    optional_missing = skill_gap.get("optional_missing_skills", [])
    learn_first = skill_gap.get("skills_to_learn_first", [])

    # ---------------- Resume Suggestions ----------------

    resume_suggestions = []

    if len(missing_skills) > 0:
        resume_suggestions.append(
            "Customize your resume according to the Job Description."
        )

    if len(matched_skills) < 5:
        resume_suggestions.append(
            "Highlight more relevant technical skills."
        )

    if len(critical_missing) > 0:
        resume_suggestions.append(
            "Mention projects demonstrating the critical skills."
        )

    resume_suggestions.extend([
        "Quantify project achievements using numbers.",
        "Add GitHub and LinkedIn profile links.",
        "Use ATS-friendly resume format.",
        "Keep resume within one page.",
        "Include certifications relevant to the role."
    ])

    # ---------------- Job Preparation Suggestions ----------------

    job_preparation = []

    if critical_missing:

        for skill in critical_missing:
            job_preparation.append(
                f"Learn {skill.title()} before applying."
            )

    else:

        job_preparation.append(
            "Revise your existing skills thoroughly."
        )

    job_preparation.extend([
        "Practice Data Structures and Algorithms.",
        "Solve coding problems daily.",
        "Prepare HR interview answers.",
        "Revise OOP concepts.",
        "Practice SQL queries.",
        "Study System Design basics.",
        "Prepare project explanations."
    ])

    # ---------------- 7 Day Plan ----------------

    seven_day_plan = {

        "Day 1": [
            "Update Resume",
            "Optimize LinkedIn",
            "Organize GitHub"
        ],

        "Day 2": [
            "Learn Top Critical Skill",
            "Watch Tutorials",
            "Take Notes"
        ],

        "Day 3": [
            "Build Mini Project",
            "Upload to GitHub"
        ],

        "Day 4": [
            "Practice SQL",
            "Practice Python",
            "Solve Easy Coding Questions"
        ],

        "Day 5": [
            "Revise Machine Learning",
            "Revise Statistics",
            "Read Interview Questions"
        ],

        "Day 6": [
            "Mock Interview",
            "Explain Resume",
            "Explain Projects"
        ],

        "Day 7": [
            "Apply for Jobs",
            "Improve Weak Areas",
            "Review Entire Preparation"
        ]
    }

    # ---------------- 30 Day Plan ----------------

    month_plan = {

        "Week 1": [
            "Master Critical Skills",
            "Improve Resume",
            "Practice Coding Daily"
        ],

        "Week 2": [
            "Complete One Major Project",
            "Upload to GitHub",
            "Improve Documentation"
        ],

        "Week 3": [
            "Practice Aptitude",
            "SQL",
            "Machine Learning",
            "Mock Interviews"
        ],

        "Week 4": [
            "Apply for Companies",
            "Daily Revision",
            "Interview Practice",
            "Resume Customization"
        ]
    }

    # ---------------- Final Result ----------------

    return {

        "resume_improvement_suggestions":
            resume_suggestions,

        "job_preparation_suggestions":
            job_preparation,

        "seven_day_plan":
            seven_day_plan,

        "thirty_day_plan":
            month_plan

    }