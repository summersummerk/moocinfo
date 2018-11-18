# 爬取MOOC上面的课程信息
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time
import os
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
final_Result = []
count = 0

url = 'https://www.icourse163.org/category/all'
driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
driver.get(url)
driver.maximize_window()  # 将浏览器最大化显示
driver.implicitly_wait(5)

page_Number = 1
max_PageNumber = 1
classNameLs = []
classSchoolLs = []
classTeacherLs = []
exceptionalLs = []
attenderCountLs = []
exceptionalAttenderLs = []
classStatusLs = []
statusExceptionals = []
while True:
    if page_Number > 1 or page_Number > max_PageNumber:
        print("已经爬取了{}页".format(page_Number-1))
        break
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    if page_Number == 1:
        pageLs = soup.find_all(name='a', attrs={'class': 'th-bk-main-gh'})
        max_PageNumber = re.search(r"[1-9][0-9][0-9]", str(pageLs[-2]))
    # 做一个循环，如果页数小于等于最大页数那么它就会一直进行
    className = soup.find_all(name='img', attrs={'height': '150px'})
    classSchool = soup.find_all(name='a', attrs={'class': 't21 f-fc9'})
    classTeacher = soup.find_all(name='a', attrs={'class': 'f-fc9','target':'_blank'})
    classAttender = soup.find_all(name='span', attrs={'class': 'hot'})
    classStatus = soup.find_all(name='span', attrs={'class': 'txt'})
    for classItem in className:
        classList = str(classItem).split('"')
        classNameLs.append(classList[1])
    for school in classSchool:
        schoolList = re.search(r'[\u4e00-\u9fa5]+[\u4e00-\u9fa5]', str(school))
        classSchoolLs.append(schoolList.group(0))
    for teacher in classTeacher:
        teacherList = re.search(r'[\u4e00-\u9fa5]+[\u4e00-\u9fa5]', str(teacher))
        try:
            teacherItem = teacherList.group(0)
            classTeacherLs.append(teacherItem)
        except:
            teacherExceptional = teacherList
            exceptionalLs.append(teacherList)
    for attender in classAttender:
        attenderCount = re.search(r'[1-9][0-9]+[\u4e00-\u9fa5]+', str(attender))
        try:
            attenderItem = attenderCount.group(0)
            attenderCountLs.append(attenderItem)
        except:
            attenderExceptional = attenderCount
            exceptionalAttenderLs.append(attenderExceptional)
    for status in classStatus:
        currentStatus = re.search(r'[1-9|\u4e00-\u9fa5].+[\u4e00-\u9fa5]+', str(status))
        try:
            statusItem = currentStatus.group(0)
            classStatusLs.append(statusItem)
        except:
            statusExceptional = attenderCount
            statusExceptionals.append(statusExceptional)
    # 此处发生错误，无法点击下一页
    driver.find_element_by_link_text("下一页").click()
    time.sleep(3)
    # 此处发生错误无法点击下一页
    page_Number = page_Number + 1
    classNameLs.append(classNameLs)
    classSchoolLs.append(classSchoolLs)
    classTeacherLs.append(classTeacherLs)
    attenderCountLs.append(attenderCountLs)
    classStatusLs.append(classStatusLs)

os.system('taskkill /im chromedriver.exe /F')
os.system('taskkill /im chrome.exe /F')


final_Result = [classNameLs,classSchoolLs,classTeacherLs,attenderCountLs,classStatusLs]

print(final_Result)

