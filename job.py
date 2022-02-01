from bs4 import BeautifulSoup
import requests
import csv

pages = int(input('Enter number of pages: '))
x = 0
skills = []
csv.field_size_limit(10)
with open('e:\Python\Job\File\jobs.csv','w') as f:
    thewriter = csv.writer(f)
    header = ['Title','','','','Company','','Skills','','','','','','','URL']
    thewriter.writerow(header)
    while x<pages:
        if x == 0:
            url = 'https://merojob.com/category/it-telecommunication/'
        else:
            url = 'https://merojob.com/category/it-telecommunication/?page='+str(x+1)
        page = requests.get(url).text

        soup = BeautifulSoup(page, 'lxml')
        address = ['Kathmandu','Remote','KTM']
        # lists = soup.find('div', class_='row job-card text-center text-lg-left')

        for item in soup.find_all('div', class_='row job-card text-center text-lg-left'):
            location = item.find('div', class_='location font-12').text

            for city in address:
                if str.lower(city) in str.lower(location): 
                    title = item.find('a')
                    post = title.text.replace('\n','')
                    more_info = title.get('href')
                    company = item.find('a',class_='text-dark').text.replace('\n','')
                    link = f"https://merojob.com{more_info}".replace('\n','')

                    for skill in item.find_all('span', class_='badge badge-pill badge-light rounded text-muted'):
                        if skill.text!=None:
                           skills.append(skill.text)

                    info = [post,'','','',company,'',skills,'','','','','','',link]
                    thewriter.writerow (info)
                    skills.clear()
        x += 1
print('File created.')