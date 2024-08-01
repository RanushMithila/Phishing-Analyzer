import requests
import pandas as pd

load_csv = pd.read_csv('data.csv')
# output_csv = pd.read_csv('output.csv')

def get_urls():
    return load_csv['url'].tolist()

# def check_status(url):
#     try:
#         userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
#         headers = {
#             "User-Agent": userAgent
#         }
#         response = requests.get(url, headers=headers)
#         print(response.text)
#         return response.status_code
#     except:
#         return "Failed to reach the server"
    
def get_status():
    analyze_endpoint1 = "http://localhost:8000/scrape/"
    analyze_endpoint2 = "http://localhost:1418/scrape/"
    output_csv = pd.DataFrame(columns=['url', 'status1', 'status2'])
    
    urls = get_urls()
    
    for url in urls:
        print(f"Analyzing {url}")
        # status1 = check_status(analyze_endpoint1)
        status1 = "-"
        status2 = requests.post(analyze_endpoint2, json={'url': url}).json()
        output_csv = output_csv._append({'url': url, 'status1': status1, 'status2': status2}, ignore_index=True)
            
            
    output_csv.to_csv('output.csv', index=False)
    return output_csv

if __name__ == "__main__":
    get_status()