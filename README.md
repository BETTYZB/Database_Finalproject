# Investor-Entrepreneur Connection System

This project simulates a multi-database investment platform that manages investors, entrepreneurs, meetings, and smart recommendations — by combining **PostgreSQL**, **MongoDB**, and **Neo4j**.

---

## 📚 Tech Stack

- **PostgreSQL** – stores structured data (investors, entrepreneurs, investments)
- **MongoDB** – logs flexible meeting feedback
- **Neo4j** – models relationships and generates graph-based recommendations
- **Python 3.12+** – connects and orchestrates all three databases
- **Docker** – spins up PostgreSQL, MongoDB, and Neo4j with minimal setup

---

## 🔧 Core Features

✅ Match investors to entrepreneurs  
✅ Log investor-entrepreneur meetings  
✅ View personalized dashboards  
✅ Search startups by industry & ratings  
✅ Generate platform-wide insights  
✅ Permanently delete users and clean data  

---

## 📁 Project Structure


## 🔧 Features Implemented

- Schedule and log investor-entrepreneur meetings
- Analyze meeting feedback and generate follow-up steps
- Match investors with startups based on shared industry, stage, and history
- Visualize relationship network using Neo4j
- Combine queries across all 3 databases

## 📁 Project Structure
      |-- project\
            |backend\
            |     |-- data\ -------------------------------- CSV and JSON data
            |     |-- db\ ---------------------------------- Database connection scripts
            |     |-- functions\ --------------------------- Core logic touching 3 data models
            |     |-- main.py ------------------------------ Entry point to demo
                  |-- requirements.txt --------------------- #All Python dependencies 
      all features
      |     |-- .env # Environment config (NOT committed)
      |     |-- README.md
            |-- .gitignore # Ignore DB volumes, .env, temp files
            |-- docker-compose.yml # Launches PostgreSQL, MongoDB, and Neo4j


---

## ⚙️ Setup Instructions

### 1. Start the Databases via Docker

```bash
docker-compose up -d

