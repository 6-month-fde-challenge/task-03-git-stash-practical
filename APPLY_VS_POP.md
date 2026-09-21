# `git stash apply` vs `git stash pop`

## The one-sentence answer

**`git stash apply` reapplies the stashed changes to the working tree but KEEPS
the stash entry in the stash list. `git stash pop` reapplies exactly the same
changes and then REMOVES the stash entry - but only if the apply succeeded.**

In other words, `git stash pop` is `git stash apply` followed by
`git stash drop`, executed as a single command, with the drop conditional on the
apply going through cleanly.

---

## Comparison table

| | `git stash apply` | `git stash pop` |
| --- | --- | --- |
| Restores the stashed changes into the working tree | Yes | Yes |
| Stash entry afterwards | **Kept** - still in `git stash list` | **Removed** - gone from `git stash list` |
| Equivalent to | `apply` | `apply` + `drop` (drop only on success) |
| Prints `Dropped refs/stash@{0} (<sha>)` | No | Yes |
| If the reapply hits a **merge conflict** | Stash kept (it was never going to be removed) | **Stash is kept**, so nothing is lost; resolve, then `git stash drop` by hand |
| Can be reused on another branch afterwards | Yes - the entry is still there | No - you would have to recreate it |
| Default target when no argument is given | `stash@{0}` | `stash@{0}` |
| Risk of losing the parked work | Low - the entry survives a bad reapply | Low, but the entry is gone once it succeeds |
| Leaves the stash list tidy | No - entries pile up | Yes |

---

## Proof from this repository's real session

These are verbatim outputs from the session captured in
[`STASH_TRANSCRIPT.md`](STASH_TRANSCRIPT.md) and
[`stash_session_capture.txt`](stash_session_capture.txt). The same stash was
applied first, then reset, then popped, so the two commands are compared on
identical input.

### `apply` - before and after

Before:

```console
$ git stash list
stash@{0}: On feature-percentage: WIP: percentage feature
```

The command:

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

After:

```console
$ git stash list
stash@{0}: On feature-percentage: WIP: percentage feature
```

**The entry is still there.** Note there is no `Dropped ...` line anywhere in
the output.

### `pop` - before and after

Before (the working tree had been reset back to clean, and the same stash was
still present precisely *because* `apply` had kept it):

```console
$ git stash list
stash@{0}: On feature-percentage: WIP: percentage feature
```

The command:

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

After:

```console
$ git stash list

```

**The list is empty** - `git stash list` prints nothing at all when no stashes
remain. The extra line `Dropped refs/stash@{0} (32adf60...)` is `pop` telling
you it deleted the entry; `32adf60` is the real stash commit that appeared as
`(refs/stash)` in `git log --graph --all` earlier in the session.

### Side by side

| Step | Command run | `git stash list` immediately after |
| --- | --- | --- |
| 6 | `git stash apply stash@{0}` | `stash@{0}: On feature-percentage: WIP: percentage feature` |
| 8 | `git stash pop` | *(empty - no output)* |

Identical files restored in both cases. The only difference is whether the stash
entry survived.

---

## When to use which

### Use `git stash apply` when

- **You want the changes on more than one branch.** Apply the same stash to a
  second branch afterwards - the entry is still there to reuse.
- **You are not sure the reapply is what you want.** If the result is wrong you
  can `git checkout -- .`, throw everything away and try again, because the
  stash is untouched. This is exactly what was done in step 7 of the transcript.
- **The stash is precious and hard to recreate**, for example an hour of
  exploratory work.
- **You are applying onto a branch that has moved on a lot** and you expect
  conflicts.

Remember to run `git stash drop stash@{0}` yourself once you are happy, or the
stash list slowly fills up with entries nobody dares delete.

### Use `git stash pop` when

- **It is a straightforward "park it and pick it back up" round trip** on the
  same branch - the common case, and what this project's percentage feature did.
- **You want the stash list to stay clean** without a second command.
- **You are certain you only need the changes once.**

### A word on conflicts

If `git stash pop` hits a merge conflict it does **not** drop the stash - git
deliberately keeps the entry so the work cannot be lost while you are resolving.
After resolving the conflict you must drop it manually:

```
git stash drop stash@{0}
```

Otherwise you are left with a stale duplicate of work that is already in your
tree.

### And `git stash drop`

`git stash drop stash@{0}` removes an entry **without restoring anything** - the
"no thanks" option, used in the transcript to bin a throwaway debug print:

```console
$ git stash drop stash@{0}
Dropped stash@{0} (99bfe2fd5417692051285869f87a9bc896dd6407)

$ git stash list

$ git diff calculator.py

```

The empty `git diff` afterwards is the proof that the change was discarded, not
reapplied.

---

## Rule of thumb

> `pop` for the everyday round trip. `apply` when you might need the stash
> again, or when you want a safety net while you find out whether the reapply is
> right.
