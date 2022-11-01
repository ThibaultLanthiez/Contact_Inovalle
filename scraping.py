import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def get_list_url():
    # list_url = []
    set_url = set()

    driver = webdriver.Chrome("chromedriver")
    driver.implicitly_wait(15)

    driver.get("https://myino.app/#/annuaire")
    driver.find_element(By.XPATH, '//*[@id="cdk-overlay-0"]/mat-bottom-sheet-container/app-cookies-acceptation-sheet/div/button[2]/span').click()
    driver.implicitly_wait(20)

    driver.find_element(By.XPATH, '//*[@id="directory"]/app-list/div/app-search-bar/form/button[2]/span').click()
    driver.implicitly_wait(20)

    for j in range(1,38): # 1 à 37
        driver.find_element(By.XPATH, f'//*[@id="mat-chip-list-1"]/div/mat-chip[{j}]').click() # 1 à 37
        driver.implicitly_wait(20)

    i = 0
    last_url = ''
    while True:
        element = driver.find_element(By.XPATH, f'//*[@id="directory"]/app-list/div/ul/li[1]/a/div[2]/a')
        url = element.get_attribute('href')
        if last_url == url:
            break
        last_url = url
        set_url.add(url)
        print(i+1, url)
        i += 1

        element_to_scroll = driver.find_element(By.XPATH, f'//*[@id="directory"]/app-list/div/ul/li[2]/a/div[2]/a')
        driver.execute_script("arguments[0].scrollIntoView();", 
                                element_to_scroll)
        element_to_scroll = driver.find_element(By.XPATH, f'//*[@id="directory"]/app-list/div/ul/li[3]/a/div[2]/a')
        driver.execute_script("arguments[0].scrollIntoView();", 
                                element_to_scroll)

        time.sleep(2)

    time.sleep(5)

    driver.close()
    return set_url


def write_file(liste):
    with open('list_url.txt', 'w') as fp:
        for item in liste:
            # write each item on a new line
            fp.write("%s\n" % item)

def write_csv(liste):
    with open('list_.csv', 'w') as fp:
        fp.write('Nom,Effectif sur Inovallée,Téléphone\n')
        for item in liste:
            fp.write(f'{",".join(item)}\n')

def read_file():
    liste = []
    with open('list_url.txt', 'r') as fp:
        for line in fp:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[:-1]

            # add current item to the list
            liste.append(x)
    return liste

def get_info(list_url):
    liste_csv = []
    for i, url in enumerate(list_url):
        try:
            driver = webdriver.Chrome("chromedriver")
            driver.implicitly_wait(15)

            driver.get(url)
            driver.find_element(By.XPATH, '//*[@id="cdk-overlay-0"]/mat-bottom-sheet-container/app-cookies-acceptation-sheet/div/button[2]/span').click()
            driver.implicitly_wait(20)

            num_section = 0

            company_name = driver.find_element(By.XPATH, 
                                    '//*[@id="fiche"]/app-header-fiche/header/div/div[2]/h1').text

            tel = driver.find_element(By.XPATH, 
                                    f'//*[@id="fiche"]/app-info-fiche/div/section[{2+num_section}]/ul/li[1]/a/p').text
                                    
            info_element = driver.find_element(By.XPATH, 
                                    f'//*[@id="fiche"]/app-info-fiche/div/section[{1+num_section}]/ul/li[3]/h3').text
            if info_element == "Effectif":
                effective_inovalle = driver.find_element(By.XPATH, 
                                    f'//*[@id="fiche"]/app-info-fiche/div/section[{1+num_section}]/ul/li[4]/p').text
            elif info_element == "Date de départ du Tarmac":                        
                effective_inovalle = driver.find_element(By.XPATH, 
                                    f'//*[@id="fiche"]/app-info-fiche/div/section[{1+num_section}]/ul/li[5]/p').text
            elif info_element == "Date d'implantation au Tarmac":                        
                effective_inovalle = driver.find_element(By.XPATH, 
                                    f'//*[@id="fiche"]/app-info-fiche/div/section[{1+num_section}]/ul/li[6]/p').text
            else:
                effective_inovalle = driver.find_element(By.XPATH, 
                                    f'//*[@id="fiche"]/app-info-fiche/div/section[{1+num_section}]/ul/li[3]/p').text

            driver.close()
            print(i+1, url, company_name, effective_inovalle, tel)
            liste_csv.append([company_name, effective_inovalle, tel])

        except Exception as e:
            continue

    return liste_csv

# list_url = get_list_url()
# write_file(list_url)

list_url = read_file()
liste_csv = get_info(list_url)

write_csv(liste_csv)