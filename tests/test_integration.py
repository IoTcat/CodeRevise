import os
import sys

# Append the directory above 'tests' to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'coderevise')))

from revise import Question, QuestionManager

import pytest
import json

@pytest.fixture
def question_manager(tmp_path):
    db_path = tmp_path / "questions.db"
    return QuestionManager(filepath=str(db_path))

def test_export_import_cycle(question_manager, tmp_path):
    questions = [
        Question("Q1", 1, 111, 211),
        Question("Q2", 2, 222, 222),
    ]
    for q in questions:
        question_manager.push(q)

    export_path = tmp_path / "export.json"
    question_manager.export_questions(str(export_path))

    new_manager = QuestionManager(filepath=str(tmp_path / "new_questions.db"))
    new_manager.import_questions(str(export_path))

    assert len(new_manager.heap) == len(questions)
    for q in questions:
        assert any(nq.name == q.name and nq.priority == q.priority for nq in new_manager.heap)

def test_full_usage_scenario(tmp_path):
    manager = QuestionManager(filepath=str(tmp_path / "usage.db"))
    manager.push(Question("Usage Q1", 5))
    manager.push(Question("Usage Q2", 10))

    export_path = tmp_path / "usage_export.json"
    manager.export_questions(str(export_path))

    manager.clear_all()
    assert len(manager.heap) == 0

    manager.import_questions(str(export_path))
    assert len(manager.heap) == 2

