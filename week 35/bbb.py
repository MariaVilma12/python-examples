import mysql.connector
import random
import string

# ------------------- Load quiz data from MySQL -------------------
def load_data_from_db(host="localhost", user="root", password="", database="quiz_db", game_choice=None):
    """
    Fetch quiz data from MySQL database using the actual schema:
    - games
    - questions
    - question_options
    """
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = conn.cursor(dictionary=True)

    data = {"games": []}

    # Fetch all games
    cursor.execute("SELECT id, name FROM games")
    games = cursor.fetchall()

    if not games:
        print("No games found in the database.")
        return data

    # Filter for specific game if requested
    if game_choice is not None and 1 <= game_choice <= len(games):
        games = [games[game_choice - 1]]

    for g in games:
        # Fetch questions for this game
        cursor.execute("""
            SELECT id, question_text, correct_index
            FROM questions
            WHERE game_id = %s
        """, (g['id'],))
        questions = []
        for q in cursor.fetchall():
            # Fetch options for this question, ordered by id
            cursor.execute("""
                SELECT option_text
                FROM question_options
                WHERE question_id = %s
                ORDER BY id
            """, (q['id'],))
            options = [row['option_text'] for row in cursor.fetchall()]
            questions.append({
                "question": q["question_text"],
                "correct": q["correct_index"],
                "content": options
            })
        data["games"].append({"questions": questions})

    cursor.close()
    conn.close()
    return data

# ------------------- Choose quiz mode -------------------
def choose_mode(data):
    games = data.get("games", [])
    print("\nAvailable Games:")
    for i in range(len(games)):
        print(f"{i+1}. {games[i]['questions'][0]['question'] if games[i]['questions'] else 'Game'}")
    print("0. All Games")

    while True:
        choice = input("\nSelect a game (0 for ALL): ").strip()
        if choice.isdigit():
            choice = int(choice)
            if 0 <= choice <= len(games):
                break
        print("Invalid choice. Enter a number corresponding to a game.")

    shuffle_questions = input("Shuffle questions? (y/n): ").strip().lower() == 'y'
    shuffle_options = input("Shuffle answer options? (y/n): ").strip().lower() == 'y'

    if choice == 0:
        questions = [q for game in games for q in game.get("questions", [])]
    else:
        questions = games[choice - 1].get("questions", [])

    if shuffle_questions:
        random.shuffle(questions)

    return questions, shuffle_options

# ------------------- Run the quiz -------------------
def run_quiz(questions, shuffle_options=False):
    score = 0
    wrong_questions = []

    print("\n--- Starting Quiz ---")

    for idx, q in enumerate(questions, start=1):
        print(f"\nQ{idx}: {q.get('question', 'No question text')}")
        options = q.get("content", [])
        correct_index = q.get("correct", 0)

        if shuffle_options:
            combined = list(zip(options, range(len(options))))
            random.shuffle(combined)
            options, new_indices = zip(*combined)
            correct_index = new_indices.index(correct_index)

        labels = list(string.ascii_uppercase[:len(options)])
        for label, opt in zip(labels, options):
            print(f"  {label}) {opt}")

        while True:
            answer = input("Your answer (A, B, C...): ").strip().upper()
            if answer in labels:
                break
            print(f"Invalid input! Enter a letter between {labels[0]} and {labels[-1]}.")

        user_index = labels.index(answer)
        if user_index == correct_index:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! Correct answer: {labels[correct_index]}) {options[correct_index]}")
            wrong_questions.append({
                "question": q.get("question", ""),
                "your_answer": answer,
                "correct_answer": labels[correct_index],
                "options": options
            })

    return score, wrong_questions

# ------------------- Show summary -------------------
def show_summary(total, score, wrong_questions):
    print("\n--- Quiz Summary ---")
    print(f"Total Questions: {total}")
    print(f"Correct Answers: {score}")
    print(f"Incorrect Answers: {total - score}")
    percent = round((score / total) * 100) if total else 0
    print(f"Percentage Score: {percent}%")

    if wrong_questions:
        print("\nReview of Incorrect Answers:")
        for idx, w in enumerate(wrong_questions, start=1):
            print(f"\n{idx}. {w['question']}")
            for label, opt in zip(string.ascii_uppercase[:len(w['options'])], w['options']):
                print(f"  {label}) {opt}")
            print(f"Your answer: {w['your_answer']}")
            print(f"Correct answer: {w['correct_answer']}")

# ------------------- Main entry point -------------------
def main():
    data = load_data_from_db(
        host="localhost",
        user="root",
        password="gokstad",
        database="QuestionsDB"
    )

    questions, shuffle_options = choose_mode(data)
    if not questions:
        print("No questions found.")
        return

    score, wrong = run_quiz(questions, shuffle_options)
    show_summary(len(questions), score, wrong)
    print("\nThank you for playing!\n")

if __name__ == "__main__":
    main()
