from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

pages = int(input('Enter number of pages: '))
x = 0
title = []
company = []
more_info = []
skills = []
skills_required = []
col_names = ['Title','Company','Skills','URL']
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
                post = item.find('a')
                title.append(post.text.replace('\n',''))
                more = post.get('href')
                company.append(item.find('a',class_='text-dark').text.replace('\n',''))
                link = f"https://merojob.com{more}".replace('\n','')
                more_info.append(link)

                for skill in item.find_all('span', class_='badge badge-pill badge-light rounded text-muted'):
                    if skill.text!=None:
                        skills.append(skill.text)
                skillset = ''
                for data in skills:
                    skillset += f'{data},'
                skills_required.append(skillset)
                skills.clear()
    x += 1
info = [title,company,skills_required,more_info]
df = pd.DataFrame(info,index=col_names)
df = df.T

writer = pd.ExcelWriter('File/jobs.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Jobs',index = False)
workbook=writer.book
worksheet = writer.sheets['Jobs']

format = workbook.add_format({'text_wrap': True})

worksheet.set_column('A:D', 15, format)

writer.save()
writer.close()

os.popen("E:/Python/Job/File/jobs.xlsx")