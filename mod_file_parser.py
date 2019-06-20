""" 
****************************************************************************

- Put this file alongside the index.html in the root of your HTML5 Bundle
- Run it with /asset/ path:
    > python mod_file_parser.py /assets/audio
- It will update the /archive/archive_files.json file with music data

****************************************************************************
 """

import os
import sys
import json

# Exclude files: Include any file here. Like .git
excludefiles = [".DS_Store", ".git"]

try:
    files_path = sys.argv[1]
except (IndexError, ValueError):
    print("Error: asset path is empty")
    sys.exit()

files_path = str(sys.argv[1])  # First arg as path
jsonPath = os.getcwd() + "/archive/archive_files.json"  # Defold json path

# Open json data
with open(jsonPath, "r") as jsonFile:
    data = json.load(jsonFile)

json_content = data["content"]
thePath = os.getcwd() + files_path
os.chdir(thePath)
theFiles = list(os.listdir(thePath))
theDict = dict()

for something in theFiles:  # Calculate size for all files.
    theStats = os.stat(something)
    theDict[something] = theStats

for item in theDict:
    isexc = False

    for filename in excludefiles:
        if item == filename:
            isexc = True
            continue

    if isexc == True:
        continue

    _new_value = {
        "name": item,
        "size": theDict[item].st_size,
        "pieces": [
            {
                "name": ".." + files_path +"/"+ item,
                "offset": 0
            }
        ]
    }

    json_content.append(_new_value)

result = {"content":  json_content}
with open(jsonPath, "w") as jsonFile:
    json.dump(result, jsonFile)

print("Done!")
