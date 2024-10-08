import requests
import csv
from urllib.parse import quote

# replace with your own MWCOMSESS value
cookies = {"MWCOMSESS": "your-own-MWCOMSESS-value",}

# get the count of all the saved words
def fetch_total_count():
    url = "https://www.merriam-webster.com/lapi/v1/wordlist/get-total-count"
    response = requests.get(url, headers=None, cookies=cookies)
    if response.status_code == 200:
        return response.json()['data']['data']['total_count']
    else:
        print(f"fetch_total_count error: {response.status_code}")
        return None

# get a list of all the saved words
def fetch_saved_words(word_count):
    url = f"https://www.merriam-webster.com/lapi/v1/wordlist/search?search=&perPage={word_count}"
    response = requests.get(url, headers=None, cookies=cookies)
    if response.status_code == 200:
        return response.json()['data']['data']['items']
    else:
        print(f"fetch_saved_words error: {response.status_code}")
        return None

# create the csv file
def create_csv(word_list, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for word in word_list:
            encoded_word = quote(word)
            url = f"https://www.merriam-webster.com/dictionary/{encoded_word}"
            back_html = f"""<p><a href='{url}'>{word}</a></p>"""
            writer.writerow([word, back_html])
    print(f"CSV file '{output_file}' has been created successfully.")

def main():
    total_count = fetch_total_count()
    saved_words = fetch_saved_words(total_count)
    word_list = []
    for word_inst in saved_words:
        word = word_inst['word'] 
        word_list.append(word)
    create_csv(word_list, 'M-W-saved-words.csv')

if __name__ == "__main__":
    main()
