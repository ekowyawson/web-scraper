from web_scraper.scraper import get_citations_needed_count,get_citations_needed_report,get_citations_needed_by_section,scan_citations_in_links

# Example usage
url = 'https://en.wikipedia.org/wiki/The_Wizard_of_Speed_and_Time'
# Perform the citation scan for links and save the results
scan_citations_in_links(url, 'citations_needed_report.txt', 'citations_in_links.json')
# Get and save the citations needed by section
get_citations_needed_by_section(url, 'citations_needed_by_section.json')
