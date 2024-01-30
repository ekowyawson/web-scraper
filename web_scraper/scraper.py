import requests
from bs4 import BeautifulSoup
import json
import time

def get_citations_needed_count(url):
    """Counts the number of "citation needed" instances in a Wikipedia article.
    Args:
        url (str): The URL of the Wikipedia article to scan.
    Returns:
        int: The number of citations needed in the article.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    citations_needed = soup.find_all('span', string='citation needed')
    return len(citations_needed)


def get_citations_needed_report(url, outputFile):
    """Generates a report of all text snippets in a Wikipedia article that
        require citations and writes it to a file.
    Args:
        url (str): The URL of the Wikipedia article to scan.
        outputFile (str): The path of the file where the report will be saved.
    Returns:
        str: A formatted string report of all citation-needed text snippets.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    citations_needed = soup.find_all('span', string='citation needed')
    report_list = []
    report = ""
    i = 0

    for citation in citations_needed:
        i += 1
        parent_tag = citation.find_parent('li')
        if not parent_tag:  # Fallback to parent paragraph if not in <li>
            parent_tag = citation.find_parent('p')
        if parent_tag:
            report_string = ' '.join(parent_tag.text.split())
            report_list.append(f"[{i}] {report_string}\n\n")
            report += f"[{i}] {report_string}\n\n"
    with open(outputFile, 'w') as output_file:
        heading = f"Citations Needed In Wiki Article: {url}"
        output_file.write(f"{heading}\n{ '=' * len(heading) }\n")
        output_file.writelines(report_list)
    return report.strip()


def get_citations_needed_by_section(url, jsonOutputFile):
    """Organizes and saves to a JSON file the sections of a Wikipedia article that
        require citations.
    Args:
        url (str): The URL of the Wikipedia article to scan.
        jsonOutputFile (str): The path of the JSON file where the report will be saved.
    Returns:
        dict: A dictionary where each key is a section heading and the value is a list of
        text snippets that need citations.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    sections = soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6'])
    report = {}

    for section in sections:
        section_title = section.text.strip()
        contents = []
        for sibling in section.find_next_siblings():
            if sibling.name in ['h2', 'h3', 'h4', 'h5', 'h6']:
                break
            if 'citation needed' in sibling.text:
                contents.append(sibling.text.strip())
        if contents:
            report[section_title] = contents   
    with open(jsonOutputFile, 'w') as file:
        json.dump(report, file, indent=4)
    return report


def scan_citations_in_links(url, outputFile, jsonOutputFile):
    """Scans all internal Wikipedia links within the article for citations needed,
        and saves the reports to text and JSON files.
    Args:
        url (str): The URL of the Wikipedia article to scan.
        outputFile (str): The path of the text file where the individual reports will be saved.
        jsonOutputFile (str): The path of the JSON file where the compiled reports will be saved.

    Returns:
    dict: A dictionary containing the citation reports for each linked article.
    """
    start_time = time.time()
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    main_content = soup.find('div', {'id': 'mw-content-text'})
    links = main_content.find_all('a', href=True)
    link_reports = {}

    for link in links:
        if time.time() - start_time > 10:  # Check if 10 seconds have elapsed
            break
        link_url = link['href']
        
        if link_url.startswith("/wiki/") and not link_url.startswith("/wiki/File:"):
            full_url = f"https://en.wikipedia.org{link_url}"
            count = get_citations_needed_count(full_url)
            if count > 0:
                report = get_citations_needed_report(full_url, outputFile)
                link_reports[full_url] = {'count': count, 'report': report}
    with open(jsonOutputFile, 'w') as file:
        json.dump(link_reports, file, indent=4)
    return link_reports
