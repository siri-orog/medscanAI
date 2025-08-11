import json
import pandas as pd

# Load the unzipped JSON file
with open("drug_label_part1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract key fields into a list
drug_list = []
for item in data.get("results", []):
    drug_name = item.get("openfda", {}).get("generic_name", ["Unknown"])[0]
    use = item.get("indications_and_usage", [""])[0]
    side_effects = item.get("adverse_reactions", [""])[0]
    warnings = item.get("warnings", [""])[0]

    drug_list.append({
        "Drug Name": drug_name,
        "Use": use.strip().replace("\n", " "),
        "Side Effects": side_effects.strip().replace("\n", " "),
        "Warnings": warnings.strip().replace("\n", " ")
    })

# Convert to DataFrame and save to CSV
df = pd.DataFrame(drug_list)
df.to_csv("drug_data.csv", index=False)
print("✅ drug_data.csv created successfully!")
