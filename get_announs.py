import os
import json
import requests
from bs4 import BeautifulSoup

def is_exist():
    return os.path.exists("announs.txt")

def get_announs(r, option):
    # Getting the page
    soup = BeautifulSoup(r.content, "html.parser")

    tbody = soup.find("tbody")

    # Finding the announcements
    table_rows = tbody.find_all("tr")[:5]    

    all_announs = []

    hrefs = []
    contents = []
    
    # Getting the hrefs and contents
    for row in table_rows:
        a_tag = row.find("a", href=True)
        
        hrefs.append(a_tag["href"])
        contents.append(a_tag.contents[0])

    # Zipping hrefs and countents
    all_announs = list(zip(hrefs, contents))

    # If there are no announs.txt we will create one (this might mean the bot running for the first time)
    if is_exist():
        # If there are one
        old_announs = []

        # We are reading the old announs
        with open("announs.txt", "r", encoding="UTF-8") as f:
            old_announs = f.readlines()

        last_announ = all_announs[0]
        last_url = "https://www.bilecik.edu.tr" + last_announ[0]
        last_content = last_announ[1].strip()

        # Since we wrote the announs in a txt file, they have become formatted in a different way
        # So we are formatting our all_announs the same way so we can compare them.
        for i, announ in enumerate(all_announs):
            all_announs[i] = str(all_announs[i]) + "\n"
        
        # The text that exist in all_announs but don't exist in old_announs
        difference = list(set(all_announs) - set(old_announs))
        
        # If there are difference we are preparing a announcements text to send it
        if len(difference) > 0:
            new_announs = f"Yeni {len(difference)} duyuru 📢: "

            for diff in difference:
                url = "https://www.bilecik.edu.tr" + diff.split("'")[1]
                content = diff.split("'")[3].strip()
                new_announs += f"\n{content}\n{url}\n"

            with open("announs.txt", "w", encoding="UTF-8") as f:
                for announs in all_announs:
                    f.writelines(str(announs) + "\n")
                
            return True, new_announs
        
        return False, f"Yeni bir duyuru yok.\n\nYayınlamış son duyuru:\n{last_content}\n{last_url}"
        
    else:
        # Creating the announs.txt and writing into it
        with open("announs.txt", "w", encoding="UTF-8") as f:
            for announs in all_announs:
                f.writelines(str(announs) + "\n")

        return False, "Program ilk defa çalışıyor."
    
def announcements(option):
    # Requesting the url
    url = "https://bilecik.edu.tr/bilgisayar/arama/4"

    r = requests.get(url)

    if r.status_code == 200:
        return get_announs(r, option)
    else:
        print(f"Connection to {url} has failed.\nStatus: {r.status_code}")
