# FunCaptcha-Solver-(Playwright + Python)-

A custom FunCaptcha (Arkose Labs) solver using **Playwright** and **OpenCV**, built from scratch with no reliance on third-party solving services like CapSolver, 2Captcha, or CapMonster.

---

## What It Does
- Detects FunCaptcha iframe on any given page
- Extracts the image canvas using Playwright
- Simulates mouse drag for rotation-based challenges
- Implements retry logic to attempt multiple challenges
- Logs all actions for **testing and educational** purposes

##  Project Structure
├── .env # Contains TARGET_URL
├── main.py # Entry point: Retry loop & solver orchestration
├── solver/
│ ├── init.py
│ ├── solver.py # Core solver logic (Playwright + OpenCV)
│ ├── utils.py # Helpers like human_delay
├── tests/
│ └── test_solver.py # Basic test mode execution


---

##  Installation

bash
git clone https://github.com/mayowa-id/funcaptcha-solver
cd funcaptcha-solver

python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate

pip install -r requirements.txt 


## Testing Mode
To test the CAPTCHA handling without solving real puzzles:

python tests/test_solver.py
This runs the browser, interacts with the canvas, and simulates human-like dragging. Ideal for sandbox sites or your own mock CAPTCHA page.

## How to Use
Create a .env file and add your test URL:

TARGET_URL=https://your-test-site.com
Run the solver:

python main.py
This will:

Launch the browser

Navigate to the page

Detect and interact with FunCaptcha

Retry up to 5 times if necessary

## Why No Third-Party Solvers?
This project demonstrates:

Deep understanding of browser automation

Handling CAPTCHA challenges without external APIs

Advanced mouse emulation and canvas interaction

## Disclaimer
This solver is strictly for educational, research, and testing purposes.


## Author
Joshua Mayowa Idowu

