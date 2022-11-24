
import json
import os
import pandas as pd
import random
from datetime import datetime
import subprocess
import re

random_indices = random.sample(range(1, 854), 170)
random_indices = sorted(random_indices)
print(random_indices)

df = pd.DataFrame([], columns=["SRS Index", 'URL','Accessibility Score'])

df_urls = pd.read_csv("./lower_market_caps.csv")["Website"]
urls = df_urls.values.tolist()

for index in random_indices:    
    bad_urls = ["nan", '']
    print(urls[index])
    if str(urls[index]).strip() in bad_urls or not urls[index]:
        print("bad url", urls[index])
        continue
    filename = str(index) + ".json"
    try:
        stream = subprocess.run(f'lighthouse {str(urls[index]).strip()} --skip-audits=full-page-screenshot --only-categories=accessibility --output=json --chrome-flags="--headless', stdout=subprocess.PIPE, shell=True)
    except:
        print('ERROR: BAD URL', urls[index])
        continue
    loaded_json = json.loads(str(stream.stdout.decode('utf-8')))
    accessibility_score = score = str(round(loaded_json["categories"]["accessibility"]["score"] * 100))
    print("Report complete for: " + str(urls[index]), "score:", accessibility_score)
    new_row = {
            "SRS Index": random_indices[index],
            "URL": urls[index],
            "Accessibility Score": score
        }
    df = pd.concat([df, pd.DataFrame([new_row])])

df.to_csv('./output/accessibility_scores.csv')
