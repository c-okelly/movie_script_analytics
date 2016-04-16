import re

f = open("Data/scripts_text/17-Again.txt", 'r')
text = f.read()
text = text[1000:1800]
print(text)

lines = text.split('\n')
print(lines)

count = 0
# for item in lines:
#     if re.search("\A\s+\Z", item):
#         print(count)
#     count += 1

# for item in lines:
#     if re.search("\A\s*MAN\s*(\(.*\))?\s*\Z", item):
#         print(item)
characters = dict()

for line in lines:
    line = line.strip()
    if (line.isupper()):

        s1 = re.search('EXT\.', line)
        s2 = re.search('INT\.', line)

        if (not(s1 or s2)):
            print(line)
            re.sub("C","CC",line)
            print(line)
            print("One line")
            if line in characters:
                characters[line] = characters[line] + 1
            else:
                characters[line] = 1

print(characters)