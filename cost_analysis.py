import pandas as pd

data = {
    "Service": ["Compute", "Storage", "Network"],
    "Usage": [120, 500, 80],
    "Cost_per_unit": [0.05, 0.02, 0.01]
}

df = pd.DataFrame(data)

df["Total_Cost"] = df["Usage"] * df["Cost_per_unit"]

print(df)
print("Total Cloud Cost:", df["Total_Cost"].sum())

