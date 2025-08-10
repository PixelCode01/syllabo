# Fix GitHub Permissions for Releases

If you're getting a 403 error when creating releases, follow these steps:

## 1. Enable GitHub Actions Permissions

1. Go to your repository on GitHub
2. Click **Settings** tab
3. In the left sidebar, click **Actions** → **General**
4. Under **Workflow permissions**, select:
   - ✅ **Read and write permissions**
   - ✅ **Allow GitHub Actions to create and approve pull requests**
5. Click **Save**

## 2. Check Repository Settings

1. Go to **Settings** → **General**
2. Scroll down to **Features**
3. Make sure **Issues** and **Wiki** are enabled (sometimes required for releases)

## 3. Verify Token Permissions

The workflow uses `GITHUB_TOKEN` which should have these permissions:
- `contents: write` - To create releases
- `packages: write` - To upload artifacts
- `actions: read` - To read workflow information

## 4. Alternative: Use Personal Access Token

If the above doesn't work, create a Personal Access Token:

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click **Generate new token (classic)**
3. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `write:packages` (Upload packages)
4. Copy the token
5. Go to your repository → Settings → Secrets and variables → Actions
6. Click **New repository secret**
7. Name: `RELEASE_TOKEN`
8. Value: Your personal access token
9. Update the workflow to use `token: ${{ secrets.RELEASE_TOKEN }}`

## 5. Test the Fix

After making changes:
1. Delete the current tag: `git tag -d v1.0.0 && git push origin --delete v1.0.0`
2. Create a new tag: `git tag -a v1.0.1 -m "Test release" && git push origin v1.0.1`
3. Check the Actions tab for successful release creation

## Common Issues

- **403 Forbidden**: Usually permissions issue - follow steps 1-2 above
- **422 Validation Failed**: Tag might already exist - delete and recreate
- **404 Not Found**: Repository might be private and token lacks access

## Quick Fix Command

Run this to recreate the release:

```bash
# Delete old tag
git tag -d v1.0.0
git push origin --delete v1.0.0

# Create new tag
git tag -a v1.0.1 -m "Release v1.0.1"
git push origin v1.0.1
```