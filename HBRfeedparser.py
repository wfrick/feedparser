import feedparser
import urllib2
import csv
import datetime

titles = []
staff = ['Justin Fox', 'Walter Frick', 'Gretchen Gavett', 'Sarah Green',
         'Katherine Bell', 'Maureen Hoch', 'Julia Kirby', 'Dan McGinn']

#convert published time stamp into day of the week
def day_of_week(published):
    year = str(published)[0:4]
    month = str(published)[5:7]
    day = str(published)[8:10]
    day_of_week = datetime.date(int(year), int(month), int(day)).weekday()
    return day_of_week

def insight_center(post):
    IC_tag = "insight-center-head"
    if IC_tag in str(post['content']):
        return True
    else:
        return False

#Open the file and save Headlines in a list
with open('dummyfile.csv') as csvfile:
    datareader = csv.reader(open('dummyfile.csv', 'rU'), dialect=csv.excel_tab, delimiter=",")
    for row in datareader:
         titles.append(str(row[0])) 

#Access the HBR RSS feed
HBR = feedparser.parse("http://feeds.harvardbusiness.org/harvardbusiness")

#This is to offset an annoying spacing issue
with open('dummyfile.csv', 'a') as csvfile:
    datawriter = csv.writer(open('dummyfile.csv', 'a'), dialect=csv.excel_tab, delimiter=",")
    datawriter.writerow('')
        
#Iterate through posts in RSS feed and add to CSV doc
for a in HBR.entries:
    #Check list of Headlines to see if this post is already in the file
    if a['title'].encode('utf-8') not in titles:
        new_row = []
        #Store title and author in a list
        new_row.append(a['title'].encode('utf-8'))
        new_row.append(a['author'].encode('utf-8'))
        #Check if author is staff, add answer to list
        if a['author'] in staff:
            new_row.append("Yes")
        else:
            new_row.append("No")
        new_row.append(a['feedburner_origlink'].encode('utf-8'))
        #Add time published to list
        new_row.append(a['published'].encode('utf-8'))
        #Add day of week
        new_row.append(day_of_week(a['published']))
        #Add Is_insight_center
        if insight_center(a) == True:
            new_row.append("Yes")
        else:
            new_row.append("No")
        #Add list as new row to CSV file
        with open('dummyfile.csv', 'a') as csvfile:
            datawriter = csv.writer(open('dummyfile.csv', 'a'), dialect=csv.excel_tab, delimiter=",")
            datawriter.writerow(new_row)
        new_row = []   

#Still to do: Tags/Categories
#In-post images and charts (look to be coming through in RSS)
#Word count
#Expand/confirm Is Staff list
