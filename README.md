## Overview
This Python program integrates Named Entity Recognition (NER), web scraping, and Azure OpenAI services to:

1. Extract keywords from user input using an NER model.
2. Scrap relevant data from predefined websites for the extracted keywords.
3. Summarize the gathered data using the Azure OpenAI GPT-4 model.

## Features
- Dynamically fetch configuration data (e.g., API keys, endpoints, model names) from a `config.json` file.
- Perform web scraping using `requests` and `BeautifulSoup`.
- Extract entities with the `dbmdz/bert-large-cased-finetuned-conll03-english` NER model via the Hugging Face `transformers` pipeline.
- Summarize data using Azure OpenAI GPT-4.

---

## Prerequisites

1. **Python**: Ensure Python 3.8 or higher is installed.
2. **Libraries**:
   - Install required Python packages using:

     ```bash
     pip install requests beautifulsoup4 transformers
     ```
3. **Azure OpenAI Service**:
   - An active Azure subscription with access to the OpenAI service.
   - Deployment of the GPT-4 model with the appropriate API version.
4. **Configuration File**:
   - Create a `config.json` file with the following content:

     ```json
     {
         "azure": {
             "api_key": "YOUR_AZURE_API_KEY_HERE",
             "endpoint": "https://YOUR_CUSTOM_ENDPOINT_HERE/openai/deployments/YOUR_MODEL/chat/completions?api-version=2024-08-01-preview"
         },
         "websites": [
             "https://www.clearias.com/constitution-of-india/?srsltid=AfmBOopG_QDOUaYaUOyAgu3dWPPz975fdFhTVtf1MW33agX6fiG3hoyo#part-i-the-union-and-its-territory",
             "https://www.thehindu.com/news/national/advanced-medium-combat-aircraft-prototype-expected-by-2028-29/article68360061.ece"
         ],
         "ner_model": {
             "model_name": "dbmdz/bert-large-cased-finetuned-conll03-english"
         }
     }
     ```

---

## How It Works

1. **Load Configuration**:
   - The program dynamically loads API keys, model names, and website URLs from the `config.json` file.

2. **Keyword Extraction**:
   - User provides a phrase or sentence.
   - Keywords are extracted using the NER model `dbmdz/bert-large-cased-finetuned-conll03-english`.

3. **Web Scraping**:
   - Predefined websites in `config.json` are scraped for content.
   - Relevant sentences containing the extracted keywords are filtered.

4. **Summarization**:
   - The gathered content is summarized using Azure OpenAI GPT-4.

---

## Running the Program

1. **Set Up the Virtual Environment (Optional but Recommended)**:
   ```bash
   python -m venv myenv
   source myenv/bin/activate   # On Windows: myenv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install requests beautifulsoup4 transformers
   ```

3. **Place the `config.json` File**:
   - Ensure the `config.json` file is in the same directory as the program.

4. **Run the Script**:
   ```bash
   python main.py
   ```

5. **Input Prompt**:
   - The program will ask for a word or phrase.
   - It will output:
     - Extracted keywords.
     - Websites scraped.
     - Summarized content.

---

## File Structure

```plaintext
project-folder/
|
|-- main.py          # Main script
|-- config.json      # Configuration file with API keys, endpoints, and settings
|-- README.md        # This documentation
|
|-- requirements.txt # Optional: List of dependencies
```

---

## Configuration Details

### `config.json` Format

| Field              | Type     | Description                                                                 |
|--------------------|----------|-----------------------------------------------------------------------------|
| `azure.api_key`    | String   | Your Azure OpenAI API key.                                                 |
| `azure.endpoint`   | String   | Endpoint URL for your Azure OpenAI deployment.                             |
| `websites`         | List     | List of website URLs to scrape.                                            |
| `ner_model.model_name` | String   | Name of the NER model used for extracting keywords.                        |

---

## Limitations

1. **Azure OpenAI Restrictions**:
   - Ensure your Azure OpenAI service allows GPT-4 requests.

2. **Website Accessibility**:
   - Websites must be publicly accessible and not block web scraping.

3. **NER Model**:
   - The `dbmdz/bert-large-cased-finetuned-conll03-english` model is trained on English text. Results may vary for non-English inputs.

---

## Future Improvements

1. Add support for real-time website selection by users.
2. Implement caching to reduce redundant API requests.
3. Support multiple languages for both NER and summarization.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact
For any questions or feedback, feel free to reach out.

