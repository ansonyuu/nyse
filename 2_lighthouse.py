
import json
import os
import pandas as pd
import random
from datetime import datetime
from subprocess import Popen

random_indices = random.sample(range(1, 5), 3)
random_indices = sorted(random_indices)
print(random_indices)

df = pd.DataFrame([], columns=["SRS Index", 'URL','Accessibility Score'])

df_urls = pd.read_csv("./inputs/urls_test.csv")["Website"]
urls = df_urls.values.tolist()

for index in random_indices:    
    bad_urls = ["nan", '']
    if urls[index] in bad_urls or not urls[index]:
        continue
    filename = str(index) + ".json"
    stream = os.popen(f'lighthouse {urls[index]} --only-categories=accessibility --quiet --output=json --output-path=./output/{index}.json --chrome-flags="--headless"')
    print("Report complete for: " + urls[index])

    
# process is stuck on creating new .json file from output... unknown reason why
# try capturing terminal input directly intead of writing to a file first
    while(not os.path.exists(f'./output/{index}.json')):
        continue

    with open("./output/"+ str(index) + ".json") as json_data:
        loaded_json = json.load(json_data)
        score = str(round(loaded_json["categories"]["accessibility"]["score"] * 100))
        print(score)
        new_row = {
            "SRS Index": random_indices[index],
            "URL": urls[index],
            "Accessibility Score": score
        }
        df = pd.concat([df, pd.DataFrame([new_row])])

df.to_csv('./output/accessibility_scores.csv')
