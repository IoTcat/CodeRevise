import heapq
import argparse
import pickle
import os
import json

class Question:
    def __init__(self, name, priority, leetcode_number=None, codepro_number=None):
        self.name = name
        self.priority = priority
        self.leetcode_number = leetcode_number
        self.codepro_number = codepro_number
    
    def __lt__(self, other):
        return -self.priority < -other.priority

    def __repr__(self):
        return (f"Name: {self.name}, Priority: {self.priority}, "
                f"LeetCode#: {self.leetcode_number}, CodePro#: {self.codepro_number}")

class QuestionManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.heap = self.load_questions()

    def push(self, question):
        existing_question = next((q for q in self.heap if q.name == question.name), None)
        if existing_question:
            existing_question.priority = question.priority
            existing_question.leetcode_number = question.leetcode_number or existing_question.leetcode_number
            existing_question.codepro_number = question.codepro_number or existing_question.codepro_number
            print(f"Updated existing question: {question.name}")
        else:
            heapq.heappush(self.heap, question)
            print(f"Added new question: {question.name}")
        self.save_questions()

    def pop(self):
        if self.heap:
            question = heapq.heappop(self.heap)
            self.save_questions()
            return question
        else:
            return "No questions to pop"

    def print_all_questions(self):
        sorted_questions = sorted(self.heap, key=lambda x: -x.priority)
        for question in sorted_questions:
            print(question)

    def save_questions(self):
        with open(self.filepath, 'wb') as file:
            pickle.dump(self.heap, file)

    def load_questions(self):
        if os.path.exists(self.filepath) and os.path.getsize(self.filepath) > 0:
            with open(self.filepath, 'rb') as file:
                return pickle.load(file)
        return []

    def export_questions(self, filepath):
        with open(filepath, 'w') as file:
            for question in self.heap:
                question_data = {
                    'name': question.name,
                    'priority': question.priority,
                    'leetcode_number': question.leetcode_number,
                    'codepro_number': question.codepro_number
                }
                file.write(json.dumps(question_data) + '\n')

    def import_questions(self, filepath):
        try:
            with open(filepath, 'r') as file:
                imported_questions = [json.loads(line.strip()) for line in file]
        except Exception as e:
            print(f"Failed to load questions from {filepath}: {e}")
            return

        updated = 0
        added = 0
        for question_data in imported_questions:
            if 'name' not in question_data or 'priority' not in question_data:
                print(f"Skipping invalid question (missing name or priority): {question_data}")
                continue

            existing_question = next((q for q in self.heap if q.name == question_data['name']), None)
            if existing_question:
                needs_update = False
                if existing_question.priority != question_data['priority']:
                    existing_question.priority = max(existing_question.priority, question_data['priority'])
                    needs_update = True
                if 'leetcode_number' in question_data and existing_question.leetcode_number != question_data['leetcode_number']:
                    existing_question.leetcode_number = question_data['leetcode_number']
                    needs_update = True
                if 'codepro_number' in question_data and existing_question.codepro_number != question_data['codepro_number']:
                    existing_question.codepro_number = question_data['codepro_number']
                    needs_update = True
                
                if needs_update:
                    updated += 1
            else:
                self.push(Question(**question_data))
                added += 1

        self.save_questions()
        print(f"Import completed. {added} questions added, {updated} questions updated.")

    def clear_all(self):
        self.heap = []
        self.save_questions()
        print("All questions have been cleared.")

def main():
    parser = argparse.ArgumentParser(description="Manage coding practice questions for revising.")
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add', help='Add a new question')
    add_parser.add_argument('name', type=str, help='Question name')
    add_parser.add_argument('priority', type=int, help='Priority value')
    add_parser.add_argument('--leetcode', type=int, help='LeetCode question number', default=None)
    add_parser.add_argument('--codepro', type=int, help='CodePro question number', default=None)

    subparsers.add_parser('pop', help='Remove the most unfamiliar question')
    subparsers.add_parser('list', help='List all questions sorted by priority')

    export_parser = subparsers.add_parser('export', help='Export questions to a file')
    export_parser.add_argument('filepath', type=str, help='File path to export questions to')

    import_parser = subparsers.add_parser('import', help='Import questions from a file')
    import_parser.add_argument('filepath', type=str, help='File path to import questions from')

    subparsers.add_parser('clear', help='Clear all questions')

    args = parser.parse_args()

    question_manager = QuestionManager(filepath="questions.db")

    if args.command == 'add':
        question = Question(args.name, args.priority, args.leetcode, args.codepro)
        question_manager.push(question)
    elif args.command == 'pop':
        print("Popping the most unfamiliar question:")
        print(question_manager.pop())
    elif args.command == 'list':
        question_manager.print_all_questions()
    elif args.command == 'export':
        question_manager.export_questions(args.filepath)
        print(f"Questions exported successfully to {args.filepath}")
    elif args.command == 'import':
        question_manager.import_questions(args.filepath)
    elif args.command == 'clear':
        question_manager.clear_all()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

