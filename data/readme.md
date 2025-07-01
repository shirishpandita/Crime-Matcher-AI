# 📂 Data Folder

This folder contains the datasets used by the **Crime Pattern Matcher AI** project.

## Files

- **`crime_dataset.csv`**  
  The primary dataset containing historical crime records, including:
  - `id`: Unique identifier
  - `location`: Place of the crime
  - `weapon`: Weapon used
  - `time`: Time of day (e.g., day/night)
  - `description`: Text description of the crime
  - `crime_type`: Labelled category (e.g., murder, robbery)
  - `latitude` / `longitude`: Geocoded coordinates for visualization

---

### 📌 Notes
- You can replace this file with your own dataset as long as the structure is similar.
- Make sure the file is encoded in **cp1252** to match the app's requirements.
- If coordinates are missing, they will be automatically added using geolocation.
