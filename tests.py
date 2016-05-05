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

    # d = {"John":1}
    #
    # x = ["John","David","John","James","Silly"]
    # for i in x:
    #     if d.get(i):
    #         d[i] += 1
    #     else:
    #         d[i] = 1
    #
    # print(d)

    string = """
    CC	Coordinating conjunction
2.	CD	Cardinal number
3.	DT	Determiner
4.	EX	Existential there
5.	FW	Foreign word
6.	IN	Preposition or subordinating conjunction
7.	JJ	Adjective
8.	JJR	Adjective, comparative
9.	JJS	Adjective, superlative
10.	LS	List item marker
11.	MD	Modal
12.	NN	Noun, singular or mass
13.	NNS	Noun, plural
14.	NNP	Proper noun, singular
15.	NNPS	Proper noun, plural
16.	PDT	Predeterminer
17.	POS	Possessive ending
18.	PRP	Personal pronoun
19.	PRP$	Possessive pronoun
20.	RB	Adverb
21.	RBR	Adverb, comparative
22.	RBS	Adverb, superlative
23.	RP	Particle
24.	SYM	Symbol
25.	TO	to
26.	UH	Interjection
27.	VB	Verb, base form
28.	VBD	Verb, past tense
29.	VBG	Verb, gerund or present participle
30.	VBN	Verb, past participle
31.	VBP	Verb, non-3rd person singular present
32.	VBZ	Verb, 3rd person singular present
33.	WDT	Wh-determiner
34.	WP	Wh-pronoun
35.	WP$	Possessive wh-pronoun
36.	WRB	Wh-adverb
    """
    string = re.sub("[0-9]?[0-9].","",string)
    string = re.sub("\n","",string)


    string = string.split("\t")
    # print(string)
    cleaned_items = []
    for i in string:
        cleaned_items.append(i.strip())

    i = 0

    dict_list = ""
    while i < len(cleaned_items):
        dict_list += ("{'"+cleaned_items[i]+"':'"+cleaned_items[i+1]+"'}") + ","
        i += 2
    print(dict_list)

