import requests
from bs4 import BeautifulSoup

def make_session():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    return session

# using sinonim.org/mo/{word} to get the word base and ending
# as there's no api, bs4 is used instead
def get_base_and_ending(word, session = make_session()):
    url = f"https://sinonim.org/mo/{word}"

    try:
        response = session.get(url, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'lxml')

        # find the page part with word analysis
        target_div = soup.find('div', class_='m_mor0')

        if not target_div:
            print("Target div not found:", word)
            return '', ''

        # extract word base and ending
        base_elements = target_div.find_all('span', class_='m_m6')
        ending_element = target_div.find('span', class_='m_m3')

        # get text (all base parts should be taken)
        # РАЗОЧАРОВАтьСЯ - разочаровася
        base_text = ''.join([elem.get_text(strip=True) for elem in base_elements]) if base_elements else ''
        ending_text = ending_element.get_text(strip=True) if ending_element else ''

        if not base_text:
            print("Error fetching the word base:", word)
            return '', ''

        return base_text, ending_text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return '', ''
