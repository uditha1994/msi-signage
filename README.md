# MSI Campus Digital Signage System

A local-network digital signage system for **Management & Science Institute (MSI)**. Shows the daily classroom timetable on a Smart TV, with lecturer photos, lesson details, event slideshows, and a special meeting mode.

Backend: Python (Flask). Frontend: plain HTML/JS. Login: Firebase Authentication.

---

## Features

- **Login protection** — admin panel secured with Firebase email/password auth
- **Weekly timetable** — separate schedule for each day (Mon–Sun)
- **Auto day detection** — TV automatically shows today's timetable
- **Program → Module → Lesson** — pick the program, then its module, then the day's lesson
- **Lecturer profiles** — add lecturers with photos; photos show on the TV timetable
- **Excel import** — bulk-load programs, modules, lessons, and lecturers from a spreadsheet
- **Special Meeting mode** — replace the whole display with a meeting screen (title, message, photos/videos), then switch back to normal
- **Media slideshow** — event photos/videos play between timetable views
- **Weekly templates** — save the full week and reload it any time
- **Auto fullscreen** — display goes fullscreen (tap once if the browser blocks it)
- **Network access** — open the TV display on any device on the same WiFi

---

## Quick Start

1. **Install Python 3.10+** from https://www.python.org/downloads/ (check "Add Python to PATH")
2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
3. **Set up Firebase login** — follow `FIREBASE_SETUP.md` (about 5 minutes)
4. **Start the server:**
   - Windows: double-click `START_AS_ADMIN.bat`
   - Mac/Linux: `./start_server.sh` (or `python3 server.py`)
5. The admin login page opens at `http://localhost:5000`

---

## Using the Admin Panel

| Tab | What it does |
|-----|--------------|
| **📋 Weekly Timetable** | Edit each day's sessions. Pick venue → add session → choose program, module, lesson, lecturer, and times. Save each day. |
| **📚 Programs & Lessons** | Manage the program/module/lesson catalog. Import everything from Excel. |
| **👤 Lecturers** | Add lecturers and upload profile photos. |
| **📢 Special Meeting** | Create a meeting screen and show it on the TV. Stop it to return to normal. |
| **📁 Templates** | Save/load the full week as a named template. |
| **🖼️ Photos & Videos** | Upload event media for the slideshow. |
| **⚙️ Settings** | Set how long the timetable and each slide stay on screen. |

---

## Excel Import Format

Create a spreadsheet with these columns (one sheet named anything):

| Program | Module | Code | Lesson | Lecturer |
|---------|--------|------|--------|----------|
| DCS 01 | Object Oriented Programming | CCS20704 | Introduction to OOP | Mr. Uditha Lashan |
| DCS 01 | Object Oriented Programming | CCS20704 | Classes and Objects | Mr. Uditha Lashan |
| DCS 01 | Database Management | CCS20203 | ER Diagrams | Ms. Dilini Fernando |

Repeat the program/module on each row. Use the **⬇ Sample Format** button in the app to download a starter file.

Advanced: you can also use separate sheets named `Programs`, `Modules`, `Lessons`, `Lecturers`.

---

## The TV Display

Open `http://[PC-IP]:5000/display` on the Smart TV browser (find the IP in the admin panel's top banner, or run `ipconfig` on Windows / `ipconfig getifaddr en0` on Mac).

- Shows today's timetable automatically
- Active session highlighted in green with a live indicator
- Lecturer photos shown next to names
- Switches to the media slideshow when event media is uploaded
- Shows the meeting screen instead when meeting mode is on
- Goes fullscreen automatically (tap once if prompted)

---

## Project Structure

```
msi-signage/
├── server.py            # Flask backend
├── login.html           # Firebase login page
├── admin.html           # Admin panel (protected)
├── display.html         # TV display
├── requirements.txt     # Python dependencies
├── FIREBASE_SETUP.md    # Auth setup guide
├── START_SERVER.bat     # Windows launcher
├── START_AS_ADMIN.bat   # Windows launcher (admin, opens firewall)
├── start_server.sh      # Mac/Linux launcher
└── public/
    ├── msi_white.png / msu_white.png   # logos for dark headers
    ├── msi_black.png / msu_black.png   # logos for login page
    ├── media/           # event slideshow files
    ├── profiles/        # lecturer photos
    └── meeting/         # special meeting media
```

Data files (auto-created): `timetable_data.json`, `presets.json`, `templates_data.json`, `catalog.json`, `lecturers.json`, `meeting.json`

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Login page shows "Firebase not configured" | Complete `FIREBASE_SETUP.md` and paste config into `login.html` + `admin.html` |
| Smart TV can't connect | PC and TV on same WiFi; run `START_AS_ADMIN.bat`; use IP not `localhost` |
| Login fails from another PC | Add that PC's IP to Firebase Authorized domains (see setup guide Step 6) |
| Port 5000 in use (Mac) | Turn off AirPlay Receiver, or change the port in `server.py` |
| Logos not showing | Keep the PNG files in `public/` |

---

*Management & Science Institute (MSI), Sri Lanka — internal use.*
