from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json, os, uuid, socket
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='public')
CORS(app)

DATA_FILE      = 'timetable_data.json'
PRESETS_FILE   = 'presets.json'
TEMPLATES_FILE = 'templates_data.json'
MEDIA_FOLDER   = 'public/media'
ALLOWED_EXT    = {'png','jpg','jpeg','gif','mp4','webm','mov'}
os.makedirs(MEDIA_FOLDER, exist_ok=True)

VENUES = [
    "5th Floor Lecture Hall",
    "4th Floor Lecture Hall A",
    "4th Floor Lecture Hall B",
    "3rd Floor Lecture Hall A",
    "3rd Floor Lecture Hall B",
    "2nd Floor Computer Lab",
    "2nd Floor Bio-Lab",
    "Basement Research Room"
]
DAYS = ['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY']

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80)); ip = s.getsockname()[0]; s.close(); return ip
    except: return '127.0.0.1'

# ── Data helpers ─────────────────────────────────────────────
def empty_week():
    return {day: {v: {"sessions": []} for v in VENUES} for day in DAYS}

def load_data():
    if not os.path.exists(DATA_FILE):
        d = {"active_day": "MONDAY", "week": empty_week(), "media": [],
             "settings": {"slide_interval": 8, "timetable_duration": 30}}
        save_data(d); return d
    with open(DATA_FILE) as f: return json.load(f)

def save_data(d):
    with open(DATA_FILE,'w') as f: json.dump(d, f, indent=2)

def load_presets():
    if not os.path.exists(PRESETS_FILE):
        p = {
            "programs":  ["DCS 01","DCS 02","BCS 01","BCS 02","DHTM 01","DHTM 02","DBMS 01","DBMS 02","PhD Sessions"],
            "subjects":  ["Introduction to Accounting","Introduction to Tourism","Introduction to Tour Operation",
                          "Information Technology","Organic Chemistry","Physical Chemistry","Data Structures",
                          "Object Oriented Programming","Database Management","Web Development",
                          "Research Methodology","Business Communication","Mathematics","Statistics"],
            "lecturers": ["Ms. Janani Perera","Mr. Imal Perera","Mr. Uditha Lashan","Ms. Fatema Shabbir Abbasbhoy",
                          "Ms. Upekshi Pavithra","Prof. Dr. Ali Khatibi","Mr. Kasun Silva","Ms. Dilini Fernando",
                          "Mr. Chamara Bandara","Ms. Nimesha Perera"]
        }
        with open(PRESETS_FILE,'w') as f: json.dump(p,f,indent=2)
        return p
    with open(PRESETS_FILE) as f: return json.load(f)

def save_presets(p):
    with open(PRESETS_FILE,'w') as f: json.dump(p, f, indent=2)

def load_templates():
    if not os.path.exists(TEMPLATES_FILE): return {}
    with open(TEMPLATES_FILE) as f: return json.load(f)

def save_templates(t):
    with open(TEMPLATES_FILE,'w') as f: json.dump(t, f, indent=2)

# ── API ──────────────────────────────────────────────────────
@app.route('/api/data')
def get_data():
    return jsonify(load_data())

@app.route('/api/network-info')
def network_info():
    ip = get_local_ip()
    return jsonify({'ip': ip, 'admin': f'http://{ip}:5000', 'display': f'http://{ip}:5000/display'})

@app.route('/api/presets')
def get_presets():
    return jsonify(load_presets())

@app.route('/api/presets', methods=['POST'])
def update_presets():
    p = load_presets(); body = request.json
    if '_replace' in body:
        for k,v in body['_replace'].items(): p[k] = v
    else:
        for key in ('programs','subjects','lecturers'):
            if key in body:
                val = body[key].strip()
                if val and val not in p[key]: p[key].append(val)
    save_presets(p); return jsonify({'ok':True})

# Save a single day's timetable
@app.route('/api/timetable', methods=['POST'])
def update_timetable():
    data = load_data(); body = request.json
    day  = body.get('day', data.get('active_day','MONDAY'))
    rows = body.get('rows', {})
    if 'week' not in data: data['week'] = empty_week()
    data['week'][day] = rows
    data['active_day'] = day
    # auto-save new values to presets
    p = load_presets(); changed = False
    for venue, vdata in rows.items():
        for sess in vdata.get('sessions', []):
            for field, pkey in [('program','programs'),('subject','subjects'),('lecturer','lecturers')]:
                val = sess.get(field,'').strip()
                if val and val not in p[pkey]: p[pkey].append(val); changed = True
    if changed: save_presets(p)
    save_data(data); return jsonify({'ok':True})

# Set which day the TV shows
@app.route('/api/active-day', methods=['POST'])
def set_active_day():
    data = load_data()
    day = request.json.get('day','MONDAY')
    if day in DAYS: data['active_day'] = day
    save_data(data); return jsonify({'ok':True})

# ── Templates ────────────────────────────────────────────────
@app.route('/api/templates')
def get_templates():
    return jsonify(load_templates())

@app.route('/api/templates/save-week', methods=['POST'])
def save_week_template():
    """Save entire week (all 7 days) as a named template"""
    body = request.json
    name = body.get('name','').strip()
    if not name: return jsonify({'error':'Name required'}),400
    data = load_data()
    templates = load_templates()
    templates[name] = {
        'week': data.get('week', empty_week()),
        'saved': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    save_templates(templates)
    return jsonify({'ok':True, 'name':name})

@app.route('/api/templates/save-day', methods=['POST'])
def save_day_template():
    """Save a single day's timetable as template"""
    body = request.json
    name = body.get('name','').strip()
    day  = body.get('day','MONDAY')
    if not name: return jsonify({'error':'Name required'}),400
    data = load_data()
    templates = load_templates()
    templates[name] = {
        'day': day,
        'rows': data.get('week',{}).get(day,{}),
        'saved': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    save_templates(templates)
    return jsonify({'ok':True, 'name':name})

@app.route('/api/templates/load/<name>')
def load_template(name):
    templates = load_templates()
    if name not in templates: return jsonify({'error':'Not found'}),404
    return jsonify(templates[name])

@app.route('/api/templates/delete/<name>', methods=['DELETE'])
def delete_template(name):
    templates = load_templates()
    if name in templates: del templates[name]; save_templates(templates)
    return jsonify({'ok':True})

# ── Media ────────────────────────────────────────────────────
@app.route('/api/media/upload', methods=['POST'])
def upload_media():
    if 'file' not in request.files: return jsonify({'error':'No file'}),400
    file = request.files['file']
    if file and '.' in file.filename and file.filename.rsplit('.',1)[1].lower() in ALLOWED_EXT:
        ext  = file.filename.rsplit('.',1)[1].lower()
        fname= f"{uuid.uuid4().hex}.{ext}"
        file.save(os.path.join(MEDIA_FOLDER, fname))
        data = load_data()
        data['media'].append({'id':uuid.uuid4().hex,'filename':fname,
            'original':secure_filename(file.filename),
            'type':'video' if ext in {'mp4','webm','mov'} else 'image',
            'added':datetime.now().isoformat()})
        save_data(data); return jsonify({'ok':True,'filename':fname})
    return jsonify({'error':'Not allowed'}),400

@app.route('/api/media/delete/<mid>', methods=['DELETE'])
def delete_media(mid):
    data = load_data()
    item = next((m for m in data['media'] if m['id']==mid),None)
    if item:
        fp = os.path.join(MEDIA_FOLDER, item['filename'])
        if os.path.exists(fp): os.remove(fp)
        data['media'] = [m for m in data['media'] if m['id']!=mid]
        save_data(data)
    return jsonify({'ok':True})

@app.route('/api/settings', methods=['POST'])
def update_settings():
    data = load_data(); data['settings'].update(request.json); save_data(data); return jsonify({'ok':True})

# ── Static ───────────────────────────────────────────────────
@app.route('/media/<path:filename>')
def serve_media(filename): return send_from_directory(MEDIA_FOLDER, filename)

@app.route('/logos/<path:filename>')
def serve_logos(filename): return send_from_directory('public', filename)

@app.route('/')
def admin(): return send_from_directory('.', 'admin.html')

@app.route('/display')
def display(): return send_from_directory('.', 'display.html')

if __name__ == '__main__':
    ip = get_local_ip()
    print("\n" + "="*56)
    print("  MSI Campus Digital Signage")
    print("="*56)
    print(f"  Admin Panel  : http://localhost:5000")
    print(f"  TV Display   : http://{ip}:5000/display")
    print("="*56 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=False)
