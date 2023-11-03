# -*- coding: utf-8 -*-
import csv

def get_instructor_from_row (row_list):
    instructors = row_list[11]
    instructors = instructors.replace("kpeck7@UR.Rochester.edu", "")
    instructors = instructors.replace("Jessica.Mcdermott@simon.Rochester.edu", "")
    instructors = instructors.replace("abarkhim@simon.rochester.edu", "")
    
    number_of_semicolons = 0
    for char in instructors:
        if char ==";":
            number_of_semicolons+=1
    
    first_semicolon_index = instructors.find(";")
    second_semicolon_index = instructors.find(";",first_semicolon_index+1)
    if instructors == "":
        return -1
    elif first_semicolon_index == -1:
        instructor_email = instructors
        return instructor_email
    elif instructors[0:first_semicolon_index] != "":
        instructor_email = instructors[0:first_semicolon_index]
        return instructor_email
    elif second_semicolon_index == -1:
        instructor_email = instructors[first_semicolon_index+1:]
        return instructor_email
    elif instructors[first_semicolon_index+1:second_semicolon_index] != "":
        instructor_email = instructors[first_semicolon_index+1:second_semicolon_index]
        return instructor_email
    else:
        return -1
    

def get_title_from_row (row_list):
    
    alt_flag = 0
    course_code = row_list[2]
    if len(course_code)>3:
        course_type = course_code.replace(" ", "")
        alt_flag = 1
    else:
        course_type = course_code
    
    course_section = row_list[6]
    
    num_idx = 0
    for char in course_section:
        if char != "0":
            break
        else:
            num_idx+=1
    
    course_section = course_section[num_idx:]
    
    if alt_flag == 1:
        course_title = course_type+"."+course_section
    else:
        course_title = course_type+course_section
    
    return [course_title, alt_flag]
        


def main():
    sectioncsv = open("sections.csv", newline="")
    sectionreader = csv.reader(sectioncsv, delimiter=",")
    
    target_term = "Fall 2023"#input("What is the target term? ")
    
    dict_rows = []
    exception_courses = []
    for row in sectionreader:
        if row[5] == target_term:
            title_return = get_title_from_row(row)
            course_title = title_return[0]
            exception_flag = title_return[1]
            if exception_flag == 1:
                exception_courses.append(course_title)
            instructor_email = get_instructor_from_row(row)
            if instructor_email != -1:    
                dict_rows.append(course_title+":"+instructor_email)
    
    configfile = open("config.txt", "w")
    configfile.write("term:"+target_term+"\n\n")
    for outrow in dict_rows:
        configfile.write(outrow+"\n")
    
    exception_file = open("exception_courses.txt","w")
    exception_file.write("Graduate course exceptions:\n\n")
    for exception_course in exception_courses:
        exception_file.write(exception_course+"\n")
    
    configfile.close()
    exception_file.close()
    sectioncsv.close()
    
main()
        
        
    
    
