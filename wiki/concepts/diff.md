---
title: "Diff"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [git, algorithms, diff, version-control]
---

# Diff

## Overview

Diff (short for "difference") refers to algorithms and tools that compute the differences between two text documents or data sets. In software development, diff is fundamental to understanding what changed between versions of code. At its core, a diff algorithm takes two sequences (typically lines of text) and produces a set of edit operations—additions, deletions, and modifications—that transform the first sequence into the second. The output, often called a "diff" or "patch," forms the foundation for version control systems, collaborative editing tools, and automated code review pipelines. Diff tools typically present changes in a structured format showing which lines were added (prefixed with `+`), removed (prefixed with `-`), or unchanged. Modern diff engines go beyond line-level comparison to perform word-level or character-level diffing, providing more granular insight into changes such as moved code blocks or refactored functions.

## Algorithms

Several classic algorithms power modern diff tools:

**Myers Algorithm** — Developed by Eugene Myers in 1986, this algorithm finds the shortest edit script (SES) between two sequences in O(ND) time complexity, where N is the total input size and D is the edit distance. It is the basis for many contemporary diff implementations, including those in Git. Myers' algorithm excels at finding a optimal (minimal) set of changes but can struggle with large inputs due to quadratic space requirements in its naive form.

**Hunt-McIlroy Algorithm** — Created by James Hunt and M. Douglas McIlroy at Bell Labs in the 1970s, this algorithm powers the original Unix `diff` command. It identifies the longest common subsequence (LCS) between two files to determine what remains unchanged, then treats everything else as modified. The algorithm builds a "hashed" representation of lines for efficient comparison but was later superseded in many use cases by Myers' more efficient approach.

**Longest Common Subsequence (LCS)** — LCS is not a single algorithm but a foundational concept underlying both Hunt-McIlroy and many other diff approaches. The longest common subsequence between two documents represents the largest set of elements that appear in the same order in both texts. Finding the LCS is a classic dynamic programming problem with O(MN) time complexity, where M and N are the lengths of the two sequences. Many practical diff tools use heuristics or divide-and-conquer strategies to approximate LCS more efficiently.

## Use Cases

**Version Control** — Diff is the backbone of every version control system. Git stores snapshots as complete file contents, but its `git diff` command computes and displays differences on demand. Every commit represents a diff from the previous state, enabling developers to review history, understand changes, and reconstruct any previous version by applying patches in sequence.

**Merge Conflicts** — When multiple developers modify the same code simultaneously, diff algorithms help identify overlapping changes. Merge tools display three-way diffs showing the original file, the local changes, and the incoming changes, making it possible to manually or automatically resolve conflicts.

**Code Review** — Platforms like GitHub, GitLab, and Bitbucket use diff views to present pull request or merge request changes. Reviewers can inspect exactly which lines changed, comment on specific lines, and approve or request modifications based on the diff output.

**Patch Application** — The Unix `patch` utility applies diff output (patches) to transform one version of a file into another. This enables distributed workflows where changes are shared as text files rather than binary blobs.

## Related

- [[git]]
- [[version-control]]
- [[merge-conflicts]]
- [[code-review]]
- [[patch]]
