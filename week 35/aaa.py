import json
import random
import string  

# ------------------- Load JSON data -------------------
def load_data(filename):
    """Load quiz data from JSON file. Exits if file not found or invalid JSON."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit()
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        exit()

    # ------------------- Choose quiz mode -------------------

def choose_mode(data):
    """Let user choose a game or all games, and whether to shuffle questions/options."""
    games = data.get("games", [])
    print("\nAvailable Games:")
    for i in range(len(games)):
        print(f"{i + 1}. Game {i + 1}")
    print("0. All Games")

    while True:
        choice = input("\nSelect a game (0 for ALL): ").strip()
        if choice.isdigit():
            choice = int(choice)
            if 0 <= choice <= len(games):
                break
        print("Invalid choice. Enter a number corresponding to a game.")

        # Shuffle questions? (y/n)
    shuffle_questions = input("Shuffle questions? (y/n): ").strip().lower() == 'y'
    # Shuffle options? (y/n)
    shuffle_options = input("Shuffle answer options? (y/n): ").strip().lower() == 'y'

    # Gather questions
    if choice == 0:
        questions = [q for game in games for q in game.get("questions", [])]
    else:
        questions = games[choice - 1].get("questions", [])

    if shuffle_questions:
        random.shuffle(questions)

    return questions, shuffle_options


# ------------------- Run the quiz -------------------
def run_quiz(questions, shuffle_options=False):
    """
    Display questions and options, accept validated user input,
    track score and store incorrectly answered questions.
    """
    score = 0
    wrong_questions = []

    print("\n--- Starting Quiz ---")

    for idx, q in enumerate(questions, start=1):
        print(f"\nQ{idx}: {q.get('question', 'No question text')}")
        options = q.get("content", [])
        correct_index = q.get("correct", 0)

        if shuffle_options:
            # Shuffle options while keeping track of correct index
            combined = list(zip(options, range(len(options))))
            random.shuffle(combined)
            options, new_indices = zip(*combined)
            correct_index = new_indices.index(correct_index)

            # Show options labeled A, B, C, ...
        labels = list(string.ascii_uppercase[:len(options)])
        for label, opt in zip(labels, options):
            print(f"  {label}) {opt}")

            # Input validation loop
        while True:
            answer = input("Your answer (A, B, C...): ").strip().upper()
            if answer in labels:
                break
            print(f"Invalid input! Enter a letter between {labels[0]} and {labels[-1]}.")

        user_index = labels.index(answer)

        if user_index == correct_index:
            print("✔ Correct!")
            score += 1
        else:
            print(f"✘ Wrong! Correct answer: {labels[correct_index]}) {options[correct_index]}")
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
    data = load_data("questions.json")
    questions, shuffle_options = choose_mode(data)
    if not questions:
        print("No questions found.")
        return
    score, wrong = run_quiz(questions, shuffle_options)
    show_summary(len(questions), score, wrong)
    print("\nThank you for playing!\n")


if __name__ == "__main__":
    main()
