# GitHub Repository Management Reference

Formerly a standalone skill. Content absorbed into `github-operations`.

## Clone / Create / Fork

```bash
# Clone
gh repo clone owner/repo

# Create new repo
gh repo create my-repo --public --clone

# Fork
gh repo fork owner/repo
```

## Nested Repo Backup

For backing up large directories (wikis, knowledge bases) into GitHub with proper .gitignore:

```bash
# In the large directory
cd /path/to/large-wiki

# Initialize with .gitignore for nested .git dirs
git init
echo "*/.git" >> .gitignore
git add .
git commit -m "Initial commit"

# Add remote and push
git remote add origin https://github.com/user/repo.git
git push -u origin main
```

**CRITICAL for nested repos:** Before committing, ensure `*/.git` is in .gitignore to avoid embedding nested .git directories.

## Releases

```bash
# Create release
gh release create v1.0.0 --title "Release v1.0.0" --notes "Release notes"

# Upload assets
gh release upload v1.0.0 ./dist/bin --clobber
```
