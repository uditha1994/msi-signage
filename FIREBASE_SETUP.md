# Firebase Authentication Setup

The admin panel is protected by a login page. The Firebase config is stored in a `.env` file (never committed to git) and loaded by the server at startup.

---

## Step 1 — Create a Firebase project

1. Go to https://console.firebase.google.com
2. Sign in with a Google account
3. Click **Add project**
4. Name it (e.g. `msi-signage`), click **Continue**
5. Turn **off** Google Analytics — not needed
6. Click **Create project**, wait, click **Continue**

## Step 2 — Enable Email/Password login

1. Left menu → **Build → Authentication**
2. Click **Get started**
3. Click the **Sign-in method** tab
4. Click **Email/Password**, turn on the first switch, click **Save**

## Step 3 — Add admin users

1. **Authentication → Users** tab
2. Click **Add user**, enter email (e.g. `admin@msi.lk`) and password
3. Repeat for each staff member

## Step 4 — Get your web config

1. Gear icon (⚙) next to "Project Overview" → **Project settings**
2. Scroll to **Your apps** → click web icon `</>`
3. Give it a nickname, click **Register app**
4. Copy the values from the `firebaseConfig` block

## Step 5 — Create your `.env` file

In the project folder, copy `.env.example` to `.env`:

```
cp .env.example .env
```

Open `.env` and paste your Firebase values:

```
FIREBASE_API_KEY=AIzaSyABC123...
FIREBASE_AUTH_DOMAIN=msi-signage.firebaseapp.com
FIREBASE_PROJECT_ID=msi-signage
FIREBASE_STORAGE_BUCKET=msi-signage.appspot.com
FIREBASE_MESSAGING_SENDER_ID=123456789
FIREBASE_APP_ID=1:123456789:web:abc123
```

Save the file. `.env` is in `.gitignore` — it will not be committed.

**Restart the server** (Ctrl+C, then start again) so the new values load.

## Step 6 — Authorize your domain (network access)

If you open the admin panel from another PC by IP (e.g. `http://192.168.1.105:5000`), Firebase needs to allow that.

1. Firebase Console → **Authentication → Settings → Authorized domains**
2. Click **Add domain** and add your PC's IP

If you only open the admin panel as `localhost` on the server PC, skip this step.

---

## Done!

Open `http://localhost:5000` — you'll see the login page. Sign in with the email/password from Step 3.

- The **TV Display** (`/display`) does not require login.
- Use the **Logout** button (top-right) to log out.
- To add/remove staff later: **Authentication → Users** in the Firebase Console.

## How it works

- `server.py` reads `.env` at startup, exposes config via `/api/firebase-config`.
- `login.html` and `admin.html` fetch the config at page load — no hardcoded keys.
- You can safely commit all `.html`, `.py`, `.md` files to git. Only `.env` is secret.
- If `.env` is missing, the server returns `configured: false` and the admin panel runs without auth (with a console warning) so you can still set things up.
