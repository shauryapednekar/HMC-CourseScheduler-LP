import json

with open(r"prereqs1_edited_by_hand.json", encoding="utf-8") as f:
    prereqs1_edited = json.load(f)

with open(r"prereqs2_edited_by_hand.json", encoding="utf-8") as f:
    prereqs2_edited = json.load(f)
    
all_prereqs_edited = prereqs1_edited.copy()
all_prereqs_edited.update(prereqs2_edited)
    
with open(r"all_prereqs_edited_sorted.json", "w") as fp:
    json.dump(all_prereqs_edited, fp, indent=4, sort_keys=True)