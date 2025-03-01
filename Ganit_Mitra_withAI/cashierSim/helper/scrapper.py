import requests
from bs4 import BeautifulSoup
from docx import Document
import html

def extraction(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        response.encoding = response.apparent_encoding  
        soup = BeautifulSoup(response.text, 'html.parser')

        text = []
        for lists in soup.find_all('ol'):
            for point in lists.find_all('li'): 
                cleaned_text = html.unescape(point.get_text(strip=True))  
                text.append(cleaned_text)

        extracted_text = '\n\n'.join(text)
        return extracted_text if extracted_text else "No ordered list found."

    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching the website: {e}"

def save_to_text(text, file_name):
    with open(file_name, "w", encoding="utf-8") as file:
        file.write("".join(text))
    print("Data saved successfully.")

url = "https://www.myperfectpack.com/post/revolutionize-your-grocery-startup-with-myperfectpack-list-of-top-100-sold-grocery-products?srsltid=AfmBOorUtB5umBdy2f1pDz9vFxqLkXXitW5wpjsi7hjC_RoZjPrqXpx3"
file_name = "items_list.txt"

data = extraction(url)

if data and "error" not in data.lower():
    save_to_text(data, file_name)
else:
    print("Failure:", data)
