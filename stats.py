import requests
import pandas as pd

load_csv = pd.read_csv('data.csv')
# output_csv = pd.read_csv('output.csv')

def get_urls():
    return load_csv['url'].tolist()
    
def get_status():
    analyze_endpoint1 = "http://localhost:8000/scrape/"
    analyze_endpoint2 = "http://localhost:1418/scrape/"
    output_csv = pd.DataFrame(columns=['url', 'Total_token', 'response'])
    
    urls = get_urls()
    
    for url in urls:
        print(f"Analyzing {url}", end="\t")
        # status1 = check_status(analyze_endpoint1)
        status1 = "-"
        status2 = requests.post(analyze_endpoint2, json={'url': url}).json()
        Total_token = status2['gpt_response']['usage']['total_tokens']
        response = status2['gpt_response']['choices'][0]['message']['content']
        
        output_csv = output_csv._append({'url': url, 'Total_token': Total_token, 'response': response}, ignore_index=True)
        print("Done")
            
            
    output_csv.to_csv('output.csv', index=False)
    return output_csv

if __name__ == "__main__":
    get_status()