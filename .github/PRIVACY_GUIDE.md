# Keeping Your GitHub Repository Private

This guide explains how to ensure your repositories stay private.

## How to Make a Repository Private

1. Go to your repository on GitHub
2. Click **Settings** tab (top of the repository page)
3. Scroll down to the **Danger Zone** section at the bottom
4. Click **Change visibility**
5. Select **Make private**
6. Confirm by typing the repository name

## How to Create a Private Repository

When creating a new repository:
1. Click the **+** icon in the top right on GitHub
2. Select **New repository**
3. Under **Visibility**, choose **Private**

## Automated Monitoring (This Repository)

This repository has a GitHub Actions workflow (`.github/workflows/check-repo-visibility.yml`) that:
- Runs **daily at 8:00 AM UTC**
- Checks if the repository is private
- **Creates a GitHub Issue alert** if the repo is ever made public accidentally

You can also trigger it manually:
1. Go to the **Actions** tab in your repository
2. Click **Check Repository Visibility**
3. Click **Run workflow**

## Good Practices

- Regularly review your repositories at https://github.com/nawafshrf?tab=repositories
- Never commit sensitive data (passwords, API keys, tokens) — even in private repos
- Use `.gitignore` to exclude sensitive files
