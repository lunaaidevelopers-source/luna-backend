# Render environment variables - copy/paste

Add the following environment variables in the Render dashboard for the Luna Backend service. Replace placeholders with your real values.

- DEBUG=false
- FIREBASE_CREDENTIALS_JSON=<paste-full-service-account-json-here>
- FRONTEND_URL=https://luna-frontend-three.vercel.app
- FRONTEND_URLS=https://luna-frontend-three.vercel.app
- GEMINI_API_KEY=<your_gemini_api_key>
- STRIPE_PUBLISHABLE_KEY=pk_test_...
- STRIPE_SECRET_KEY=sk_test_...
- STRIPE_WEBHOOK_SECRET=whsec_...  # if you use Stripe webhooks
- RATE_LIMIT_STORAGE=memory://

Notes:
- If you prefer to upload the Firebase JSON as a secret/file, set FIREBASE_CONFIG_PATH to its path and do not paste the raw JSON into an env var.
- Ensure the Render service Start Command is empty so it uses the Procfile, or set the Start Command to the same gunicorn line in the Procfile.
- After saving, click "Save, rebuild, and deploy" to apply changes.
