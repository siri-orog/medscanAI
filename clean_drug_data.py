import pandas as pd

with open("drug_data.csv", "r", encoding="utf-8") as file:
    lines = file.readlines()

drugs = []
drug_name, use, side_effects, warnings = "", "", "", ""
capture = ""

for line in lines:
    line = line.strip()

    if line == "":
        continue

    if "INDICATION" in line.upper():
        capture = "use"
        continue
    elif "ADVERSE REACTIONS" in line.upper():
        capture = "side"
        continue
    elif "WARNINGS" in line.upper():
        capture = "warn"
        continue
    elif line.isupper() and len(line.split()) <= 5:
        if drug_name:
            drugs.append([drug_name, use.strip(), side_effects.strip(), warnings.strip()])
            use, side_effects, warnings = "", "", ""
        drug_name = line.title()
        capture = ""
        continue

    if capture == "use":
        use += " " + line
    elif capture == "side":
        side_effects += " " + line
    elif capture == "warn":
        warnings += " " + line

if drug_name:
    drugs.append([drug_name, use.strip(), side_effects.strip(), warnings.strip()])

df = pd.DataFrame(drugs, columns=["Drug Name", "Use", "Side Effects", "Warnings"])
df.to_csv("drug_data_clean.csv", index=False)
print("✅ Clean CSV created")

