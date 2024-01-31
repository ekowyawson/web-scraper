# LAB - Class 17

## Project: Web Scraping

### Author: Ekow Yawson

**Project Overview**: This is a specialized web scraping tool designed for Wikipedia articles. It uses the **requests** and **BeautifulSoup** Python libraries to fetch and parse HTML content from Wikipedia, focusing on identifying sections where citations are needed. The `scraper.py` module comprises several functions, each serving a distinct purpose in the citation analysis process.

1. **`get_citations_needed_count(url)`**: This function takes a Wikipedia article URL as input and returns the total number of "*citation needed*" instances within that article. It does this by finding all `<span>` elements with the text "*citation needed*."

2. **`get_citations_needed_report(url, outputFile)`**: Similar to the first function, this one also scans a Wikipedia article for "*citation needed*" tags. However, instead of just counting them, it compiles a detailed report listing each specific instance where a citation is needed, including the associated text. This report is returned as a string.

3. **`get_citations_needed_by_section(url, jsonOutputFile)`**: This function enhances the citation analysis by organizing the "*citation needed*" instances by their respective section headings in the Wikipedia article. It creates a structured report where each key is a section title, and the associated value is a list of text snippets needing citations within that section.

4. **`scan_citations_in_links(url, outputFile, jsonOutputFile)`**: This function expands the scope of the analysis to include internal Wikipedia links found within the main content of the specified article. It follows these links (*up to a 10-second time limit to prevent excessive load*) and performs the citation analysis on each linked article. The results, including the number of citations needed and detailed reports for each linked article, are compiled and returned.

5. **`save_to_file`** This function takes care of saving the retrieved data in either JSON or text format.

Overall, this script is a powerful tool for Wikipedia editors and researchers, aiding in identifying areas where additional citations are required to improve the reliability and veracity of the information presented in Wikipedia articles.

### Links and Resources

- [Wikipedia - History of Mexico](https://en.wikipedia.org/wiki/History_of_Mexico)
- [The Wizard of Speed and Time](https://en.wikipedia.org/wiki/The_Wizard_of_Speed_and_Time)
- [Citation Hunt](https://meta.wikimedia.org/wiki/Citation_Hunt)
- [Citation Hunt Checks](https://citationhunt.toolforge.org/en?id=a3602df0)
- [Difference between write() and writelines() function in Python](https://www.geeksforgeeks.org/difference-between-write-and-writelines-function-in-python/)

### Setup

**Environment Setup Steps**:

1. Clone the repo to your local machine.
2. Create a virtual environment with Python venv.
3. Run the following command to install dependencies:
   - `pip install -r requirements.txt`.
4. Modify `main.py` as needed.

#### How to initialize/run your application

**Running the Code**:

To run the code, execute `main.py` in your Python environment. This will run the functions defined in the scraper module with the provided URL and save the output to the specified files. Ensure that BeautifulSoup and requests are installed in your environment, as they are required by the scraper module.

```python
# Example usage
url = 'https://en.wikipedia.org/wiki/The_Wizard_of_Speed_and_Time'

# Perform the citation scan for links
links_report = scan_citations_in_links(url)
save_to_file(links_report, 'citations_in_links.json', 'json')

# Get citations needed by section
sections_report = get_citations_needed_by_section(url)
save_to_file(sections_report, 'citations_needed_by_section.json', 'json')
```
