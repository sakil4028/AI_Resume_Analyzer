from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils.analyzer import extract_skills


def calculate_ats_score(resume_text, job_description):

    documents = [resume_text, job_description]

    tfidf = TfidfVectorizer()

    tfidf_matrix = tfidf.fit_transform(documents)

    similarity_score = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )

    ats_score = round(similarity_score[0][0] * 100, 2)

    return ats_score


def missing_skills(resume_text, job_description):

    resume_skills = extract_skills(resume_text)

    job_skills = extract_skills(job_description)

    missing = []

    for skill in job_skills:

        if skill not in resume_skills:
            missing.append(skill)

    return missing


def keyword_match(resume_text, job_description):

    resume_words = set(resume_text.lower().split())

    jd_words = set(job_description.lower().split())

    matched_words = resume_words.intersection(jd_words)

    percentage = (len(matched_words) / len(jd_words)) * 100

    return round(percentage, 2)