# Advanced Git Operations

This note records a cherry-pick and stash exercise on two isolated branches.

## Cherry-pick source

- Source branch: `feature-cherry-source`.
- Target branch: `feature-cherry-target`.
- The source commit adds this exercise note; its hash is recorded on the target branch.
- The target applies the source commit with `git cherry-pick <commit-hash>`.
