# Self-Evolving AI Content Generation Agent

An AI-powered content generation agent that creates educational lessons, evaluates them against multiple quality criteria, learns from failures using persistent memory, and automatically retries generation using evaluator feedback.

## Overview

This project implements a self-improving AI content generation workflow.

The agent does not simply generate a lesson and stop. It first generates the content, evaluates the content, identifies any problems, stores the lessons learned from failures, and retries generation using the evaluator's feedback.

The workflow is:

Generate → Evaluate → Learn → Retry → Improve

The system evaluates every generated lesson using six quality checks:

1. Accuracy
2. Beginner Friendly
3. Example Based
4. Jargon Free
5. Key Points
6. Coherent Flow

If all checks pass, the lesson is accepted.

If any check fails, the system records the failure, saves the lesson learned to persistent memory, creates feedback, and retries the generation.

---

## Architecture

```text
                    User Topic
                        |
                        v
              +-------------------+
              | Content Generator |
              +-------------------+
                        |
                        v
                Generated Lesson
                        |
                        v
              +-------------------+
              |     Evaluator     |
              +-------------------+
                        |
                +-------+-------+
                |               |
              PASS             FAIL
                |               |
                v               v
          Final Lesson     Rejection Log
                                |
                                v
                         Persistent Memory
                                |
                                v
                       Improvement Feedback
                                |
                                v
                       Content Generator
                                |
                                v
                              Retry

## Project Structure

```text
rag-content-agent/
│
├── src/
│   ├── main.py
│   ├── generator.py
│   ├── evaluator.py
│   ├── prompts.py
│   ├── schemas.py
│   ├── memory.py
│   └── rejection_log.py
│
├── data/
│   └── memory.json
│
├── outputs/
│   └── rejection_log.json
│
├── final_lesson.md
├── requirements.txt
├── .gitignore
└── README.md


## Key Components

### Generator

`generator.py` generates educational lessons using the Groq API.

It receives the requested topic, previous lessons learned from persistent memory, and feedback from the evaluator.

### Evaluator

`evaluator.py` evaluates each generated lesson using six quality checks:

- Accuracy
- Beginner Friendly
- Example Based
- Jargon Free
- Key Points
- Coherent Flow

The evaluator returns a structured result that is validated using Pydantic models defined in `schemas.py`.

### Persistent Memory

`memory.py` stores lessons learned from previous failures in `data/memory.json`.

If the evaluator identifies a problem, such as unexplained technical terms, the failure reason and recommended improvement are stored.

The stored memory is loaded during future executions and provided to the generator.

This allows the agent to retain lessons learned across different runs.

### Rejection Log

`rejection_log.py` stores rejected attempts in `outputs/rejection_log.json`.

Each rejection records:

- Attempt number
- Failed checks
- Reason for failure
- Recommended improvement

## Self-Improvement Workflow

The agent follows this process:

Generate Lesson
       ↓
Evaluate Lesson
       ↓
Does it pass?
   /       \
 YES       NO
  ↓         ↓
Final    Save Rejection
Lesson       ↓
         Save to Memory
              ↓
       Generate Feedback
              ↓
            Retry
              ↓
       Generate Again

When a lesson fails, the evaluator's feedback is sent back to the generator.

The failure is also stored in persistent memory so that the agent can use the lesson learned during future generations.

## Technology Stack

- Python
- Groq API
- Pydantic
- python-dotenv
- JSON-based persistent storage

## Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
2. Activate the virtual environment

On Windows:
.venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Configure the API key

Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key

Running the Agent

From the project root:

python src\main.py

The agent will:

Load previous memory.
Generate a lesson.
Evaluate the lesson.
Accept the lesson if it passes.
Save the rejection if it fails.
Store the lesson learned.
Generate feedback.
Retry the generation.
Example Output

A rejected attempt may look like:

===== ATTEMPT 1 =====

LESSON GENERATED

EVALUATION RESULT:
Overall Pass: False
Failed Checks: ['jargon_free']

LESSON REJECTED.

The feedback is then sent to the generator.

A later attempt can pass:

===== ATTEMPT 2 =====

LESSON GENERATED

EVALUATION RESULT:
Overall Pass: True
Failed Checks: []

LESSON PASSED!

The rejection is stored in outputs/rejection_log.json.

The lesson learned is stored in data/memory.json.

Future Improvements
More advanced memory retrieval
Semantic similarity for previous failures
Additional evaluation criteria
Source citation verification
Database-backed persistent memory
Human feedback integration
Support for multiple LLM providers
Conclusion

This project demonstrates a self-evolving AI content generation workflow where the system can generate content, evaluate its quality, identify failures, remember lessons, use evaluator feedback, retry generation, and produce improved results.
