##  Super Shredder: Secure Data Wiping Tool

This repository hosts the complete source code for **Super Shredder**, a robust, cross-platform application designed to securely and permanently wipe files and directories, preventing forensic data recovery. It also includes the code for the companion landing page, built with Django and React, to promote the tool.

-----

##  Key Features

  * **Secure Wiping Algorithms:** Implements industry-standard algorithms (e.g., [mention specific standards like DoD 5220.22-M or Gutmann] - *if applicable*) to overwrite data multiple times.
  * **Cross-Platform Core:** The core wiping logic, contained in the `main` directory, is designed for broad operating system compatibility.
  * **Intuitive GUI:** A user-friendly graphical interface built with Python/Qt (in the `main/gui` directory) for easy file selection and shredding.
  * **Modern Landing Page:** A responsive web front-end built with **Django** and **React** for promotion, documentation, and download links.

-----

## 💻 Repository Structure

The project is logically divided into three main components:

| Directory | Purpose | Tech Stack |
| :--- | :--- | :--- |
| **`main`** | **The Core Super Shredder Application.** Contains the secure wiping logic, command-line utility, and GUI source code and a build.py for making executables. | Python, PyQt/Tkinter (GUI) |
| **`backend`** | **Django Backend** for serving the  potential API endpoints for the  contact form. | Django (Python) |
| **`frontend`** | **React Frontend** code for the **Landing Page** UI. | React, JavaScript, Vite/Webpack, Tailwind CSS |


-----

## 🛠️ Getting Started

Follow these steps to set up and run the entire project locally.

### Prerequisites

1.  **Python 3.x**
2.  **Node.js & npm/yarn**
3.  **Git** (to clone the repository)

### 1\. Set Up the Python Environment (Backend & Main App)

From the project root directory (`file-shredder`):

```bash
# Create a New Virtual Envionment and activate it 
 python3 -m venv fsenv
 source fsenv/bin/activate

# Install Backend dependencies
pip install -r backend/requirements.txt

# Install Main App dependencies (if any separate requirements exist)
pip install -r main/requirements.txt
```

### 2\. Set Up the Frontend (Landing Page)

Navigate to the `frontend` directory and install dependencies:

```bash
cd frontend
npm install # or yarn install
```

-----

## 🚀 Running the Project

### 1\. Running the Super Shredder Application (Core)

To test the core functionality, you can run the main file shredder application directly:

```bash
# Ensure fsenv is active
cd main
python main.py
```

This will launch the application GUI.

### 2\. Running the Landing Page (Django + React)

Start the React development server for the frontend assets:

```bash
# In Terminal 1
cd frontend
npm start
```

Start the Django development server (which will serve the API and the combined page):

```bash
# In Terminal 2, ensure fsenv is active
cd backend
python manage.py runserver
```

Access the landing page at http://localhost:5173 

-----

## 🤝 Contributing

We welcome contributions\! Please see the guidelines below:

1.  Fork the Project.
2.  Create your Feature Branch (`git checkout -b feature/NewAlgorithm`).
3.  Commit your Changes (`git commit -m 'Feat: Added new Gutmann wipe method'`).
4.  Push to the Branch (`git push origin feature/NewAlgorithm`).
5.  Open a Pull Request.

-----



## ⚠️ Disclaimer

SuperShredder is a destructive tool. Files deleted with this tool cannot be recovered. The Android wiper may perform a factory reset on connected devices. The developers are not responsible for any data loss or damage caused by the misuse of this software. Use with caution
