
import json
import os
import pandas as pd
from datetime import datetime

df = pd.DataFrame([], columns=['URL','Accessibility Score'])

# TODO: create list of websites for 280 websites
# df_urls = pd.read_csv("all_data.csv")["Website"]
# urls = df_urls.values.tolist()

urls = ["https://airtable.com/shrwRSTAxBhy1JkRf"]

for url in urls:    
    stream = os.popen(f'lighthouse {url} --only-categories=accessibility --quiet --output=json --output-path=./output/accessibility.json --chrome-flags="--headless"')
    print("Report complete for: " + url)

    with open("./output/accessibility.json") as json_data:
        loaded_json = json.load(json_data)
        score = str(round(loaded_json["categories"]["accessibility"]["score"] * 100))
        print(score)
        new_row = {
            "URL": url,
            "Accessibility Score": score
        }
        df = pd.concat([df, pd.DataFrame([new_row])])

df.to_csv('./output/accessibility_scores.csv')
