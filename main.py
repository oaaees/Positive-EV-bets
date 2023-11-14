from selenium import webdriver
from selenium.webdriver.common.by import By

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
        print(f'{self.team1} vs {self.team2} with prob {self.p1:.5f} - {self.ptie:.5f} - {self.p2:.5f}')
    def printCSV(self) :
        return f'{self.team1},{self.team2},{self.p1:.5f},{self.ptie:.5f},{self.p2:.5f},,,,{self.date}\n'


#pinnacle_urls = ['https://www.pinnacle.com/es/soccer/spain-la-liga/matchups/',
#                 'https://www.pinnacle.com/es/soccer/england-premier-league/matchups/',
#                 'https://www.pinnacle.com/es/soccer/italy-serie-a/matchups/',
#                 'https://www.pinnacle.com/es/soccer/germany-bundesliga/matchups/',
#                 'https://www.pinnacle.com/es/soccer/fifa-world-cup-qualifiers-south-america/matchups/',
#                 'https://www.pinnacle.com/es/soccer/uefa-euro-qualifiers/matchups/',
#                 'https://www.pinnacle.com/es/soccer/uefa-champions-league/matchups/',
#                 ]

pinnacle_urls = ['https://www.pinnacle.com/es/soccer/fifa-world-cup-u17/matchups']
driver = webdriver.Chrome()
driver.implicitly_wait(10)

def get_matches(pinnacle_urls) :
    Matches = []

    for url in pinnacle_urls:
        driver.get(url)
        main = driver.find_element(By.TAG_NAME, "main")
        page = main.find_element(By.CSS_SELECTOR,".contentBlock.square")

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

                sum = 0
                for i in range(len(p)) : 
                    if p[i].text == '' : 
                        p[i] = 0
                        continue
                    p[i] = float(p[i].text)
                    p[i] = (1 / p[i]) * 100 
                    sum += p[i]
                for i in range(len(p)) :
                    if sum == 0 : break
                    p[i] /= sum

                Matches.append(Match(teams[0].text.replace(' (Partido)', ''), teams[1].text.replace(' (Partido)', ''), date.replace(',',''), time.text, p[0], p[1], p[2]))
    return Matches

Matches = get_matches(pinnacle_urls)

f = open("results.csv", "w")

for match in Matches :
    f.write(match.printCSV())

f.close()






    

