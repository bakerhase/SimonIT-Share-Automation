# -*- coding: utf-8 -*-
"""
Created March 2023

@author: Baker Hase

If you have questions or bugs to report, email me at bhase@u.rochester.edu

Currently there are no error returns, the script will just not fully function
"""

# All required packages come with python by default (tkinter) or from selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import tkinter as tk

# Takes the first three letter abbreviation of a month and returns a two-digit month as a string
def monthnum (month):
    if month == 'Jan' or month == 'jan':
        return '01'
    elif month == 'Feb' or month == 'feb':
        return '02'
    elif month == 'Mar' or month == 'mar':
        return '03'
    elif month == 'Apr' or month == 'apr':
        return '04'
    elif month == 'May' or month == 'may':
        return '05'
    elif month == 'Jun' or month == 'jun':
        return '06'
    elif month == 'Jul' or month == 'jul':
        return '07'
    elif month == 'Aug' or month == 'aug':
        return '08'
    elif month == 'Sep' or month == 'sep':
        return '09'
    elif month == 'Oct' or month == 'oct':
        return '10'
    elif month == 'Nov' or month == 'nov':
        return '11'
    elif month == 'Dec' or month == 'dec':
        return '12'


# Takes the date in the format used by Echo and turns it into the format used by the Help Desk
def dateformat(datestring):
    monthstr = datestring[0:3]
    month = monthnum(monthstr)
    daystr = datestring[4:8]
    if daystr[3]==' ':
        day = '0'+daystr[0]
        year = datestring[10:12]
    else:
        day = daystr[0:2]
        year = datestring[11:13]
    date_formatted = month+'.'+day+'.'+year
    return date_formatted

# Passed in the title of an echo recording page, returns a string of the total course number (e.g. CIS442.31B)
def titleparse(page_title):
    endidx = page_title.index("'")
    reverse_title = ''
    flag = 0
    idxadd = -1
    while flag == 0:
        if page_title[endidx+idxadd] == ' ':
            flag = 1
        else:
            reverse_title+=page_title[endidx+idxadd]
            idxadd += -1
    
    course_title = reverse_title[::-1]
    return course_title


def assigntoprofessor(driver, course_name):
    details_button = driver.find_element(By.ID, 'content-tab-details')
    details_button.click()
    
    change_owner_button = driver.find_element(By.ID, 'change-owner-open')
    change_owner_button.click()
    
    owner_dropdown = driver.find_element(By.ID, 'change-owner-select_input')
    owner_dropdown.click()
    
    owner_dropdown_input = driver.find_element(By.ID, 'react-select-4-input')
    owner_dropdown_input.send_keys('glenn.huels@simon.rochester.edu')
    
    #done_button = driver.find_element(By.ID, 'change-owner-done')
    #done_button.click()

def scrollbarchecker(idstr):
    truthval = True
    
    checklist = []
    for num in [0,1,2,3,4,5,6,7]:
        checklist.append('react-select-12-option-'+str(num))
        checklist.append('react-select-7-option-'+str(num))
    
    for idref in checklist:
        if idstr == idref:
            truthval = False
    
    if truthval:
        return True
    else:
        return False
            

# Main function which opens and fills information for classes in Google Chrome
# Passed in a URAD username and password, as well as a list of URLs for the desired classes
def script(uname, pwrd, urllist):
    # All the data that is necessary for the script at current moment.
    usremail = uname+'@u.rochester.edu'# ASSUMES AD USERNAME IS THE SAME AS EMAIL ADDRESS. CORRECT ASSUMPTION?
    usrname = uname
    passwrd = pwrd
    tgtURL = "https://echo360.org/home"
    term = 'Spring 2023' # CURRENTLY NEEDS TO BE CHANGED MANUALLY EACH TERM

    # Makes it so the window stays open after program execution
    chrome_options = Options()
    chrome_options.add_experimental_option("detach",True)
    
    # Starts webdriver service
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options = chrome_options) #option call also needed for persistent window
    driver.get(tgtURL)


    # Enters email into Echo login page
    email_field = driver.find_element(by=By.ID, value = "email")
    email_field.send_keys(usremail)
    submit_button = driver.find_element(By.ID,value='submitBtn')
    submit_button.click()


    driver.implicitly_wait(0.5)


    # Enters active directory username and password into UR login page
    uname_field = driver.find_element(By.ID, "usernamevis")
    pwrd_field = driver.find_element(By.ID, "password")
    logon_button = driver.find_element(By.ID, "log-on")

    uname_field.send_keys(usrname)
    pwrd_field.send_keys(passwrd)

    # specifically navigates the dropdown menu
    domain_select = driver.find_element(By.ID, "domain")
    d_select = Select(domain_select)
    d_select.select_by_value("@ur.rochester.edu")

    logon_button.click()


    # While loop prevents the rest of the script from running until properly on the Echo site
    title = driver.title

    while len(title)<2 or title[1] != 'o': # Length requirement prevents error if title is an empty string
        driver.implicitly_wait(0.5)
        title = driver.title
    
    # Loops over each URL in the given URL list
    for URL in urllist:
        
        driver.switch_to.new_window('tab')
        driver.get(URL)
        
        #driver.implicitly_wait(40)
        
        title = driver.title
        # Takes course name from title of webpage to later pass into fields
        
        total_coursename = titleparse(title)
    
        course_type = total_coursename[0:3]
        course_number = total_coursename[3:]
    
    
        #driver.implicitly_wait(15)
    
        date_elt = driver.find_element(By.ID, 'created-timestamp')
        datestring = date_elt.get_attribute('title')
        date = dateformat(datestring)
    
        #assigntoprofessor(driver, course_number) ### REMOVE IN THE CASE OF NOT WANTING TO UPKEEP DICTIONARY
    
        #Press the 'Share' button
        share_button = driver.find_element(By.ID,'share-button')
        share_button.click()
    
        #driver.implicitly_wait(150)
    
        #Press the 'Class' tab
        class_tab_button = driver.find_element(By.CSS_SELECTOR , "button[id*='share-tabs-tab-2']")
        class_tab_button.click()
    
        #Navigates 'Course' dropdown menu
        course_type_dropdown = driver.find_element(By.ID, "shareWithClass-courseSelect_input")
        course_type_dropdown.click()
    
        #course_dropdown_input = driver.find_element(By.ID, 'react-select-6-input')
        #course_dropdown_input.send_keys(course_type+':')
        #course_dropdown_input.send_keys(Keys.RETURN)
    
        course_type_selection = driver.find_element(By.XPATH , "//*[contains(text(),'"+course_type+":"+"')]")
        course_type_selection.click()
    
        #Navigates 'Term' dropdown menu
        term_dropdown = driver.find_element(By.ID,"shareWithClass-termSelect_input")
        term_dropdown.click()
    
        #term_dropdown_input = driver.find_element(By.ID, "react-select-7-input")
        #term_dropdown_input.send_keys(term)
        #term_dropdown_input.send_keys(Keys.RETURN)
    
        term_selection = driver.find_element(By.XPATH , "//*[text()='"+term+"']")
        term_selection.click()
    
        #Navigates 'Section' dropdown menu
    
        section_dropdown = driver.find_element(By.ID,"shareWithClass-sectionSelect_input")
        section_dropdown.click()
        
        section_selection = driver.find_element(By.XPATH , "//*[text()='"+course_number+"']")
        section_id = section_selection.get_attribute('id')
        
        scroll_bool = scrollbarchecker(section_id)
        
        if scroll_bool:
    
            section_dropdown_input = driver.find_element(By.XPATH, '''//*[@id="react-select-7-input"]''')
            section_dropdown_input.send_keys(course_number)
    
            section_dropdown_input.send_keys(Keys.RETURN)
        else:
            section_selection.click()
        
        
    
        #presses the 'New Class' button
        new_class_tab_button = driver.find_element(By.ID, "shareWithClass-classTabs-tab-new-class")
        new_class_tab_button.click()
    
        #Enters recording name into 'Class Name' field
        class_name_field = driver.find_element(By.NAME, "className")
        class_name_field.send_keys("Zoom."+total_coursename+"-"+date)
    

    
# Performs the functions of the 'submit' button. Deletes values in entries of the GUI
# Calls script passing in the user-entered URAD credentials and URL list
def run_script():
    uname = uname_entry.get()
    pwrd = pwrd_entry.get()
    urlstring = URL_box.get("1.0",tk.END)
    newstr = urlstring.replace('\n','`')
    
    urllist = []
    entry = ''
    stopidx = len(newstr)-1
    idx = 0
    for elt in newstr:
        if elt != '`':
            entry+=elt
            if idx+1 == stopidx:
                urllist.append(entry)
        elif elt =='`' and idx != stopidx:
            urllist.append(entry)
            entry=''
        elif elt == '`' and idx ==stopidx:
            continue
            
        idx+=1
    
    uname_entry.delete(0, tk.END)
    pwrd_entry.delete(0,tk.END)
    URL_box.delete("1.0",tk.END)
    script(uname, pwrd, urllist)
    advisory_label["text"]='Done!'
    
   
    

# Generates GUI window
window = tk.Tk()
window.title("Zoom Recording Share Automation")
window.withdraw() #hides main window until Read me is addressed

# Labels and creates username entry field
uname_label = tk.Label(text='AD User')
uname_entry = tk.Entry(fg='black', bg='white', width = 50)

# Labels and creates password entry field
pwrd_label = tk.Label(text='AD Password')
pwrd_entry = tk.Entry(fg='black', bg='white', show = '*', width = 50)

# Labels and creates URL entry text box
URL_label = tk.Label(text = 'Start each class recording URL on a new line')
URL_box = tk.Text() #Play with text wrapping. Is it better for no wrapping? Will that be confusing? Will having text wrapping be confusing?


#Labels and creates submit button
submit = tk.Button(text='Submit for Upload Process', command=run_script)


advisory_label = tk.Label(text = ' ')



# Adds GUI elements to the window
uname_label.pack()
uname_entry.pack()
pwrd_label.pack()
pwrd_entry.pack()
URL_label.pack()
URL_box.pack()
submit.pack()
advisory_label.pack()

# Shows a READ ME box giving info on the state of the app and some disclaimers
tk.messagebox.showinfo(title = 'READ ME', message = 'Hello! This app is a work in progress.\n\u2022Currently, it autofills the information for sharing zoom course recordings.\n\u2022It DOES NOT ASSIGN the recording to the instructor (though it may in the future).\n\u2022This app throws up NO ERROR MESSAGES if an input is incorrect (e.g. typo in AD Username).\n\u2022It assumes that the email that gets you into echo is of the form ADUsername@u.rochester.edu.\n\u2022Be sure to DOUBLE CHECK any and all auto-filled information. I take no responsibility for any errors in shared class information as a result of usage of this app.\n\u2022It stores no data whatsoever on your AD credentials. This app is entirely open-source, so you may verify this personally if you feel so inclined.\n\u2022If you find any bugs or if the assumption about email format is wrong, please notify Baker either in person or at bhase@u.rochester.edu.\n\u2022You can find the source code on my GitHub, github.com/bakerhase')
window.deiconify() #shows the main app window once the Read Me has been addressed




window.mainloop()



