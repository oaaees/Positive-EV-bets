from selenium import webdriver
from selenium.webdriver.common.by import By

urls = ['https://www.pinnacle.com/es/soccer/england-premier-league/matchups/']
driver = webdriver.Chrome()
driver.implicitly_wait(10)

pages = []

for url in urls:
    driver.get(url)
    main = driver.find_element(By.TAG_NAME, "main")
    pages.append(main.find_element(By.CSS_SELECTOR,".contentBlock.square"))

class Match:
    def __init__(self, team1, team2, date, time, p1, ptie, p2):
        self.team1 =  team1
        self.team2 = team2
        self.date = date
        self.time = time
        self.p1 = p1
        self.ptie = ptie
        self.p2 = p2
    def print(self) :
        print(self.team1 + " vs " + self.team2 + " " + self.p1 + " - " + self.ptie + " - " + self.p2)

Matches = []

for page in pages:
    divs = page.find_elements(By.TAG_NAME, "div")
    date = ""

    for div in divs:
        is_date = "style_dateBar__1adEH" in div.get_attribute("class")
        is_spacer = "style_row__3l5MS" in div.get_attribute("class")
        is_match = "style_row__12oAB" in div.get_attribute("class")

        if is_date: date = div.text
        if is_spacer: continue
        if is_match:
            teams = div.find_elements(By.CLASS_NAME, "style_gameInfoLabel__2m_fI")
            time = div.find_element(By.CLASS_NAME, "style_matchupDate__UG-mT")
            p = div.find_elements(By.CLASS_NAME, "style_button-wrapper__2u2GV")

            Matches.append(Match(teams[0].text.replace('(Partido)', ''), teams[1].text.replace('(Partido)', ''), date, time.text, p[0].text, p[1].text, p[2].text))

for m in Matches:
    m.print()






    

