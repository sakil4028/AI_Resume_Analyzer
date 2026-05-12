from utils.preprocess import preprocess_text


skills_database = [
    "python",
    "java",
    "sql",
    "machine learning",
    "deep learning",
    "flask",
    "django",
    "power bi",
    "excel",
    "tableau",
    "tensorflow",
    "pandas",
    "numpy",
    "data analysis",
    "nlp",
    "computer vision",
    "html",
    "css",
    "javascript",
    "react"
]


def extract_skills(resume_text):

    processed_text = preprocess_text(resume_text)

    found_skills = []

    resume_string = " ".join(processed_text)

    for skill in skills_database:

        if skill.lower() in resume_string:

            found_skills.append(skill)

    return list(set(found_skills))