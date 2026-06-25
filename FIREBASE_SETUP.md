# Firebase Authentication Setup

The admin panel is protected by a login page. You need a free Firebase project to enable this. It takes about 5 minutes.

---

## Step 1 — Create a Firebase project

1. Go to https://console.firebase.google.com
2. Sign in with a Google account
3. Click **Add project** (or **Create a project**)
4. Name it (e.g. `msi-signage`), click **Continue**
5. You can turn **off** Google Analytics — it is not needed
6. Click **Create project**, wait, then click **Continue**

---

## Step 2 — Enable Email/Password login

1. In the left menu, click **Build → Authentication**
2. Click **Get started**
3. Click the **Sign-in method** tab
4. Click **Email/Password**
5. Turn on the first switch (**Email/Password**), click **Save**

---

## Step 3 — Add admin user accounts

1. Still in **Authentication**, click the **Users** tab
2. Click **Add user**
3. Enter the admin email (e.g. `admin@msi.lk`) and a password
4. Click **Add user**
5. Repeat for each staff member who should have access

> These are the email and password you will type on the login page.

---

## Step 4 — Get your web config

1. Click the **gear icon** (⚙) next to "Project Overview" → **Project settings**
2. Scroll down to **Your apps**
3. Click the **web icon** `</>`
4. Give it a nickname (e.g. `signage-web`), click **Register app**
5. You will see a `firebaseConfig` block like this:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyABC123...",
  authDomain: "msi-signage.firebaseapp.com",
  projectId: "msi-signage",
  storageBucket: "msi-signage.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abc123"
};
```

6. **Copy this whole block.**

---

## Step 5 — Paste the config into two files

You must paste the **same** config into **both** files. Open them in any text editor (Notepad works).

### File 1 — `login.html`

Find this block near the bottom (inside `<script type="module">`):

```javascript
const firebaseConfig = {
  apiKey: "PASTE_YOUR_API_KEY",
  authDomain: "PASTE_YOUR_PROJECT.firebaseapp.com",
  ...
};
```

Replace it with the config you copied from Firebase.

### File 2 — `admin.html`

Find the **same** `firebaseConfig` block near the top (inside the first `<script type="module">`) and replace it with the same config.

Save both files.

---

## Step 6 — Authorize your domain (for network access)

If you open the admin panel from another computer using the PC's IP address (e.g. `http://192.168.1.105:5000`), Firebase needs to allow that.

1. In Firebase Console → **Authentication → Settings** tab → **Authorized domains**
2. `localhost` is already allowed
3. Click **Add domain** and add your PC's IP address (e.g. `192.168.1.105`)

> If you only ever open the admin panel on the PC running the server (using `localhost`), you can skip this step.

---

## Done!

Now when you start the server and open `http://localhost:5000`, you will see the **login page**. Sign in with the email and password you created in Step 3.

- The **TV Display** (`/display`) does **not** require login — only the admin panel is protected.
- To log out, use the **Logout** button in the top-right of the admin panel.

---

## Notes

- If you skip this setup, the admin panel still works but shows a warning and is **not** protected. Anyone on the network could change the timetable. For real use, complete the setup.
- The Firebase free tier (Spark plan) is more than enough — email/password auth has no cost.
- To add or remove staff later, go to **Authentication → Users** in the Firebase Console.
