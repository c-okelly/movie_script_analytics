import re

import text_objects
import numpy as np

# f = open("Data/scripts_text/17-Again.txt", 'r')
# text = f.read()
# text = text[900:1500]
# print(text)

# count = len(re.findall("\W+",text))
# print(count)
#
# lines = text.split('\n')
# lines_on_empty = re.split("\n\s+\n", text)
# print(len(lines))
# print(len(lines_on_empty))
#
# # Find empty lines
# count = 0
# for item in lines:
#     if re.search("\A\s+\Z", item):
#         print(count)
#     count += 1
#
# # Search for character names in list
# for item in lines:
#     if re.search("\A\s*Name_character\s*(\(.*\))?\s*\Z", item):
#         print(item)

# # Generate list of characters from the script
# characters = dict()
#
#
# for line in lines:
#     #Strip whitespace and check if whole line is in capital letters
#     line = line.strip()
#     if (line.isupper()):
#
#         # Exclude lines with EXT / INT in them
#         s1 = re.search('EXT\.', line)
#         s2 = re.search('INT\.', line)
#
#         # Select correct lines and strip out and elements within parathenses. Normally continued
#         if (not(s1 or s2)):
#             line = re.sub("\s*\(.*\)","",line)

#             # If character no in dict add them. If a already in increase count by 1
#             if line in characters:
#                 characters[line] = characters[line] + 1
#             else:
#                 characters[line] = 1
#
# print(characters)



# Get description lines

if __name__ == '__main__':

    #
    # string = "           -EARLY APRIL, 1841"
    # print(re.match("^\s+-(\w+\s{0,3},?/?){0,4}(\s\d{0,5})-\s+",string))

    # for i in np.arange(0,1,0.1):
    #     print(i,"to",i+0.1)

    array= [1,3,5,6,1]

    count = 0

