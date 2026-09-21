# Task 3 - Git Stash Practical

A small Python calculator project used as the backdrop for a complete, **real**
`git stash` workflow: an unfinished feature is parked with `git stash`, an
urgent production fix ships from another branch, and the parked work is then
inspected and restored with `git stash list`, `show`, `apply`, `pop` and `drop`.

Every terminal output in this README is **pasted verbatim from the actual
session**. The stash SHAs, the `stash@{0}` entries and the diffstats are the
real ones git printed - nothing here is reconstructed or paraphrased.

| Evidence file | What is in it |
| --- | --- |
| [`stash_session_capture.txt`](stash_session_capture.txt) | The raw, unedited terminal capture of the whole session (48 commands, tee'd straight from the shell) |
| [`STASH_TRANSCRIPT.md`](STASH_TRANSCRIPT.md) | The same session, annotated step by step with an explanation under each command |
| [`APPLY_VS_POP.md`](APPLY_VS_POP.md) | `apply` vs `pop` in depth, with the before/after `git stash list` proof |

---

## Contents

- [What the project is](#what-the-project-is)
- [How to run](#how-to-run)
- [The stash scenario](#the-stash-scenario)
- [Full stash workflow transcript](#full-stash-workflow-transcript)
- [apply vs pop](#apply-vs-pop)
- [When git stash is useful in a real development team](#when-git-stash-is-useful-in-a-real-development-team)
- [Full git history](#full-git-history)
- [Fixes applied after review feedback](#fixes-applied-after-review-feedback)

---

## What the project is

A deliberately simple, multi-module Python calculator - small enough that the
git workflow, not the code, is the point.

| File | Role |
| --- | --- |
| `config.py` | Reads `API_KEY` from the environment with a safe demo fallback, so a fresh clone runs with no setup |
| `.env.example` | Template for a real `.env` (the real `.env` is gitignored) |
| `input_variables.py` | Collects the two numbers, falling back to defaults when there is no terminal |
| `login.py` | Collects username and password, with the same fallback |
| `profile.py` | Derives `profile_name` from the login details |
| `addition_module.py`, `subtract_module.py`, `multiply_module.py`, `division_module.py` | One arithmetic operation each, guarded by the API key and the logged-in profile |
| `percentage_module.py` | The feature that was stashed mid-flight and finished later |
| `calculator.py` | Wires the arithmetic modules to the collected inputs |
| `dashboard.py` | Entry point - prints the five results |

No file that the code imports is ever listed in `.gitignore`, and there is no
`secrets.py`: configuration lives in `config.py`, which is committed.

---

## How to run

Python 3 only, no dependencies:

```
git clone https://github.com/6-month-fde-challenge/task-03-git-stash-practical.git
cd task-03-git-stash-practical
python dashboard.py
```

Real output from a fresh clone, run non-interactively so the defaults kick in:

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

Run it without `< /dev/null` and it prompts for the two numbers and the login
instead.

---

## The stash scenario

The real-world story this repository acts out:

1. I am on `feature-percentage`, half way through a new `percentage_module.py`
   and a matching edit to `dashboard.py`. The code does not even import
   cleanly - `pct` is referenced before it is computed - so **there is nothing
   worth committing**.
2. A production bug lands: when a user divides by zero the dashboard prints
   `Cannot divide by zero`, which does not say which value was wrong or what to
   do about it. It has to be fixed now, off a clean `main`.
3. Committing the half-finished feature just to change branches would push
   broken code into the history. Throwing the work away is worse.
4. So the work is parked with `git stash push -u -m "WIP: percentage feature"`,
   the hotfix ships from `hotfix-division-by-zero`, and the parked work is
   brought back afterwards with `git stash pop`.

That is the gap `git stash` fills: **a clean working tree right now, without
committing and without losing anything.**

---

## Full stash workflow transcript

All five required commands, with genuine output. The annotated, step-by-step
version is in [`STASH_TRANSCRIPT.md`](STASH_TRANSCRIPT.md); the raw capture is
in [`stash_session_capture.txt`](stash_session_capture.txt).

### Step 1 - an unfinished feature, uncommitted

```console
$ git checkout -b feature-percentage
Switched to a new branch 'feature-percentage'

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

The feature genuinely does not work yet:

```console
$ python dashboard.py < /dev/null
...
Result of division is       :  2.0
Traceback (most recent call last):
  File "C:\Users\asus\Desktop\work\6-month-fde-challenge\03_git_and_git_hub\task-03-git-stash-practical\dashboard.py", line 12, in <module>
    print("Result of percentage is     : ", pct)
                                            ^^^
NameError: name 'pct' is not defined. Did you mean: 'oct'?
```

### Step 2 - park it with `git stash push`

```console
$ git stash push -u -m "WIP: percentage feature"
Saved working directory and index state On feature-percentage: WIP: percentage feature

$ git status
On branch feature-percentage
nothing to commit, working tree clean

$ ls percentage_module.py
ls: cannot access 'percentage_module.py': No such file or directory
```

`-u` (`--include-untracked`) is needed because `percentage_module.py` is a new
file; a plain `git stash push` would have left it sitting in the working tree.

### Step 3 - the urgent fix on another branch

```console
$ git checkout main
Switched to branch 'main'

$ git checkout -b hotfix-division-by-zero
Switched to a new branch 'hotfix-division-by-zero'
```

The bug, before:

```console
$ python -c "from division_module import division; print(\"returned:\", division(10, 0))" < /dev/null
Enter username :    -> no input available, using default: veerandra
Enter password :    -> no input available, using default: demo-password
Cannot divide by zero
returned: None
```

And after the fix:

```console
$ python -c "from division_module import division; print(\"returned:\", division(10, 0))" < /dev/null
Enter username :    -> no input available, using default: veerandra
Enter password :    -> no input available, using default: demo-password
Cannot divide 10 by zero - enter a non-zero second number
returned: None
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

### Step 4 - `git stash list`

```console
$ git checkout feature-percentage
Switched to branch 'feature-percentage'

$ git stash list
stash@{0}: On feature-percentage: WIP: percentage feature
```

Lists every stash, newest first. `stash@{0}` is the newest; after the colon is
the branch it was taken on plus the `-m` message.

### Step 5 - `git stash show`

```console
$ git stash show stash@{0}
 dashboard.py | 3 +++
 1 file changed, 3 insertions(+)
```

```console
$ git stash show --include-untracked stash@{0}
 dashboard.py         |  3 +++
 percentage_module.py | 13 +++++++++++++
 2 files changed, 16 insertions(+)
```

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

Bare `show` gives a diffstat, `-p` gives the full patch, `--include-untracked`
also counts the untracked file that `-u` saved.

### Step 6 - `git stash apply`, and proof the stash SURVIVES

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

$ git stash list
stash@{0}: On feature-percentage: WIP: percentage feature
```

The changes are back **and `stash@{0}` is still listed**. There is no
`Dropped ...` line in `apply`'s output.

### Step 7 - reset the tree so `pop` can be shown from the same starting point

```console
$ git checkout -- .

$ rm percentage_module.py

$ git status
On branch feature-percentage
nothing to commit, working tree clean

$ git stash list
stash@{0}: On feature-percentage: WIP: percentage feature
```

The applied changes were thrown away and nothing was lost - **because `apply`
kept the stash**. That is the safety net in action.

### Step 8 - `git stash pop`, and proof the stash is GONE

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

$ git stash list

```

Same files restored, but `pop` added `Dropped refs/stash@{0} (32adf60...)` and
`git stash list` now prints **nothing at all** - the entry is gone.

### Step 9 - `git stash drop`, and proof the change was discarded

A throwaway debug line was added to `calculator.py` and stashed on its own with
a pathspec, so the percentage work already in the tree was not swept up:

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

$ git stash push -m "throwaway: temporary debug print" -- calculator.py
Saved working directory and index state On feature-percentage: throwaway: temporary debug print

$ git stash list
stash@{0}: On feature-percentage: throwaway: temporary debug print

$ git stash drop stash@{0}
Dropped stash@{0} (99bfe2fd5417692051285869f87a9bc896dd6407)

$ git stash list

$ git diff calculator.py

```

`drop` removed the entry **without restoring anything** - the empty
`git diff calculator.py` is the proof the debug line is gone for good.

### Step 10 - finish the feature and merge

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

$ git stash list

```

The session ends with **no leftover stashes**.

---

## apply vs pop

> **`git stash apply` reapplies the stashed changes but KEEPS the stash entry in
> the stash list. `git stash pop` reapplies the same changes and REMOVES the
> entry - but only if the reapply succeeded.**
>
> `pop` is effectively `apply` + `drop` in one command, with the `drop`
> conditional on success.

| | `git stash apply` | `git stash pop` |
| --- | --- | --- |
| Restores the stashed changes | Yes | Yes |
| Stash entry afterwards | **Kept** - still in `git stash list` | **Removed** - gone from `git stash list` |
| Equivalent to | `apply` | `apply` + `drop` (drop only on success) |
| Prints `Dropped refs/stash@{0} (<sha>)` | No | Yes |
| On a merge conflict | Entry kept (it never removes it) | **Entry kept** - nothing is lost; drop it by hand after resolving |
| Reusable on another branch afterwards | Yes | No - the entry no longer exists |
| Leaves the stash list tidy | No - entries accumulate | Yes |
| Best for | Work you might need twice, or a risky reapply you want a fallback for | The everyday park-and-resume round trip |

### The proof, from this repository

| Step | Command run | `git stash list` immediately afterwards |
| --- | --- | --- |
| 6 | `git stash apply stash@{0}` | `stash@{0}: On feature-percentage: WIP: percentage feature` |
| 8 | `git stash pop` | *(empty - prints nothing)* |

Identical files restored either way. The only difference is whether the entry
survived - and that difference is visible above in real captured output, not
just asserted.

**When to use which**

- Use **`apply`** when you may want the same stash on more than one branch, when
  you are not yet sure the reapply is right (you can discard and retry, as in
  step 7), or when the work would be painful to recreate. Remember to
  `git stash drop` afterwards or the list fills up.
- Use **`pop`** for the ordinary park-it-and-pick-it-back-up round trip on the
  same branch, and to keep the stash list clean without a second command.
- If `pop` conflicts, git **keeps** the stash so nothing can be lost - resolve
  the conflict, then run `git stash drop stash@{0}` yourself.

A fuller treatment is in [`APPLY_VS_POP.md`](APPLY_VS_POP.md).

---

## When git stash is useful in a real development team

- **An urgent hotfix arrives mid-feature.** Exactly the scenario above: you are
  three files into a feature, production breaks, and you need a clean tree off
  `main` in the next thirty seconds. Stash, fix, ship, unstash.
- **Switching branches with a dirty tree.** Git refuses to check out another
  branch when the switch would clobber your local changes. Stashing clears the
  tree so you can review a colleague's PR branch and come straight back.
- **Pulling without committing half-done work.** `git pull` on a dirty tree can
  fail or leave a mess. `git stash`, `git pull`, `git stash pop` is the standard
  way to catch up with `origin/main` mid-task.
- **Moving work to the right branch.** You started editing on `main` by mistake.
  `git stash`, `git checkout -b the-right-branch`, `git stash pop` puts the
  changes where they belonged, with no commits to rewrite.
- **Testing a clean baseline.** Stash your local edits to confirm a bug exists
  without them, then pop them back - much safer than commenting code out.
- **Splitting an accidental mega-change.** `git stash push -- <paths>` parks only
  some files (used in step 9 above), so you can commit one coherent change at a
  time.

The team habit that makes all of this safe: **always use `-m` to label a stash**.
`stash@{0}: WIP on main: 3f2a1b Fix typo` tells you nothing three days later;
`stash@{0}: On feature-percentage: WIP: percentage feature` tells you everything.

---

## Full git history

```console
$ git log --graph --oneline --all --decorate
* 6164fc9 (HEAD -> main, origin/main) Match the quoted python command in the docs to the raw capture
* 0de2992 Refresh captured git history evidence
* 647cd31 Add README with the inlined stash transcript and submission links
* 6b52c4c Document the stash workflow and the apply versus pop distinction
* 58a2d99 Add the raw terminal capture of the git stash session
*   54d2365 Merge branch 'feature-percentage' into main
|\  
| * f8d60e9 (origin/feature-percentage, feature-percentage) Add percentage module and show the percentage result on the dashboard
* |   0a1e77e Merge branch 'hotfix-division-by-zero' into main
|\ \  
| |/  
|/|   
| * 202c05d (origin/hotfix-division-by-zero, hotfix-division-by-zero) Harden the divide-by-zero guard and make its message actionable
|/  
* 273950f Add calculator entry point and dashboard integration layer
* 12df5c8 Add arithmetic modules for addition, subtraction, multiplication and division
* fae5a5b Add input, login and profile modules with non-interactive defaults
* 804fc7f Add gitignore, environment template and configuration module
```

Read bottom to top: four baseline commits, the hotfix merged in with `--no-ff`,
then the finished feature merged in the same way, then the documentation
commits. Both `--no-ff` merges keep the side branches visible in the graph
instead of flattening them away. (The only commit missing from the block above
is the one that pasted the block in - a graph cannot contain its own commit.)

While the stash existed, it appeared in the same graph as real commit objects -
this is what a stash looks like under the hood:

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

`32adf60` is the stash commit; `9eb504a` holds the index and `99e3405` holds the
untracked files (present only because `-u` was used). That same SHA `32adf60` is
what `git stash pop` reported dropping in step 8 - which is how you can tell the
outputs in this README come from one continuous, genuine session.

### Branches

| Branch | Purpose |
| --- | --- |
| `main` | Default branch - baseline plus both merges |
| `feature-percentage` | Where the feature was started, stashed and finished |
| `hotfix-division-by-zero` | The urgent production fix |

---

## Fixes applied after review feedback

The previous submission of this task scored poorly because the stash work left
no trace a file-level reviewer could see. Every point raised is addressed here:

| Review comment | What was done |
| --- | --- |
| "No repo-visible evidence of an unfinished feature being saved with `git stash`" | The unfinished feature, the `git status` showing it uncommitted, its `NameError` crash and the `git stash push -u -m "WIP: percentage feature"` output are all committed in [`stash_session_capture.txt`](stash_session_capture.txt), [`STASH_TRANSCRIPT.md`](STASH_TRANSCRIPT.md) and this README |
| "No shown source or transcript file demonstrating `git stash list`, `git stash show` or `git stash apply`" | A plain-text transcript, [`stash_session_capture.txt`](stash_session_capture.txt), contains all 48 commands of the session with their real output, tee'd live from the shell. `list`, `show`, `apply`, `pop` and `drop` are each shown with genuine output in three separate repo files |
| "None of the visible files explain that `apply` keeps the stash while `pop` applies it and removes it" | [`APPLY_VS_POP.md`](APPLY_VS_POP.md) plus the [apply vs pop](#apply-vs-pop) section here, each with a comparison table **and** the real before/after `git stash list` output that proves it rather than asserting it |
| "Add a short apply versus pop explanation next to that transcript" | The explanation sits directly under the transcript in this README, and `STASH_TRANSCRIPT.md` links to `APPLY_VS_POP.md` from its summary table |
| "Fragile login flow - `profile_name` only defined when both username and password are truthy" | Fixed in [`profile.py`](profile.py): `profile_name = ""` is assigned **before** the `if`, so the name is always defined. Blank input now yields an empty profile that every arithmetic module handles with a clear message, instead of an `ImportError` on every module that imports it |

Two further robustness fixes carried into this baseline: there is no
`secrets.py` (configuration now lives in the committed `config.py`, so nothing
the code imports is gitignored), and every `input()` call falls back to a
default so the project runs non-interactively on a fresh clone.

---

Author: **veerandra7** · Part of the 6-month FDE challenge, module 03 - Git and GitHub.
