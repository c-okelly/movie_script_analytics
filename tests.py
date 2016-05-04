import re

import text_objects

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

    # dog_array = []
    #
    # dog = text_objects.Speech("Hello",0.4)
    # dog_array.append(dog)
    # dog = text_objects.Speech("cat",0.5)
    # dog_array.append(dog)
    # dog = text_objects.Speech("DOG \n yello",0.6)
    # dog_array.append(dog)
    #
    # for i in dog_array:
    #     print(i)
    #
    # new_array = []
    #
    # for i in dog_array:
    #     if i.count >= 0.5:
    #         new_array.append(i)
    #
    # print(new_array)

    d = {"John":1}

    x = ["John","David","John","James","Silly"]
    for i in x:
        if d.get(i):
            d[i] += 1
        else:
            d[i] = 1

    print(d)
