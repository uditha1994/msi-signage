# MSI Campus Digital Signage System

A local network digital signage system for **Management & Science Institute (MSI)** campus. Displays the daily classroom timetable on a Smart TV, with support for event photo/video slideshows.

Built with Python (Flask) for the backend and plain HTML/JS for the frontend — no internet required after setup.

---

## Features

- **Weekly timetable** — enter sessions for each day (Mon–Sun) per venue
- **Auto day detection** — TV display automatically shows today's timetable
- **Live clock** — current time shown on screen, with green highlight on the active session
- **Media slideshow** — upload photos or videos for events; plays between timetable views
- **Weekly templates** — save the full week as a named template and reload it any week
- **Autocomplete** — program, subject, and lecturer fields suggest from a saved preset list
- **Network access** — admin panel and TV display both accessible from any device on the same WiFi

---

## Project Structure

```
msi-signage/
├── server.py            # Flask backend — API + file serving
├── admin.html           # Admin panel — edit timetable, upload media, manage templates
├── display.html         # TV display — full-screen timetable + media slideshow
├── requirements.txt     # Python dependencies
├── START_SERVER.bat     # One-click start for Windows
├── START_AS_ADMIN.bat   # Same, but requests admin rights (needed for firewall)
└── public/
    ├── msi_white.png    # MSI logo (white, for dark header)
    ├── msu_white.png    # MSU logo (white, for dark header)
    └── media/           # Uploaded photos and videos (auto-created)
```

Data files are created automatically on first run:
- `timetable_data.json` — current week's schedule
- `presets.json` — autocomplete lists for programs, subjects, lecturers
- `templates_data.json` — saved weekly templates

---

## Requirements

- **Python 3.10+** — [python.org](https://www.python.org/downloads/)
- **Windows** (tested) — also works on Mac/Linux with minor adjustments
- Smart TV or Chromecast on the same WiFi network as the PC running the server

---

## Setup

**1. Install Python**

Download from [python.org](https://www.python.org/downloads/) and install. During installation, check **"Add Python to PATH"**.

**2. Install dependencies**

Open a terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

**3. Start the server**

On Windows, double-click `START_AS_ADMIN.bat` (runs as administrator so the firewall rule is added automatically).

Or run manually:

```bash
python server.py
```

The terminal will show:

```
Admin Panel  : http://localhost:5000
TV Display   : http://192.168.x.x:5000/display
```

The admin panel opens automatically in your browser.

---

## Usage

### Admin Panel — `http://localhost:5000`

**Weekly Timetable tab**
- Click a day (Mon–Sun) to switch to that day
- Click **+ Add Session** on any venue row to add a lecture slot
- Enter start time, end time, program, subject, and lecturer
- Fields show autocomplete suggestions as you type
- Click **💾 Save Day** when done

**Templates tab**
- Enter a name and click **💾 Save Full Week** to save all 7 days as a template
- Load a saved template any week with **⬇ Load**
- Useful when the weekly schedule repeats

**Photos & Videos tab**
- Drag and drop or click to upload images or videos
- Supported formats: JPG, PNG, GIF, MP4, WEBM, MOV
- Uploaded files play as a slideshow on the TV between timetable views

**Presets tab**
- Manage the autocomplete lists for programs, subjects, and lecturers
- New values typed in the timetable are saved to presets automatically

**Settings tab**
- Set how long the timetable stays on screen before switching to media (default: 30 seconds)
- Set how long each photo/video shows (default: 8 seconds)

---

### TV Display — `http://[PC-IP]:5000/display`

Open this URL on the Smart TV browser or cast it via Chromecast.

- Automatically detects today's day and shows that day's timetable
- Currently active session is highlighted in green
- Switches to media slideshow if photos/videos are uploaded, then returns to timetable
- Refreshes data every 60 seconds — timetable changes appear automatically

**To find your PC's IP address on Windows:**
1. Press `Win + R`, type `cmd`, press Enter
2. Type `ipconfig` and press Enter
3. Look for **IPv4 Address** — e.g. `192.168.1.105`
4. Open `http://192.168.1.105:5000/display` on the TV

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/data` | Full app data (week, media, settings) |
| POST | `/api/timetable` | Save one day's timetable |
| GET | `/api/presets` | Get autocomplete lists |
| POST | `/api/presets` | Add or update presets |
| GET | `/api/templates` | List saved templates |
| POST | `/api/templates/save-week` | Save full week as template |
| GET | `/api/templates/load/<name>` | Load a template |
| DELETE | `/api/templates/delete/<name>` | Delete a template |
| POST | `/api/media/upload` | Upload a photo or video |
| DELETE | `/api/media/delete/<id>` | Delete a media file |
| POST | `/api/settings` | Update display settings |
| GET | `/api/network-info` | Get server IP and URLs |

---

## Venues

The system has 8 predefined venues:

- 5th Floor Lecture Hall
- 4th Floor Lecture Hall A / B
- 3rd Floor Lecture Hall A / B
- 2nd Floor Computer Lab
- 2nd Floor Bio-Lab
- Basement Research Room

---

## Troubleshooting

**Smart TV cannot connect**
- Make sure the PC and TV are on the same WiFi network
- Run `START_AS_ADMIN.bat` so the Windows firewall allows port 5000
- Use the IP shown in the admin panel banner, not `localhost`

**Admin panel won't open**
- Check that Python is installed and added to PATH
- Re-run `START_SERVER.bat` and look for error messages in the terminal

**Timetable not updating on TV**
- The TV display refreshes every 60 seconds automatically
- If it still doesn't update, reload the page on the TV browser

**Logo not showing**
- `msi_white.png` and `msu_white.png` must be in the `public/` folder
- Check the `public/` folder exists after extracting the zip

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask, Flask-CORS |
| Frontend | HTML, CSS, Vanilla JavaScript |
| Data storage | JSON files (no database needed) |
| Fonts | Google Fonts — Inter, Roboto Condensed |

---

## License

Internal use — Management & Science Institute (MSI), Sri Lanka.
