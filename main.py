from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
from fractions import Fraction

# Setup
option = webdriver.ChromeOptions()
option.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
# driver_path = "C:/Users/Jerico Rangel/Documents/chromedriver-win64/chromedriver-win64/chromedriver.exe"
# driver = webdriver.Chrome(executable_path=driver_path, options=option)
driver = webdriver.Chrome(options=option)

def scrape_recipe(url: str, target_class: str, p: float) -> pd.DataFrame:
    """
    Quick recipe scraper for scaling a Cooknook recipe for a specified portion

    :param url: cookingnook url
    :type url: str
    :param target_class: ingredients class from DOM
    :type target_class: str
    :param p: number of portions
    :type p: float

    :return: DF with the necessary ingredient amounts and descriptions
    :rtype: DataFrame
    """
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    recipe_name = soup.find('h1').text
    print(f'Recipe for {recipe_name} with {p} portions')

    amount_arr = []
    desc_arr = []
    ingredients = soup.find_all(class_=target_class)

    for n in ingredients:
        line = n.text

        # Amounts
        amt = re.findall(r'^\S+', line)
        if amt[0].isdigit():
            amount_arr.append(p*float(amt[0]))
        elif '/' in amt[0]:
            result = float(sum(Fraction(s) for s in amt[0].split()))
            amount_arr.append(p*result)
        else:
            amount_arr.append(0)

        # Descriptions
        _desc = re.findall(r'[^0-9.]', line)
        desc = ''.join(_desc).replace('-', '').replace('/', '').strip()
        desc_arr.append(desc)

    df = pd.DataFrame(dict(amount=amount_arr, notes=desc_arr))

    return df


def scrape_recipe2(url: str, target_class: str, p: float) -> pd.DataFrame:
    """
    Possibly better(?) recipe scraper for scaling a Cooknook recipe for a specified portion

    :param url: cookingnook url
    :type url: str
    :param target_class: ingredients class from DOM
    :type target_class: str
    :param p: number of portions
    :type p: float

    :return: DF with the necessary ingredient amounts and descriptions
    :rtype: DataFrame
    """
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    recipe_name = soup.find('h1').text
    print(f'Recipe for {recipe_name} with {p} portions')

    ingredients = soup.find_all(class_=target_class)

    info_arr = []
    for n in ingredients:
        specific_soup = BeautifulSoup(str(n), 'html.parser')

        amount = specific_soup.find('span', class_='wprm-recipe-ingredient-amount')
        unit = specific_soup.find('span', class_='wprm-recipe-ingredient-unit')
        name = specific_soup.find('span', class_='wprm-recipe-ingredient-name')
        notes = specific_soup.find('span', class_='wprm-recipe-ingredient-notes')

        amt = amount.text if amount else ''
        if amt.isdigit():
            amt = p*float(amt)
        elif '/' in amt:
            result = float(sum(Fraction(s) for s in amt.split()))
            amt = p*result
        else:
            amt = 0

        info_arr.append(
            dict(Amount=amt,
                 Unit=unit.text.strip() if unit else None,
                 Ingredient=name.text.strip() if name else None,
                 Notes=notes.text.strip() if notes else None)
        )

    df = pd.DataFrame(info_arr)

    return df

if __name__ == '__main__':
    url = 'https://www.cookingnook.com/recipe/carbonara/'

    # df1 = scrape_recipe(url=url, target_class='wprm-recipe-ingredient', p=2)
    # print(df1)

    df2 = scrape_recipe2(url=url, target_class='wprm-recipe-ingredient', p=2)
    print(df2.to_string())
