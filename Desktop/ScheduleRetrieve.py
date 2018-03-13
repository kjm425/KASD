from selenium import webdriver
import bs4 as bs
import re

#Fill the two fields below to make it work
drexelusername = "kjm425"
bannerwebPIN = "139666"

browser= webdriver.Firefox()
browser.get('https://banner.drexel.edu/pls/duprod/bwskfshd.P_CrseSchd')
bannerUsername = browser.find_element_by_xpath('//*[@id="UserID"]')
bannerPassword = browser.find_element_by_xpath('/html/body/div[3]/form/table/tbody/tr[2]/td[2]/input')
bannerSubmit = browser.find_element_by_xpath('/html/body/div[3]/form/p/input')
bannerUsername.send_keys(drexelusername)
bannerPassword.send_keys(bannerwebPIN)
bannerSubmit.click()
browser.get('https://banner.drexel.edu/pls/duprod/bwskfshd.P_CrseSchd')
source= browser.page_source
soup=bs.BeautifulSoup(source,"lxml")
table=soup.find("table",{"class":"datadisplaytable"})
table_rows=table.find_all('tr')
classes = re.findall("(\w{4}\s\d{3}.+\d+:\d\d\w\w)",str(table_rows))

WeekdayTranslation={
    "0":"Monday",
    "1":"Tuesday",
    "2":"Wednesday",
    "3":"Thursday",
    "4":"Friday",
    '5':"Saturday",
    "6":"Sunday"
}

for x in range(len(classes)):
    classes[x] = re.sub("<br/>.+<br/>",'',classes[x])
schedule=[]
for tr in table_rows:
    td = tr.find_all("td")
    row = [i.text for i in td]
    for element in range(len(row)):
        rowelement= re.findall("(\w{4}\s\d{3}.+\d+:\d\d\s\w\w)", row[element])
        rowelement.append(WeekdayTranslation[str(element)])
        if len(rowelement)>1:
            rowelement[0] = re.sub("-.+Class", ',', rowelement[0])
            schedule.append(rowelement)

print(schedule)
Monday = ["Monday"]
Tuesday = ["Tuesday"]
Wednesday = ["Wednesday"]
Thursday = ["Thursday"]
Friday = ["Friday"]
for y in range(len(schedule)):
    if schedule[y][1]=="Monday":
        Monday.append(schedule[y][0])
    elif schedule[y][1] == "Tuesday":
        Tuesday.append(schedule[y][0])
    elif schedule[y][1] == "Wednesday":
        Wednesday.append(schedule[y][0])
    elif schedule[y][1] == "Thursday":
        Thursday.append(schedule[y][0])
    elif schedule[y][1] == "Friday":
        Friday.append(schedule[y][0])
file = open("myschedule.txt","w")
Days= [Monday,Tuesday,Wednesday,Thursday,Friday]
for day in Days:
    file.write(day[0])
    for z in range(1,len(day)):
        file.write("|" + day[z])
    file.write(";")
file.close()