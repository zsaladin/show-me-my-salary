from bs4 import BeautifulSoup


def get_parsed_data(text):
    soup = BeautifulSoup(text, 'html.parser')
    
    title_string = soup.title.string 
    encrypted_value = soup.find('input', {'name':'_viewData'})['value']
    return title_string,  encrypted_value
