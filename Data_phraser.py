#Author - Conor O'Kelly
# The main code to take in and prase the text files

from bs4 import BeautifulSoup
import os
import sys

# Increase maximum recusrion depth
sys.setrecursionlimit(20000)

def clean_html_and_save_to_file(file_directory,file_name,save_directory):
    try:
        #File location
        file_path = file_directory + file_name
        # Open file and turn into beautiful soup object
        with open(file_path, "r",encoding="utf-8",errors="ignore") as file:
            soup_object = BeautifulSoup(file)
        # print(soup_object)

        # Select correct section using class. Then select correct subsection of this class
        # Comment out as was casuing some scripts to be coorectly selected 
            # div_section = soup_object.find("td",{"class":"scrtext"})
            # text_section = div_section.find("pre")

        text_section = soup_object.getText()

        #  Convert all text to string
        str_text_section = str(text_section)

        # Save text to file
        new_file_name = file_name.replace(".html",".txt") # change file extension
        save_path = save_directory + new_file_name
        new_file = open(save_path,"w")
        new_file.write(str_text_section)



    except FileExistsError:
        print("File not found")

def run_text_cleaner_for_directory(file_directory, save_directory):
    # Find all files in directory and run them through clean_html_and_save_to_file
    list_all_files = os.listdir(file_directory)

    # Trim list for unwanted pdf and hidden files
    list_files_to_convert = []
    count = 0

    for item in list_all_files:
        if item[-3:] != "pdf":      # Check file is not pdf
            if item[0:1] != ".":    # Check not hidden file
                list_files_to_convert.append(item)      # Add to list of target files
                count += 1

    print(list_files_to_convert)
    # Run all items through function
    for file in list_files_to_convert[0:20]:
        try:
            clean_html_and_save_to_file(file_directory,file,save_directory)
            print(file)
        except:
            print("The file %s has failed to convert" % file)
            print(sys.exc_info()[0])
            pass

if __name__ == '__main__':
    print("Start")
    file_directory = "Data/scripts_html/"
    save_directory = "Data/scripts_text/"
    run_text_cleaner_for_directory(file_directory,save_directory)
    # clean_html_and_save_to_file(file_directory,"12.html",save_directory)
