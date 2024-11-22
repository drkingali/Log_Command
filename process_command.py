import json

# Load the command.json file
with open('command.json', 'r') as file:
    data = json.load(file)

# Step 1: Remove objects with any null values, empty fields, or missing required keys
required_keys = {"pageIdentifier", "uniqueCode", "remainingLogs", "signTime"}

clean_data = [
    item for item in data 
    if all(key in item for key in required_keys) and  # بررسی وجود تمام کلیدها
       all(value is not None and value != "" and str(value).strip() != "" for value in item.values())  # بررسی مقدار معتبر
]
# Step 2: Group by pageIdentifier
groups = {}
for item in clean_data:
    page_id = int(item["pageIdentifier"])
    if page_id not in groups:
        groups[page_id] = []
    groups[page_id].append(item)

# Step 3: Process each group
processed_groups = {}
for page_id, items in groups.items():
    # Find maximum signTime (x)
    items = sorted(items, key=lambda x: int(x["signTime"]), reverse=True)
    x = int(items[0]["signTime"])

    # Select objects in the range [x-360, x]
    gamma_items = [item for item in items if x - 360 <= int(item["signTime"]) <= x]
    gamma_items.sort(key=lambda x: int(x["signTime"]))

    # Find object y with max remainingLogs
    y = max(
        gamma_items,
        key=lambda obj: (int(obj["remainingLogs"]), -int(obj["signTime"]))
    )

    z = int(y["remainingLogs"])

    # Find object f after skipping z items from y
    index_y = gamma_items.index(y)
    f = None
    if index_y + z < len(gamma_items):
        f = gamma_items[index_y + z]

    # Remove objects with signTime greater than f
    if f:
        items = [obj for obj in items if int(obj["signTime"]) <= int(f["signTime"])]

    # Sort the remaining items by signTime
    processed_groups[page_id] = sorted(items, key=lambda x: int(x["signTime"]))

# Step 4: Sort groups by pageIdentifier
sorted_groups = dict(sorted(processed_groups.items()))

# Flatten the sorted groups into a single list
final_output = []
for page_id, items in sorted_groups.items():
    final_output.extend(items)

# Save processed data back to command.json
with open('command.json', 'w') as file:
    json.dump(final_output, file, indent=4)

print("Processed command.json successfully!")
