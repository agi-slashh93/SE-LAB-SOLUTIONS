# Lab 5 Reflection

**Name:** R Agilesh  
**SRN:** PES2UG24CS385

1. **Which issues were the easiest to fix, and which were the hardest? Why?**  
   The easiest fixes were the style issues, such as renaming `addDue` to `add_due`, adding docstrings, and correcting spacing. The hardest issue was removing `eval` without losing the demonstration's ability to calculate `50 * 2`. I replaced it with a small AST evaluator that accepts only numeric literals and basic arithmetic operators, so it retains the needed calculation without executing arbitrary Python.

2. **Did the static analysis tools report any false positives? If so, describe one example.**  
   I did not identify a false positive among the reported findings. The SQL interpolation and `eval` warnings pointed to real unsafe patterns. Bandit's hard-coded password warning was valid as a source-code risk even though that constant was not used by the demonstration.

3. **How would you integrate static analysis tools into your actual software development workflow?**  
   I would run Flake8, Pylint, and Bandit locally before committing, then run the same checks in continuous integration on every pull request. I would fix security and correctness findings first, and keep the checks visible so regressions are caught before merging.

4. **What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?**  
   The SQL now treats inputs as values, and penalty calculations cannot execute arbitrary code. Each call to `add_due` gets independent history unless a caller provides a list. Invalid dues are rejected, missing payments return an explicit `None`, and the function names and docstrings make the code easier to follow. The example still collects a payment, calculates a penalty, and lists unpaid flats.
