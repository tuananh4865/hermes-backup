# GitHub PR Workflow Reference

Formerly a standalone skill. Content absorbed into `github-operations`.

## Standard PR Lifecycle

```bash
# 1. Create branch
git checkout -b feature/my-feature

# 2. Make changes and commit
git add .
git commit -m "feat: add new feature"

# 3. Push and create PR
git push -u origin feature/my-feature
gh pr create --title "feat: add new feature" --body "Description" --reviewer owner

# 4. Check CI status
gh pr checks

# 5. Merge (squash merge)
gh pr merge --squash

# 6. Delete branch
git branch -d feature/my-feature
git push origin --delete feature/my-feature
```

## PR from Fork

```bash
# Clone fork
gh repo clone your-username/repo
cd repo

# Add upstream
git remote add upstream https://github.com/original-owner/repo.git

# Create PR
git checkout -b feature
# make changes
git push your-username feature
gh pr create --repo original-owner/repo
```

## Sync Fork with Upstream

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push
```
