from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST

def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id", -1)

    if current_question_id == -1:
        bot_responses.append(BOT_WELCOME_MESSAGE)
        next_question, next_question_id = get_next_question(current_question_id)
        session["current_question_id"] = next_question_id
        session.save()
        bot_responses.append(next_question)
        return bot_responses

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses

def record_current_answer(answer, current_question_id, session):
    if current_question_id is None or current_question_id == -1:
        return False, "No question id was passed"

    if current_question_id < 0 or current_question_id >= len(PYTHON_QUESTION_LIST):
        return False, "Invalid question id"

    question_details = PYTHON_QUESTION_LIST[current_question_id]

    if answer not in question_details["options"]:
        return False, "Select a valid option"
    
    answers = session.get("answers", {})
    answers[current_question_id] = answer
    session["answers"] = answers
    session.save()

    return True, ""

def get_next_question(current_question_id):
    if current_question_id is None or current_question_id == -1:
        next_question_id = 0
    else:
        next_question_id = current_question_id + 1

    if next_question_id >= len(PYTHON_QUESTION_LIST):
        return None, -1

    question_details = PYTHON_QUESTION_LIST[next_question_id]
    next_question = question_details["question_text"]
    options = question_details["options"]
    options_text = "\n".join([f"{i + 1}. {option}" for i, option in enumerate(options)])
    full_question_text = f"{next_question}\nOptions:\n{options_text}"
    return full_question_text, next_question_id


def generate_final_response(session):
    answers = session.get("answers", {})
    score = 0
    total_questions = len(PYTHON_QUESTION_LIST)

    for question_id, question_details in enumerate(PYTHON_QUESTION_LIST):
        correct_answer = question_details["answer"]
        user_answer = answers.get(question_id)
        if user_answer == correct_answer:
            score += 1

    result_message = f"Your score is {score} out of {total_questions}.\n"

    if score == total_questions:
        result_message += "Excellent! You got all the answers correct!"
    elif score >= total_questions / 2:
        result_message += "Good job! You got more than half of the answers correct."
    else:
        result_message += "Keep practicing! You'll get better with more practice."

    return result_message
