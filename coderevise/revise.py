import heapq
import argparse
import pickle
import os
import json
import appdirs
from tabulate import tabulate

class Question:
    def __init__(self, name, priority, leetcode_number=None, codepro_number=None):
        self.name = name
        self.priority = priority
        self.leetcode_number = leetcode_number
        self.codepro_number = codepro_number
    
    def __lt__(self, other):
        return -self.priority < -other.priority

    def __repr__(self):
        headers = ["Name", "Priority", "LeetCode#", "CodePro#"]
        rows = [[self.name, self.priority, self.leetcode_number, self.codepro_number]]
        return tabulate(rows, headers=headers)

class QuestionManager:
    def __init__(self, filepath=None):
        appname = "CodeRevise"
        appauthor = "MyCompany"  # Change as appropriate for your app/company
        default_db_path = os.path.join(appdirs.user_data_dir(appname, appauthor), 'questions.db')
        
        # Use an environment variable to specify the DB path. Fallback to path provided by appdirs.
        self.filepath = os.getenv('CODE_REVISE_DB_PATH', default_db_path)

        if filepath:
            self.filepath = filepath

        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        
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

    def pop(self, new_priority=None):
        if self.heap:
            question = heapq.heappop(self.heap)
            if new_priority:
                question.priority = new_priority
            else:
                question.priority *= 0.7
            heapq.heappush(self.heap, question)
            self.save_questions()
            return question
        else:
            return "No questions to pop"

    def print_all_questions(self):
        sorted_questions = sorted(self.heap, key=lambda x: -x.priority)
        headers = ["Name", "Priority", "LeetCode#", "CodePro#"]
        rows = []
        for question in sorted_questions:
            row = [question.name, question.priority, question.leetcode_number, question.codepro_number]
            rows.append(row)
        print(tabulate(rows, headers=headers))


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

    pop_parser = subparsers.add_parser('pop', help='Pop the most unfamiliar question and reduce its priority')
    pop_parser.add_argument('--priority', type=int, help='Set a new priority for the popped question')
    
    subparsers.add_parser('list', help='List all questions sorted by priority')

    export_parser = subparsers.add_parser('export', help='Export questions to a file')
    export_parser.add_argument('filepath', type=str, help='File path to export questions to')

    import_parser = subparsers.add_parser('import', help='Import questions from a file')
    import_parser.add_argument('filepath', type=str, help='File path to import questions from')

    subparsers.add_parser('clear', help='Clear all questions')

    args = parser.parse_args()

    question_manager = QuestionManager()

    if args.command == 'add':
        question = Question(args.name, args.priority, args.leetcode, args.codepro)
        question_manager.push(question)
    elif args.command == 'pop':
        print("Popping the most unfamiliar question:")
        print(question_manager.pop(args.priority))
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

