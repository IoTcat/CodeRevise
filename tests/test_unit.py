import os
import sys

# Append the directory above 'tests' to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'coderevise')))

from revise import Question, QuestionManager

import pytest

@pytest.fixture
def question_manager(tmp_path):
    db_path = tmp_path / "questions.db"
    return QuestionManager(filepath=str(db_path))

def test_add_question(question_manager):
    question = Question("Test Unit", 3)
    question_manager.push(question)
    assert any(q.name == "Test Unit" for q in question_manager.heap)

def test_avoid_duplicate_addition(question_manager):
    q_name = "Duplicate Question"
    question_manager.push(Question(q_name, 1, 100))
    question_manager.push(Question(q_name, 2, 101))  # Attempt to add duplicate
    assert len(question_manager.heap) == 1
    assert any(q.leetcode_number == 101 for q in question_manager.heap)  # Updated info

def test_pop_question(question_manager):
    question_manager.push(Question("Low", 1))
    question_manager.push(Question("High", 10))
    popped_question = question_manager.pop()
    assert popped_question.name == "High"

def test_clear_all_questions(question_manager):
    question_manager.push(Question("Q1", 1))
    question_manager.push(Question("Q2", 2))
    question_manager.clear_all()
    assert len(question_manager.heap) == 0

