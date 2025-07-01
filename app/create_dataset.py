import pandas as pd

# Fake crime data
data = [
    {
        "id": "CR001",
        "location": "Srinagar",
        "weapon": "knife",
        "time": "night",
        "description": "A man was stabbed outside his home.",
        "crime_type": "assault"
    },
    {
        "id": "CR002",
        "location": "Baramulla",
        "weapon": "gun",
        "time": "day",
        "description": "Shots were fired at a crowded market.",
        "crime_type": "firearm assault"
    },
    {
        "id": "CR003",
        "location": "Anantnag",
        "weapon": "blunt object",
        "time": "night",
        "description": "Someone was attacked with a rod during a break-in.",
        "crime_type": "home invasion"
    }
]

# Save as CSV
df = pd.DataFrame(data)
df.to_csv("crime_dataset.csv", index=False)
print("✔ Dataset created and saved as crime_dataset.csv")
