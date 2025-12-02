# 🌞 SolarFarm-Optimizer-AI

Multi-agent AI prototype that analyzes satellite imagery and geospatial features to recommend optimal locations for solar farms. The system combines computer vision, geospatial analysis, and an AI agentic pipeline in a Streamlit dashboard for end‑to‑end site evaluation. [web:2][web:4]

---

## ✨ Key Features

- 🛰️ **Satellite image analysis**: Upload a satellite image and extract terrain, land‑use and obstacle information using a vision pipeline. [web:9]
- 🤖 **Multi‑agent orchestration**: Dedicated agents for data ingestion, vision, optimization, and validation, coordinated in a single workflow. [web:6][web:10]
- 📍 **Site scoring & ranking**: Compute scores for candidate sites based on irradiance, constraints, accessibility, and grid distance.
- 🗺️ **Interactive geospatial UI**: Streamlit app with maps, overlays and tables for exploring recommended locations. [web:7][web:13]
- 📊 **Field reality check**: Compare theoretical scores with on‑site “field_reports.csv” to measure planning vs. reality gaps.

---

## 🧱 Architecture

- **Frontend**: Streamlit dashboard for file upload, parameter tuning and visualization.
- **Vision layer**: Preprocessing, segmentation and obstacle detection on satellite images.
- **Optimization layer**: Heuristic / rule‑based scoring of candidate sites.
- **Validation layer**: Cross‑checks predictions against structured field data.
- **Storage**: Simple CSV inputs (`field_reports.csv`) and image files in `demo_data/`.

Directory overview:

