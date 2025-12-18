# Submission Guide - SHL Assessment Recommendation Engine

Follow these steps to package and submit your project to ensure it runs perfectly for the reviewers.

## 1. Verify Before Packaging
Before zipping, make sure everything works on a fresh setup.
1. **Run the verification script**:
   ```powershell
   python verify.py
   ```
   *Expected Output*: Should print "✅ Diagnosis Successful".

2. **Check the Notebook**:
   Open `notebooks/Assessment_Recommendation_Engine.ipynb` and ensure all cells have been run and saved (so they can see the output without running it themselves).

## 2. Cleaner (Important!)
Remove temporary files to keep the submission clean and small.
- Delete the `venv` or `.venv` folder (reviewers will install their own requirements).
- Delete `__pycache__` folders inside `src/` if present.

## 3. Packaging
1. Zip the entire project folder `shl1`.
   - **Name the zip file**: `Firstname_Lastname_SHL_Assessment_Engine.zip`
2. **Contents of Zip** should look like this:
   ```text
   /
   ├── app.py
   ├── requirements.txt
   ├── README.md
   ├── verify.py
   ├── data/
   │   ├── job_roles.csv
   │   └── shl_products.csv
   ├── src/
   │   ├── __init__.py
   │   ├── features.py
   │   ├── preprocessing.py
   │   ├── recommender.py
   │   └── evaluation.py
   └── notebooks/
       └── Assessment_Recommendation_Engine.ipynb
   ```

## 4. Final Checklist
- [ ] **Links**: Ensure all links in `README.md` are valid (if you added any github repos).
- [ ] **Paths**: The code uses relative paths (e.g., `data/shl_products.csv`), so it will work on any machine. Do NOT hardcode paths like `C:/Users/...`.
- [ ] **Requirements**: Ensure `requirements.txt` is present.

## 5. Submission
- Upload the `.zip` file to the submission portal or Google Drive link provided by the recruiter.
- If submitting via GitHub:
  1. Initialize git: `git init`
  2. Add files: `git add .`
  3. Commit: `git commit -m "Initial commit"`
  4. Push to receiving repository.
  5. **Note**: Make sure `data/` files are included (remove them from `.gitignore` if present).

## Troubleshooting for Reviewers
If the reviewer asks how to run it, point them to the **How to Run** section in the `README.md`.
