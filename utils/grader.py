from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def grade_answer(student_answer, reference_answer):
    score = util.cos_sim(model.encode(student_answer), model.encode(reference_answer))
    return float(score[0][0]) * 10  # scale 1–10

def grade_multiple_answers(student_text, reference_answers):
    return [round(grade_answer(student_text, ans), 2) for ans in reference_answers]
