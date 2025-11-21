# Remove Secrets from Git History

## 🚨 Problem

GitHub detected Google OAuth credentials in commit `8fec0cb` and blocked the push. The secrets are in the git history even though we've removed them from the current file.

## ✅ Solution Options

### Option 1: Use GitHub's Allow Secret (Quickest)

1. **Visit the GitHub link:**
   - Client ID: https://github.com/thatdeveloperkokou/era-bot-group3/security/secret-scanning/unblock-secret/35ji6LE5vGnJjzCtpRxhvkcv20M
   - Client Secret: https://github.com/thatdeveloperkokou/era-bot-group3/security/secret-scanning/unblock-secret/35ji6M8e0V6xYLkwdoOsR9MwDVC

2. **Click "Allow secret"** on both pages
3. **Push again:**
   ```bash
   git push origin main
   ```

**Note:** This allows the secret in git history, but it's already exposed. For better security, use Option 2.

---

### Option 2: Remove from Git History (Recommended)

**Use git filter-branch to remove secrets from history:**

```bash
# Remove the file from that commit
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch GOOGLE_CLIENT_ID_SETUP.md" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (WARNING: This rewrites history)
git push origin --force --all
```

**⚠️ Warning:** This rewrites git history. Only do this if you're the only one working on this branch.

---

### Option 3: Create New File Without Secrets

1. **Delete the file:**
   ```bash
   git rm GOOGLE_CLIENT_ID_SETUP.md
   git commit -m "Remove file with secrets"
   ```

2. **Create new file with placeholders** (already done)

3. **Push:**
   ```bash
   git push origin main
   ```

---

## 🎯 Recommended: Option 1 (Quickest)

Since the secrets are already in the commit, the quickest solution is to use GitHub's "Allow secret" feature. The Client ID is meant to be public anyway (it's used in frontend code), and the Client Secret isn't needed for our implementation.

---

## 📝 For Future Reference

**Never commit secrets to git!** Always:
- Use environment variables
- Use `.gitignore` for config files
- Use placeholders in documentation
- Store secrets in Railway/Vercel environment variables

---

**I recommend Option 1 - use GitHub's allow secret feature to unblock the push!** 🚀

