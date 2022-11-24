import json
import pandas as pd
import random
import subprocess

random_indices = random.sample(range(1, 854), 85)
random_indices = sorted(random_indices)
print(random_indices)

df_urls = pd.read_csv("./lower_market_caps.csv")["Website"]
urls = df_urls.values.tolist()

df = pd.DataFrame(columns=["SRS Index", "URL", "Accessibility Score"])

for index in random_indices:    
    new_row = {
        "SRS Index": index,
        "URL": urls[index],
        "Accessibility Score": 'NONE'
    }   

    bad_urls = ["nan", '']
    print(urls[index])

    try:
        if str(urls[index]).strip() in bad_urls or not urls[index]:
            print("Bad URL", urls[index])
            raise Exception("Bad URL", urls[index])
        filename = str(index) + ".json"
        stream = subprocess.run(f'lighthouse {str(urls[index]).strip()} --skip-audits=full-page-screenshot --only-categories=accessibility --output=json --chrome-flags="--headless', stdout=subprocess.PIPE, shell=True)
        
        if not (output := stream.stdout.decode('utf-8')):
            raise Exception("Stream is Empty")
        if not (loaded_json := json.loads(output)):
            raise Exception("No JSON Returned")
        if not (score := loaded_json["categories"]["accessibility"]["score"]):
            raise Exception ("No Score Returned")
        
        score = str(round(score * 100))
        print("Report complete for: " + str(urls[index]), "score:", score)
        new_row["Accessibility Score"] = score  
    except:
        print("ERROR: Score Not Found")
    df = pd.concat([df, pd.DataFrame([new_row])])

df.to_csv('./output/accessibility_scores.csv')
