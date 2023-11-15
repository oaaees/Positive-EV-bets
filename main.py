from selenium import webdriver
from selenium.webdriver.common.by import By

class Match:
    def __init__(self, team1, team2, date, time, p1, ptie, p2, odds1, oddstie, odds2):
        self.team1 =  team1
        self.team2 = team2
        self.date = date
        self.time = time
        self.p1 = p1
        self.ptie = ptie
        self.p2 = p2
        self.odds1 = odds1
        self.oddstie = oddstie
        self.odds2 = odds2
    def print(self) :
        print(f'{self.team1} vs {self.team2} with prob {self.p1:.5f} - {self.ptie:.5f} - {self.p2:.5f}')
    def printCSV(self) :
        return f'{self.team1},{self.team2},{self.p1:.5f},{self.ptie:.5f},{self.p2:.5f},{self.odds1},{self.oddstie},{self.odds2},{ ((self.odds1 - 1)* self.p1) - self.ptie - self.p2 },{((self.oddstie - 1)* self.ptie) - self.p1 - self.p2 },{((self.odds2 - 1)* self.p2) - self.p1 - self.ptie },{self.p1*(1*(self.odds1 - 1) - (1 + 0)) + self.ptie*(1*(self.oddstie - 1) - (1 + 0)) + self.p2*(0*(self.odds2 - 1) - (1 + 1))},{self.p1*(1*(self.odds1 - 1) - (1 + 0)) + self.ptie*(0*(self.oddstie - 1) - (1 + 1)) + self.p2*(1*(self.odds2 - 1) - (0 + 1))},{self.p1*(0*(self.odds1 - 1) - (1 + 1)) + self.ptie*(1*(self.oddstie - 1) - (0 + 1)) + self.p2*(1*(self.odds2 - 1) - (0 + 1))},{self.date} - {self.time}\n'


#pinnacle_urls = ['https://www.pinnacle.com/es/soccer/spain-la-liga/matchups/',
#                 'https://www.pinnacle.com/es/soccer/england-premier-league/matchups/',
#                 'https://www.pinnacle.com/es/soccer/italy-serie-a/matchups/',
#                 'https://www.pinnacle.com/es/soccer/germany-bundesliga/matchups/',
#                 'https://www.pinnacle.com/es/soccer/fifa-world-cup-qualifiers-south-america/matchups/',
#                 'https://www.pinnacle.com/es/soccer/uefa-euro-qualifiers/matchups/',
#                 'https://www.pinnacle.com/es/soccer/uefa-champions-league/matchups/',
#                 ]

pinnacle_urls = ['https://www.pinnacle.com/es/soccer/fifa-world-cup-u17/matchups/', 
                 'https://www.pinnacle.com/es/soccer/fifa-world-cup-qualifiers-south-america/matchups/#all',
                 'https://www.pinnacle.com/es/soccer/fifa-world-cup-qualifiers-asia/matchups/',
                 'https://www.pinnacle.com/es/soccer/fifa-world-cup-qualifiers-africa/matchups/',
                 'https://www.pinnacle.com/es/soccer/uefa-euro-qualifiers/matchups/',
                 'https://www.pinnacle.com/es/soccer/concacaf-nations-league/matchups/']
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
                
                print(f"Enter odds for {teams[0].text.replace(' (Partido)', '')} vs {teams[1].text.replace(' (Partido)', '')}")
                print(f"Enter odds for {teams[0].text.replace(' (Partido)', '')}")
                odds1 = float(input())
                print(f"Enter odds for tie")
                oddstie = float(input())
                print(f"Enter odds for {teams[1].text.replace(' (Partido)', '')}")
                odds2 = float(input())

                Matches.append(Match(teams[0].text.replace(' (Partido)', ''), teams[1].text.replace(' (Partido)', ''), date.replace(',',''), time.text, p[0], p[1], p[2], odds1, oddstie, odds2))
    return Matches

Matches = get_matches(pinnacle_urls)
    

f = open("results.csv", "w")
f.write(f'TEAM1, TEAM2, P1, PTIE, P2, ODDS1, ODDSTIE, ODDS2, EV1, EVTIE, EV2, EV1TIE, EV12, EV2TIE, DATE\n')

for match in Matches :
    f.write(match.printCSV())

f.close()






    

