#importing python library
from plyer import notification
import time
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from tkinter import *
from tabulate import tabulate
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
#send request to the url to get the data
def getData(url):
    r = requests.get(url)
    return r.text
def getData2(url):
    r=requests.get(url)
    return r.text
#notification function
def notifyMe(title, message):
    notification.notify(
        title=title,
        message=message,
        app_icon='C://Users//umer//PycharmProjects//corona//icon1.ico',
        timeout=20
    )
#this is the function to print the data state wise
def printtable():
 url="https://www.mohfw.gov.in/"
 response=requests.get(url).content
 soup=BeautifulSoup(response,'html.parser')
 header=[]
 for i in soup.find_all('th'):
    header.append(i.text)
 table=PrettyTable(header)
 rw=[]
 for row in soup.find_all('tr')[1:35]:
    for i in row.find_all('td'):
        rw.append(i.text)
    table.add_row(rw)
    rw=[]
 return table
#this is the function which return the detail of the covid-19 cases in india
def get_corona_detail():
    url="https://www.mohfw.gov.in/"
    html_data=getData2(url)
    soup=BeautifulSoup(html_data,'html.parser')
    active_status=soup.find("div",class_="status-update").find("h2").get_text()
    a1=active_status
    info_div=soup.find("div",class_="site-stats-count").find_all("li",class_="bg-blue")
    info_div2=soup.find("div", class_="site-stats-count").find_all("li", class_="bg-green")
    info_div3= soup.find("div", class_="site-stats-count").find_all("li", class_="bg-red")
    info_div4 = soup.find("div", class_="site-stats-count").find_all("li", class_="bg-orange")
    all_details = ""
    for item in info_div:
        text = item.find("span").get_text()
        count = item.find("strong").get_text()
        #print(text + ":" + count)
    for item in info_div2:
        text2 = item.find("span").get_text()
        count2 = item.find("strong").get_text()
        #print(text2 + ":" + count2)
    for item in info_div3:
        text3 = item.find("span").get_text()
        count3 = item.find("strong").get_text()
        #print(text3 + ":" + count3)
    for item in info_div4:
        text4 = item.find("span").get_text()
        count4 = item.find("strong").get_text()
        #print(text4 + ":" + count4)
        all_details=all_details + a1+"\n" +text + ":" + count+"\n"+text2 + ":" + count2+"\n"+text3 + ":" + count3+"\n" +text4 + ":" + count4+"\n"

    return( all_details)
#this is the function which refrehed the data
def refresh():
   print("Refreshing.....")

content_extract_fromMOH = lambda row: [x.text.replace('\n', '') for x in row]
URL = 'https://www.mohfw.gov.in/'
SHORT_HEADERS = ['SNo', 'State', 'Indian-Confirmed', 'Cured', 'Death']
response = requests.get(URL).content
soup = BeautifulSoup(response, 'html.parser')
header = content_extract_fromMOH(soup.tr.find_all('th'))
stats = []
all_rows = soup.find_all('tr')
for row in all_rows:
    stat = content_extract_fromMOH(row.find_all('td'))
    if stat:
        if len(stat) == 6:
            # last row
            stat = ['', *stat]
            stats.append(stat)
        elif len(stat) == 5:
            stats.append(stat)
stats[-1][1] = "Total Cases"
stats.remove(stats[-1])
objects = []
for row in stats:
    objects.append(row[2])
y_pos = np.arange(len(objects))
performance = []
for row in stats[:len(stats)] :
    performance.append(int(row[3]))
for row in stats:
    if stat:
        if len(stat) == 6:
            stat = ['', *stat]
            stats.append(stat)
table = tabulate(stats, headers=SHORT_HEADERS, tablefmt="pretty")
data1 = {'states': objects, 'confirmed': performance }
df1 = pd.DataFrame(data1, columns=['states', 'confirmed'])

# function to get the World coronavirus informationfrom tabulate import tabulate
def extracting_Worldcoronaviruscases(url):
    # getting the request from the url
    data = requests.get(url)
    # converting the text
    soup = BeautifulSoup(data.text, 'html.parser')
    # finding meta info for total cases
    total = soup.find("div", class_="maincounter-number").text
    # filtering it
    total = total[1: len(total) - 2]
    # finding meta information for the other numbers
    other = soup.find_all("span", class_="number-table")
    # getting recovered cases number
    recovered = other[2].text
    # getting death cases number
    deaths = other[3].text
    # filtering the data
    deaths = deaths[1:]
    # saving details in dictionary
    ans = {'Total Cases': total, 'Recovered Cases': recovered,'Total Deaths': deaths}
    # returnng
    return ans
# THIS IS THE COVID-19 CASES WINDOW GUI
root = Tk()
root.geometry("800x450")
root.title("COVID-19 TRACKER")
root.configure(background='white')
f = ("poppins", 20, "bold")
banner = PhotoImage(file="covid1.png")
bannerLabel = Label(root, image=banner)
bannerLabel.pack()
mainLabel = Label(root, text=get_corona_detail(), font=f, bg='red').pack()
button = Button(root, text="REFRESH", font=f, relief='solid', command=refresh).pack()
root.mainloop()
# THIS IS THE STATE-WISE CASES WINDOW
root1 = Tk()
root1.geometry("800x450")
root1.title("STATEWISE-DATA")
root1.configure(background='white')
f1= ("poppins", 7, "bold")
mainLabel1=Label(root1,text="COVID-19 CASES STATE WISE").pack()
mainLabel1 = Label(root1, text=printtable(), font=f1, bg='pink').pack()
root1.mainloop()
#THIS IS THE GRAPH OF COVI-19 STATE WISE
root2 = Tk()
root2.geometry("800x450")
root2.title("STATEWISE GRAPH")
root2.configure(background='white')
figure1=plt.Figure(figsize=(10,5),dpi=100)
ax1=figure1.add_subplot(111)
bar1= FigureCanvasTkAgg(figure1,root2)
bar1.get_tk_widget().pack()
df1 = df1[['states', 'confirmed']].groupby('states').sum()
df1.plot(kind='barh', legend=True, ax=ax1)
ax1.set_xlabel('Confirmed Cases in States')
ax1.set_title('State vs Confirmed Cases')
root2.mainloop()
# IT IS THE FUNCTION TO CALLING THE NOTIFICATION
if __name__ == "__main__":
    print(get_corona_detail())
    print(printtable())
    myHtmlData = getData('https://www.mohfw.gov.in/')
    soup = BeautifulSoup(myHtmlData, 'html.parser')
    myDatastr = ""
    for tr in soup.find_all('tbody')[0].find_all('tr'):
        myDatastr = tr.get_text()
        myDatastr = myDatastr[1:]
        itemlist = (myDatastr.split("\n\n"))
        states = ['Chandigarh', 'Delhi', 'Goa', 'Manipur','Uttar Pradesh','Punjab','Tamil Nadu']
        for item in itemlist:
             datalist = item.split('\n')
             if datalist[1] in states:
              print(datalist)
              ntitle = 'Cases in Covid-19'
              ntext = f"STATE {datalist[1]}\nTotal:{datalist[2]}\nCured:{datalist[3]}\nDeath:{datalist[4]}"
              notifyMe(ntitle, ntext)
              time.sleep(2)




