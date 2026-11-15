# Static website hosting

This directory is a standalone HTML/CSS/JavaScript demo. No Python, build step,
API keys, or paid server is required. Open `index.html` directly to try it locally.
Fonts use Google Fonts when online, with local fallback fonts when offline.

## GitHub Pages

1. Commit and push the `docs` directory to your intended GitHub repository.
2. In that repository, open **Settings → Pages**.
3. Under **Build and deployment**, select **Deploy from a branch**.
4. Choose the branch containing these files and the **/docs** folder, then Save.
5. GitHub will display the published website URL when deployment completes.

Official instructions: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

Only publish this directory. Never copy `.env` or cloud credentials into it.
Relative asset paths support GitHub Pages repository URLs and custom domains.
You can also upload this directory to any static web host.

## What the demo does

- Shows the existing sample authentication bug and a predefined Python fix.
- Runs four actual JavaScript checks on equivalent login logic before and after the fix.
- Lets visitors review, approve locally, download the Python proposal, and reset.
- Keeps all demo state in memory; refreshing resets it.

It does not execute Python, use Gemini, fix arbitrary submitted code, or push to GitHub.
The existing FastAPI application remains available separately via `python run_local.py`.
Real AI debugging requires a separately hosted backend; never embed an AI API key
in public frontend JavaScript.
