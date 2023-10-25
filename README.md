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
    
    `python3 futur.py`

## Configuration

Create your own curriculum by copying and modifying the JSON files under `/curricula`. You will need to change `DEFAULT_CURRICULUM_FILENAME` in constants.py.

## Planned features and changes

- introduce a table of rewordings so the prompt is more like "What is 'manger' in this inflection: 'Vous..."
- improve and refactor the spitballed performance timing (currently spread across two files) 
- command line options to at least select which curriculum to use
- a vocabulary question type (would need a separate vocabulary data file), so probably splitting GuessQuestion into GuessVerbQuestion and GuessTranslationQuestion
- an option to time your typing to parameterise the performance rating
- a vocabulary list downloaded from the web so that I can update it remotely (w/o making a commit, I mean)
- perhaps a UI
- better variable names (more domain-driven)