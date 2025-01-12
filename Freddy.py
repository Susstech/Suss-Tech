import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import json

# Load configuration data from the `config.json` file
def load_config(config_file="config.json"):
    """Load configuration data from a JSON file."""
    try:
        with open(config_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Configuration file '{config_file}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from '{config_file}'.")
        return None

# Initialize configuration
config = load_config()
if not config:
    raise Exception("Failed to load configuration. Ensure the 'config.json' file exists and is valid.")

# Extract data from the configuration
api_key = config["azure"]["api_key"]
endpoint = config["azure"]["endpoint"]
websites = config["websites"]
ner_model_name = config["ner_model"]["model_name"]

# Initialize the NER pipeline with the model specified in the config
pipe = pipeline("token-classification", model=ner_model_name)

# Function to extract keywords using the NER pipeline
def extract_keywords(text):
    """Extract keywords using the specified NER model."""
    ner_results = pipe(text)
    keywords = [result['word'] for result in ner_results if result['entity'] != 'O']
    return keywords

# Website scraper function
def fetch_website_data(url, keywords):
    """Fetch website content and filter text containing specific keywords."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        text_content = soup.get_text()
        relevant_text = [
            sentence for sentence in text_content.split(".")
            if any(keyword.lower() in sentence.lower() for keyword in keywords)
        ]
        return " ".join(relevant_text)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return ""

# Summarization using Azure OpenAI
def summarize_text_with_openai(text):
    """Summarize the extracted text using Azure OpenAI API."""
    prompt = f"Summarize the following text:\n\n{text}"
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
    }
    data = {
        "model": "gpt-4",
        "messages": [{"role": "system", "content": "You are a helpful assistant."},
                     {"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 150
    }
    response = requests.post(endpoint, headers=headers, json=data)
    if response.status_code == 200:
        response_json = response.json()
        return response_json['choices'][0]['message']['content'].strip()
    else:
        print(f"Error with Azure OpenAI request: {response.status_code}")
        return None

# Main function
def main():
    user_input = input("Enter a word or phrase: ")
    print("\nExtracting keywords...")
    keywords = extract_keywords(user_input)
    print(f"Identified Keywords: {keywords}")

    print("\nScraping websites for relevant data...")
    gathered_data = []
    for site in websites:
        print(f"Fetching data from: {site}")
        data = fetch_website_data(site, keywords)
        if data:
            gathered_data.append(data)

    combined_data = " ".join(gathered_data)
    if not combined_data.strip():
        print("\nNo relevant data found on the provided websites.")
        return

    print("\nSummarizing the gathered data using Azure OpenAI...")
    summary = summarize_text_with_openai(combined_data)
    if summary:
        print("\nSummarized Output:")
        print(summary)
    else:
        print("\nFailed to generate a summary.")

if __name__ == "__main__":
    main()
