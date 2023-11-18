# Futur

**A language-learning flashcard game by Kevin Higgins**

## Setup

**Requirements:**
- Python 3.9.0+ (tested on 3.10.12)
- pip

**Steps:**
1. Create a venv in your local copy of this repo

    `python3 -m venv .venv`
1. Activate the venv
    
    `source .venv/bin/activate` (Linux) or `.\.venv\scripts\bin\activate` (Windows)
1. Install fsrs (spaced repetition library)
    
    `pip install fsrs`
1. Run the app
    
    `python3 futur.py future-irregular-top-10.json`

## Configuration

Create your own curriculum by copying and modifying the JSON files under `curricula`.

Choose which curriculum to examine via the final command line argument when running the program.

Tweak the wording of the questions by modifying `question-wordings/templates.json` and
`question-wordings/column-renamings.json`. The intention of the latter is to yield more
naturalistic prompts with a pronoun like "vous" instead of a bunch of grammatical terms.

## Planned features and changes

- friendlier presentation of due date - "today", "tomorrow", "in 5 minutes"
- better control and options, a quit key, remove debug text
- multiple-choice questions (with the Question storing many wrong answers, some of which are randomly chosen when it is asked)
- improve and refactor the spitballed performance timing (currently spread across two modules) 
- a vocabulary question type (would need a separate vocabulary data file), so probably splitting GuessQuestion into GuessVerbQuestion and GuessTranslationQuestion
- an option to time your typing to parameterise the performance rating
- a vocabulary list downloaded from the web so that I can update it remotely (w/o making a commit, I mean)
- perhaps a UI
- better variable names (more domain-driven)