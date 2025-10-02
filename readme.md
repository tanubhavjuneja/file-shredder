# Secure File Shredder App

## **Project Overview / Objective**

The **Secure File Shredder App** is a full-stack application designed to **securely delete files** from a system by overwriting their content multiple times before deletion, ensuring that sensitive data cannot be recovered.

**Key Features:**

* Overwrites files multiple times (customizable number of passes).
* Configurable chunk size for overwriting.
* Optionally wipe free space on the disk (simulation).
* Synchronous backend execution for simplicity (no Celery required).
* Frontend in React shows task status and completion messages.
* Safe for development testing with dummy files before production use.

**Use Case:**
Ideal for users or organizations that need to ensure files containing sensitive information are **irrecoverably deleted**.

---

## **Technology Stack**

* **Backend:** Django + Django REST Framework (Python)
* **Frontend:** React.js
* **HTTP Requests:** Axios
* **File Handling:** Python standard libraries (`os`, `random`, `time`)

---

## **Installation Guide**

### **1. Backend Setup (Django)**

1. Clone the repository:

```bash
git clone <your-repo-url>
cd shredder/backend
```

2. Create a Python virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. Install required Python packages:

```bash
pip install -r requirements.txt
```

4. Apply Django migrations:

```bash
python manage.py migrate
```

5. Start the Django development server:

```bash
python manage.py runserver
```

> The API will be available at `http://localhost:8000/api/`.

---

### **2. Frontend Setup (React)**

1. Navigate to the frontend directory:

```bash
cd ../frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm start
```

4. Start Build
```bash
npm run build
```
5. Navigate to Main Directory
```bash
python manage.py runserver localhost:8000

```

> The frontend will be available at `http://localhost:3000/` (default React port).

---

## **Usage**

1. Open the React frontend in your browser (`http://localhost:3000/`).
2. Enter the **absolute path** of the file you want to shred.
3. Configure the shredding options:

   * **Passes:** Number of overwrites (minimum 3 recommended).
   * **Chunk Size:** Size in MB for each overwrite chunk.
   * **Wipe Free Space:** Optional.
4. Click **Start Secure Shredding**.
5. Observe the **status panel**:

   * "Processing..." while backend is shredding.
   * "Completed" with success message once done.
   * "Failed" if an error occurs.

**⚠️ Important:** Always test on **dummy files** first. The shredding process **permanently deletes files**.

---

## **Project Structure**

```
shredder/
├── backend/
│   ├── manage.py
│   ├── shred_core.py       # Core shredding logic
│   ├── views.py            # API endpoints
│   ├── urls.py
│   └── ...
├── frontend/
│   ├── src/
│   │   ├── ShredFormSync.js
│   │   └── ShredStatusTracker.js
│   ├── package.json
│   └── ...
└── README.md
```

```json
{
  "target_path": "/home/user/test.txt",
  "passes": 7,
  "chunk_size_mb": 100,
  "wipe_free_space": "false"
}
```

**Response Example (Success):**

```json
{
  "status": "success",
  "message": "Shredding completed successfully for /home/user/test.txt",
  "result": {
    "status": "success",
    "message": "Successfully shredded and deleted test.txt"
  }
}
```

---

## **Notes**

* This setup is **development-only**. Do not expose it to the internet without proper authentication.
* Always verify **file paths** carefully to avoid accidental deletion.
* For production: Consider using Celery/Redis for asynchronous shredding and live progress tracking.
