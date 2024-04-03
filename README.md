# CodeRevise

CodeRevise is a command-line interface (CLI) tool designed to help programmers manage their coding practice questions, focusing on revising and prioritizing questions from LeetCode and other coding platforms.

## Features

- **Add Questions**: Add new coding practice questions with a name, priority, and optional LeetCode or CodePro numbers.
- **List Questions**: View all questions sorted by their priority, helping you focus on what to revise next.
- **Pop Questions**: Remove and display the most unfamiliar question based on its priority, indicating it's time to review that question.
- **Export Questions**: Export your list of questions to a file, allowing for easy backup or sharing.
- **Import Questions**: Import questions from a file, with checks for validity, avoidance of duplicates, and intelligent merging.
- **Clear All Questions**: Clear all stored questions, allowing you to start afresh or manage different sets of questions.

## Installation

To install CodeRevise, follow these steps:

1. Clone this repository or download the source code.
2. Navigate to the root directory of the project in a terminal.
3. Install the package locally using pip:

    ```bash
    pip install .
    ```

This process installs `CodeRevise` globally on your system, making the `coderevise` command available in your terminal.

## Usage

### Add a New Question

```bash
coderevise add "Question Name" priority [--leetcode LEETCODE_NUMBER] [--codepro CODEPRO_NUMBER]
```


