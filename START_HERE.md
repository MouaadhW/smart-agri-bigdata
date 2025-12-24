# STEP-BY-STEP GUIDE – How to Run Docker & Start Everything

Follow this **exact order**. Each step shows where to be and what to type.

---

## STEP 1: Open Terminal (PowerShell)

**Where**: Click on the project folder in Windows Explorer or VS Code

**What to do**: Right-click → Open PowerShell Here (or open Terminal)

**You should see**: 
```
PS C:\Users\...\smart-agri-bigdata>
```

**Verify you're in the right place**: Type this command:
```powershell
dir
```

You should see folders: `app`, `hadoop`, `mongodb`, `spark`, and files like `docker-compose.yml`, `README.md`

---

## STEP 2: Create the `.env` File

**Where**: In that same PowerShell terminal (in the project root)

**What to do**: Create a file named `.env` with these credentials:

**Option A - Using PowerShell (easiest for Windows):**
```powershell
@"
MONGOINITDBROOTUSERNAME=root
MONGOINITDBROOTPASSWORD=example
MONGODB=agridb
"@ | Out-File -Encoding UTF8 .env
```

**Option B - Using Notepad (if above doesn't work):**
1. Press `Win + R`
2. Type `notepad` and press Enter
3. Copy-paste this:
```
MONGOINITDBROOTUSERNAME=root
MONGOINITDBROOTPASSWORD=example
MONGODB=agridb
```
4. Save as `.env` (in the project folder)
5. Make sure filename is `.env` (not `.env.txt`)

**Verify it worked:**
```powershell
cat .env
```

Should display the 3 lines above.

---

## STEP 3: Start Docker Containers

**Where**: PowerShell terminal in the project root folder

**What to do**: Type this command:
```powershell
docker compose up -d
```

**What to expect**: You'll see output like:
```
[+] Running 5/5
 ✔ Container hadoop-namenode      Started
 ✔ Container hadoop-datanode      Started
 ✔ Container spark                Started
 ✔ Container mongodb              Started
 ✔ Container app                  Started
```

**Verify containers are running:**
```powershell
docker ps
```

You should see 5 containers listed with status "Up"

---

## STEP 4: Generate Sample Data

**Where**: Same PowerShell terminal

**What to do**: Run these 2 commands (one at a time):

**Command 1:**
```powershell
python app/scripts/simulate_sensors_gateway.py
```

**What to expect:**
```
Sensor simulation finished. Files in data/gateway_output/
```

**Command 2:**
```powershell
python app/scripts/prepare_disease_metadata.py
```

**What to expect:**
```
Disease metadata cleaned and loaded into MongoDB.
```

**Verify files were created:**
```powershell
dir app\data\gateway_output
```

You should see ~96 JSON files like `sensorbatch202512090000.json`

---

## STEP 5: Start Streamlit UI

**Where**: Same PowerShell terminal

**What to do**: Type this command:
```powershell
python -m streamlit run app/interface.py
```

**What to expect**: You'll see:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://10.0.0.xxx:8501
```

**What to do next**: Open your browser and go to:
```
http://localhost:8501
```

---

## STEP 6: Explore the UI

**In the browser** at http://localhost:8501:

1. **Home Tab** → You see the README
2. **Runbook Tab** → Shows all Docker commands
3. **Data Tab** → Shows CSVs from `app/data/` and `app/results/`
4. **Analytics Tab** → Shows MongoDB data (if connected)
5. **Architecture Tab** → System overview

✅ **This means everything is working!**

---

## STEP 7: Stop Everything (When Done)

**Where**: Open a **NEW** PowerShell terminal in the project folder

**What to do**: Type:
```powershell
docker compose down
```

**What to expect:**
```
[+] Running 5/5
 ✔ Container spark         Removed
 ✔ Container app           Removed
 ✔ Container mongodb       Removed
 ✔ Container hadoop-namenode  Removed
 ✔ Container hadoop-datanode  Removed
```

---

## QUICK REFERENCE TABLE

| Step | Command | Location | Expected Result |
|------|---------|----------|-----------------|
| 1 | `dir` | Project root | See app, hadoop, etc. |
| 2 | `cat .env` | Project root | Shows 3 lines of config |
| 3 | `docker compose up -d` | Project root | 5 containers start |
| 3b | `docker ps` | Project root | 5 containers listed (Up) |
| 4a | `python app/scripts/simulate_sensors_gateway.py` | Project root | 96 JSON files created |
| 4b | `python app/scripts/prepare_disease_metadata.py` | Project root | Data loaded to MongoDB |
| 5 | `python -m streamlit run app/interface.py` | Project root | http://localhost:8501 opens |
| 7 | `docker compose down` | Project root | 5 containers removed |

---

## TROUBLESHOOTING

### Problem: "docker: command not found"
**Solution**: Docker Desktop not installed or not in PATH
- Install Docker Desktop from https://www.docker.com/products/docker-desktop
- Restart PowerShell after installation

### Problem: "docker compose: command not found"
**Solution**: Old Docker version (need Docker v2+)
- Uninstall and reinstall Docker Desktop

### Problem: `.env` file not created
**Solution**: Use Notepad method (Step 2, Option B)
- Or try: `notepad .env` then save in project folder

### Problem: "Sensor simulation finished" but no files created
**Solution**: 
```powershell
dir app\data\gateway_output
```
If empty, run:
```powershell
python app/scripts/simulate_sensors_gateway.py
```

### Problem: Streamlit won't start
**Solution**:
```powershell
pip install -r requirements.txt
python -m streamlit run app/interface.py
```

### Problem: MongoDB connection failed
**Solution**: Wait 10 seconds for MongoDB to start, then refresh browser page

---

## TYPICAL WORKFLOW (Copy-Paste Ready)

Open PowerShell in project folder, then paste these commands one-by-one:

```powershell
# Check location
dir

# Create .env
@"
MONGOINITDBROOTUSERNAME=root
MONGOINITDBROOTPASSWORD=example
MONGODB=agridb
"@ | Out-File -Encoding UTF8 .env

# Start Docker
docker compose up -d

# Wait 5 seconds, then generate data
Start-Sleep 5
python app/scripts/simulate_sensors_gateway.py
python app/scripts/prepare_disease_metadata.py

# Start UI
python -m streamlit run app/interface.py
```

Then open http://localhost:8501 in browser ✅

---

**That's it! You now have the full stack running.** 🚀
