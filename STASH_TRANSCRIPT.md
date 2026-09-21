# STASH_TRANSCRIPT.md - the full captured `git stash` session

Every command below was run for real in Git Bash on Windows 11 inside this
repository, and **every line of output is pasted verbatim** from the terminal.
The raw, unannotated capture of exactly the same session is committed next to
this file as [`stash_session_capture.txt`](stash_session_capture.txt).

Nothing in this document is invented or paraphrased: the stash SHAs
(`32adf60a5aac468c512e8569c147262ba8b48787`,
`99bfe2fd5417692051285869f87a9bc896dd6407`), the `stash@{0}` entries and the
diffstats are the ones git actually printed.

**Quick jump to the five required commands:**
[`git stash list`](#4-git-stash-list) ·
[`git stash show`](#5-git-stash-show) ·
[`git stash apply`](#6-git-stash-apply---reapplies-and-keeps-the-stash) ·
[`git stash pop`](#8-git-stash-pop---reapplies-and-removes-the-stash) ·
[`git stash drop`](#9-git-stash-drop---discards-a-stash-without-applying-it)

---

## The scenario

I am half way through a new `percentage` feature on `feature-percentage`.
Nothing is committable yet - the code does not even run. A production bug is
reported: division by zero prints a message that tells the user nothing useful.
The fix has to go out now, from a clean branch off `main`.

That is exactly the situation `git stash` exists for.

---

## 1. Start the feature - and leave it unfinished

```console
$ git checkout -b feature-percentage
Switched to a new branch 'feature-percentage'
```

A new `percentage_module.py` was created and `dashboard.py` was edited, both
deliberately incomplete.

```console
$ git status
On branch feature-percentage
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   dashboard.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	percentage_module.py

no changes added to commit (use "git add" and/or "git commit -a")
```

One tracked file modified, one brand new untracked file - and **nothing is
committed**.

```console
$ git diff --stat
 dashboard.py | 3 +++
 1 file changed, 3 insertions(+)
```

`git diff` only sees the tracked file; the untracked module is invisible to it,
which matters for the stash command chosen in step 2.

The work really is unfinished - the project does not run:

```console
$ python dashboard.py < /dev/null
Enter a number 1 :    -> no input available, using default: 10
Enter a number 2 :    -> no input available, using default: 5
Enter username :    -> no input available, using default: veerandra
Enter password :    -> no input available, using default: demo-password
API key present and logged in as veerandra
API key present and logged in as veerandra
API key present and logged in as veerandra
API key present and logged in as veerandra
*************** DASHBOARD ***************
Result of addition is       :  15
Result of subtraction is    :  5
Result of multiplication is :  50
Result of division is       :  2.0
Traceback (most recent call last):
  File "C:\Users\asus\Desktop\work\6-month-fde-challenge\03_git_and_git_hub\task-03-git-stash-practical\dashboard.py", line 12, in <module>
    print("Result of percentage is     : ", pct)
                                            ^^^
NameError: name 'pct' is not defined. Did you mean: 'oct'?
```

This crash is the proof that committing here would have broken `main`.

---

## 2. Park the work with `git stash push`

```console
$ git stash push -u -m "WIP: percentage feature"
Saved working directory and index state On feature-percentage: WIP: percentage feature
```

`-m` labels the stash so it is recognisable later; `-u` (`--include-untracked`)
is required here because `percentage_module.py` is untracked and a plain
`git stash push` would have left it behind in the working tree.

```console
$ git status
On branch feature-percentage
nothing to commit, working tree clean
```

The working tree is now genuinely clean - this is the whole point of stashing.

```console
$ git stash list
stash@{0}: On feature-percentage: WIP: percentage feature
```

```console
$ ls percentage_module.py
ls: cannot access 'percentage_module.py': No such file or directory
```

The untracked file really was taken away by `-u`, not just ignored.

---

## 3. Ship the urgent fix on another branch

```console
$ git checkout main
Switched to branch 'main'

$ git checkout -b hotfix-division-by-zero
Switched to a new branch 'hotfix-division-by-zero'
```

Switching branches was only possible because the tree was clean.

Reproducing the reported bug first:

```console
$ python -c "from division_module import division; print(\"returned:\", division(10, 0))" < /dev/null
Enter username :    -> no input available, using default: veerandra
Enter password :    -> no input available, using default: demo-password
Cannot divide by zero
returned: None
```

"Cannot divide by zero" does not say which value was wrong or what to do next.

After the fix:

```console
$ python -c "from division_module import division; print(\"returned:\", division(10, 0))" < /dev/null
Enter username :    -> no input available, using default: veerandra
Enter password :    -> no input available, using default: demo-password
Cannot divide 10 by zero - enter a non-zero second number
returned: None
```

```console
$ git diff
diff --git a/division_module.py b/division_module.py
index 23788ce..90607d2 100644
--- a/division_module.py
+++ b/division_module.py
@@ -1,6 +1,8 @@
 from config import api_key
 from profile import profile_name
 
+ZERO_DIVISOR_MESSAGE = "Cannot divide {} by zero - enter a non-zero second number"
+
 
 def division(a, b):
     """Return a / b once the API key and the logged-in profile are present."""
@@ -11,7 +13,13 @@ def division(a, b):
         print("No logged-in profile - cannot run division")
         return None
     if b == 0:
-        print("Cannot divide by zero")
+        print(ZERO_DIVISOR_MESSAGE.format(a))
         return None
     print("API key present and logged in as", profile_name)
-    return a / b
+    try:
+        return a / b
+    except ZeroDivisionError:
+        # Backstop for numeric types whose zero does not compare equal to 0,
+        # so a bad divisor can never take the whole dashboard down.
+        print(ZERO_DIVISOR_MESSAGE.format(a))
+        return None
```

```console
$ git commit -m "Harden the divide-by-zero guard and make its message actionable" -m "..."
[hotfix-division-by-zero 202c05d] Harden the divide-by-zero guard and make its message actionable
 1 file changed, 10 insertions(+), 2 deletions(-)

$ git checkout main
Switched to branch 'main'

$ git merge --no-ff hotfix-division-by-zero -m "Merge branch 'hotfix-division-by-zero' into main"
Merge made by the 'ort' strategy.
 division_module.py | 12 ++++++++++--
 1 file changed, 10 insertions(+), 2 deletions(-)
```

The hotfix is on `main` and the half-written feature never touched it.

Note what the history looks like while the stash exists - git stores a stash as
real commit objects hanging off `refs/stash`:

```console
$ git log --oneline --graph --all --decorate
*   0a1e77e (HEAD -> main) Merge branch 'hotfix-division-by-zero' into main
|\  
| * 202c05d (hotfix-division-by-zero) Harden the divide-by-zero guard and make its message actionable
|/  
| *   32adf60 (refs/stash) On feature-percentage: WIP: percentage feature
|/|\  
| | * 99e3405 untracked files on feature-percentage: 273950f Add calculator entry point and dashboard integration layer
| * 9eb504a index on feature-percentage: 273950f Add calculator entry point and dashboard integration layer
|/  
* 273950f (feature-percentage) Add calculator entry point and dashboard integration layer
* 12df5c8 Add arithmetic modules for addition, subtraction, multiplication and division
* fae5a5b Add input, login and profile modules with non-interactive defaults
* 804fc7f Add gitignore, environment template and configuration module
```

`32adf60` is the stash commit, with `9eb504a` (the index) and `99e3405` (the
untracked files, present only because `-u` was used) as its parents. Remember
that SHA `32adf60` - `git stash pop` prints it again in step 8.

---

## 4. `git stash list`

Back on the feature branch:

```console
$ git checkout feature-percentage
Switched to branch 'feature-percentage'

$ git status
On branch feature-percentage
nothing to commit, working tree clean
```

```console
$ git stash list
stash@{0}: On feature-percentage: WIP: percentage feature
```

`git stash list` shows every saved stash, newest first. `stash@{0}` is the most
recent one; the text after the colon is the branch it was made on plus the
message given with `-m`.

---

## 5. `git stash show`

```console
$ git stash show stash@{0}
 dashboard.py | 3 +++
 1 file changed, 3 insertions(+)
```

Without options, `git stash show` prints a **diffstat** - a summary of which
tracked files the stash touches and by how much.

```console
$ git stash show --include-untracked stash@{0}
 dashboard.py         |  3 +++
 percentage_module.py | 13 +++++++++++++
 2 files changed, 16 insertions(+)
```

`--include-untracked` also lists the untracked file that `-u` saved. Worth
knowing: the plain form above silently omits it.

```console
$ git stash show -p stash@{0}
diff --git a/dashboard.py b/dashboard.py
index ece6422..78a743e 100644
--- a/dashboard.py
+++ b/dashboard.py
@@ -1,10 +1,13 @@
 """Final integration point - displays the results produced by calculator.py."""
 
 from calculator import total, subtraction, multiplication, div
+from percentage_module import percentage  # TODO: a and b are not imported yet
 
 print("*************** DASHBOARD ***************")
 print("Result of addition is       : ", total)
 print("Result of subtraction is    : ", subtraction)
 print("Result of multiplication is : ", multiplication)
 print("Result of division is       : ", div)
+# TODO: pct is not computed anywhere yet - this line is still a placeholder
+print("Result of percentage is     : ", pct)
 print("*****************************************")
```

`-p` (`--patch`) prints the full diff instead of the summary, so the exact
parked changes can be reviewed before deciding to restore them.

---

## 6. `git stash apply` - reapplies AND KEEPS the stash

```console
$ git stash apply stash@{0}
On branch feature-percentage
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   dashboard.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	percentage_module.py

no changes added to commit (use "git add" and/or "git commit -a")
```

The parked changes are back in the working tree.

```console
$ git status
On branch feature-percentage
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   dashboard.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	percentage_module.py

no changes added to commit (use "git add" and/or "git commit -a")
```

**And now the important part:**

```console
$ git stash list
stash@{0}: On feature-percentage: WIP: percentage feature
```

The stash entry **is still listed**. `apply` restored the changes and left the
stash in place. Note also that `apply` printed no "Dropped ..." line - compare
this with step 8.

---

## 7. Reset the working tree so `pop` can be demonstrated cleanly

```console
$ git checkout -- .

$ rm percentage_module.py

$ git status
On branch feature-percentage
nothing to commit, working tree clean
```

`git checkout -- .` discards the modification to the tracked file and `rm`
deletes the restored untracked file, putting the tree back to the state it was
in before `apply`.

```console
$ git stash list
stash@{0}: On feature-percentage: WIP: percentage feature
```

The stash survived being applied and then thrown away - because `apply` kept it,
the work was never at risk. That is the safety net this whole section is about.

---

## 8. `git stash pop` - reapplies AND REMOVES the stash

```console
$ git stash pop
On branch feature-percentage
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   dashboard.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	percentage_module.py

no changes added to commit (use "git add" and/or "git commit -a")
Dropped refs/stash@{0} (32adf60a5aac468c512e8569c147262ba8b48787)
```

The restored changes are identical to what `apply` produced - but look at the
last line: `Dropped refs/stash@{0} (32adf60...)`. That SHA is the same stash
commit `32adf60` seen in the graph in step 3. `pop` deleted the entry as part of
the same command.

```console
$ git status
On branch feature-percentage
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   dashboard.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	percentage_module.py

no changes added to commit (use "git add" and/or "git commit -a")
```

```console
$ git stash list

```

**The list is now completely empty.** `git stash list` prints nothing at all
when there are no stashes. Side by side:

| after | `git stash list` output |
| --- | --- |
| `git stash apply` (step 6) | `stash@{0}: On feature-percentage: WIP: percentage feature` |
| `git stash pop` (step 8) | *(nothing - the entry is gone)* |

Same restored files, different effect on the stash list. That is the entire
difference between the two commands.

---

## 9. `git stash drop` - discards a stash WITHOUT applying it

A throwaway debug line was added to `calculator.py`:

```console
$ git diff calculator.py
diff --git a/calculator.py b/calculator.py
index 52c73c7..6eefaa0 100644
--- a/calculator.py
+++ b/calculator.py
@@ -16,3 +16,4 @@ if __name__ == "__main__":
     print("Subtraction of the two numbers is    : ", subtraction)
     print("Multiplication of the two numbers is : ", multiplication)
     print("Division of the two numbers is       : ", div)
+print("DEBUG: throwaway trace line, never meant to be committed")
```

It is stashed on its own with a pathspec, so the real percentage work still
sitting in the tree from step 8 is not swept up with it:

```console
$ git stash push -m "throwaway: temporary debug print" -- calculator.py
Saved working directory and index state On feature-percentage: throwaway: temporary debug print

$ git stash list
stash@{0}: On feature-percentage: throwaway: temporary debug print
```

```console
$ git status
On branch feature-percentage
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   dashboard.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	percentage_module.py

no changes added to commit (use "git add" and/or "git commit -a")
```

`calculator.py` is no longer listed as modified - only that one file went into
the stash - while the percentage work is untouched.

```console
$ git stash drop stash@{0}
Dropped stash@{0} (99bfe2fd5417692051285869f87a9bc896dd6407)

$ git stash list

```

```console
$ git diff calculator.py

```

`drop` deleted the stash entry and **never restored anything**: the empty
`git diff calculator.py` proves the debug line is gone for good. Use it to bin
a stash you have decided you do not want.

---

## 10. Finish the feature properly and merge

With the popped work back in the tree the feature was completed, and the project
runs again:

```console
$ python dashboard.py < /dev/null
Enter a number 1 :    -> no input available, using default: 10
Enter a number 2 :    -> no input available, using default: 5
Enter username :    -> no input available, using default: veerandra
Enter password :    -> no input available, using default: demo-password
API key present and logged in as veerandra
API key present and logged in as veerandra
API key present and logged in as veerandra
API key present and logged in as veerandra
API key present and logged in as veerandra
*************** DASHBOARD ***************
Result of addition is       :  15
Result of subtraction is    :  5
Result of multiplication is :  50
Result of division is       :  2.0
Result of percentage is     :  200.0
*****************************************
```

```console
$ git commit -m "Add percentage module and show the percentage result on the dashboard" -m "..."
[feature-percentage f8d60e9] Add percentage module and show the percentage result on the dashboard
 2 files changed, 30 insertions(+)
 create mode 100644 percentage_module.py

$ git checkout main
Switched to branch 'main'

$ git merge --no-ff feature-percentage -m "Merge branch 'feature-percentage' into main"
Merge made by the 'ort' strategy.
 dashboard.py         |  5 +++++
 percentage_module.py | 25 +++++++++++++++++++++++++
 2 files changed, 30 insertions(+)
 create mode 100644 percentage_module.py
```

```console
$ git stash list

```

The session ends with **no leftover stashes**.

---

## Summary of the five commands

| Command | What it does | Touches the working tree? | Removes the stash entry? |
| --- | --- | --- | --- |
| `git stash list` | Lists saved stashes, newest first as `stash@{0}`, `stash@{1}`, ... | No | No |
| `git stash show [-p] stash@{0}` | Shows a diffstat, or the full patch with `-p` | No | No |
| `git stash apply stash@{0}` | Reapplies the changes | Yes | **No - the stash stays** |
| `git stash pop` | Reapplies the changes | Yes | **Yes - if the apply succeeded** |
| `git stash drop stash@{0}` | Deletes a stash entry without restoring it | No | Yes |

The `apply` versus `pop` distinction is expanded, with this same before/after
evidence, in [APPLY_VS_POP.md](APPLY_VS_POP.md).
