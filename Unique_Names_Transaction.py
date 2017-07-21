import json
from difflib import SequenceMatcher

# IN: List<String> filled with logic -> [i]==name [i+1]==nickname
# OUT: Dict{name<String>:nicknames[]} == {name_1:[nickname1_1,nickname1_2],name_2:[nickname2_1]...nickname_i:[]}
def makeDict(list,maDict):
    for i in range(1,len(list),2):
        if list[i-1] in maDict:
            maDict[list[i-1]].append(list[i])
        else:
            maDict[list[i-1]] = []
            maDict[list[i-1]].append(list[i])

# IN: search_key<String>, text<String>, strictness<Int>
# OUT: TRUE if search_key and text is similar in strictness ratio, else FALSE.
def fuzzy_search(search_key, text, strictness):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        words = line.split()
        for word in words:
            similarity = SequenceMatcher(None, word, search_key)
            if similarity.ratio() > strictness:
                return True
        return False

# IN: Dict{name<String>:nicknames[]} == {name_1:[nickname1_1,nickname1_2],name_2:[nickname2_1]...nickname_i:[]}
# OUT: Dict{nickname<String>:nicknames[]} -> nicknames in list become keys and their value is the list they were in.
def util_dict(my_dict, key, value,result):
    if not(value in result):
        result[value] = []
    for nick in my_dict[key]:
        result[value].append(nick)

# IN: Transaction details ( billNameOnCard splitted ) billFirstName<String>, billLastName<String>, shipFirstName<String>
#                                               , shipLastName<String> , c_first<String>, c_last<String>, card<String>
# OUT: Number<int> of unique names in transaction
def countUniqueNames_Action(billFirstName, billLastName, shipFirstName, shipLastName, c_first, c_last, card):
    b_name = billFirstName + " " + billLastName
    s_name = shipFirstName + " " + shipLastName

    # ~ Stage 1
    # Check if all names are the same
    if fuzzy_search(b_name, card, 0.80) and fuzzy_search(s_name, card, 0.80) and fuzzy_search(b_name, s_name, 0.80):
        return 1

    # ~ Stage 2
    flag = 2
    # Flag is a guide tool for Stage 3, with the flag we can know if (shipFull && billFull) || are similar so Max people
    #                                                                (shipFull && CardFull) || become two
    #                                                                (billFull && CardFull)
    # If last names are similar, check if the first names are likely to belong to the same person.
    # *If last names are not similar its three persons

    # Min 1 - Max 3
    # billLastName && shipLastName
    # Compare last names ( Combination #1 )
    if fuzzy_search(billLastName, shipLastName, 0.70):
        # Compare first names ( Combination #1 )
        if fuzzy_search(billFirstName, shipFirstName, 0.70):
            # Flag = 1 -> indicate that there are Min 1 - Max 2 unique names
            flag = 1
            # Compare last names ( Combination #2 )
            if fuzzy_search(billLastName, c_last, 0.70):
                # Compare first names ( Combination #2 )
                if fuzzy_search(billFirstName, c_first, 0.70):
                    return 1
                else:
                    if billFirstName in dict_nick:
                        for nick in dict_nick[billFirstName]:
                            # Find nick name matched to first name ( Combination #2 )
                            if fuzzy_search(c_first, nick, 0.70):
                                return 1
        else:
            for keys in dict_nick:
                # Find nick name matched to first name ( Combination #1 )
                if fuzzy_search(keys, billFirstName, 0.70):
                    for nick in dict_nick[keys]:
                        # Find nick name matched to first name ( Combination #1 )
                        if fuzzy_search(shipFirstName, nick, 0.70):
                            # Flag = 1 -> indicate that there are Min 1 - Max 2 unique names
                            flag = 1
                            # Compare last names ( Combination #2 )
                            if fuzzy_search(billLastName, c_last, 0.70):
                                # Compare first names ( Combination #2 )
                                if fuzzy_search(billFirstName, c_first, 0.70):
                                    return 1
                                else:
                                    if billFirstName in dict_nick:
                                        for nick_second in dict_nick[nick]:
                                            # Find nick name matched to first name ( Combination #2 )
                                            if fuzzy_search(c_first, nick_second, 0.70):
                                                return 1

    # Min 1 - Max 3
    # billLastName && c_last
    if fuzzy_search(billLastName, c_last, 0.70):
        if fuzzy_search(billFirstName, c_first, 0.70):
            # Min 1 - Max 2
            flag = 1
            if fuzzy_search(billLastName, shipLastName, 0.70):
                if fuzzy_search(billFirstName, shipFirstName, 0.70):
                    return 1
                else:
                    if billFirstName in dict_nick:
                        for nick in dict_nick[billFirstName]:
                            if fuzzy_search(shipFirstName, nick, 0.70):
                                return 1
        else:
            for keys in dict_nick:
                if fuzzy_search(keys, billFirstName, 0.70):
                    for nick in dict_nick[keys]:
                        if fuzzy_search(c_first, nick, 0.70):
                            # Min 1 - Max 2
                            if fuzzy_search(billLastName, shipLastName, 0.70):
                                if fuzzy_search(billFirstName, shipFirstName, 0.70):
                                    return 1
                                else:
                                    if billFirstName in dict_nick:
                                        for nick_second in dict_nick[nick]:
                                            if fuzzy_search(shipFirstName, nick_second, 0.70):
                                                return 1

    # Min 1 - Max 3
    # shipLastName && c_last
    if fuzzy_search(shipLastName, c_last, 0.70):
        if fuzzy_search(shipFirstName, c_first, 0.70):
            # Min 1 - Max 2
            flag = 1
            if fuzzy_search(shipLastName, billLastName, 0.70):
                if fuzzy_search(billFirstName, shipFirstName, 0.70):
                    return 1
                else:
                    if billFirstName in dict_nick:
                        for nick in dict_nick[billFirstName]:
                            if fuzzy_search(shipFirstName, nick, 0.70):
                                return 1
        else:
            for keys in dict_nick:
                if fuzzy_search(keys, shipFirstName, 0.70):
                    for nick in dict_nick[keys]:
                        if fuzzy_search(c_first, nick, 0.70):
                            # Min 1 - Max 2
                            flag = 1
                            if fuzzy_search(billLastName, shipLastName, 0.70):
                                if fuzzy_search(billFirstName, shipFirstName, 0.70):
                                    return 1
                                else:
                                    if billFirstName in dict_nick:
                                        for nick_second in dict_nick[nick]:
                                            if fuzzy_search(shipFirstName, nick_second, 0.70):
                                                return 1

    # ~ Stage 3
    if flag == 1:
        return 2
    else:
        return 3

# IN: billFirstName<String>, billLastName<String>, shipFirstName<String>, shipLastName<String>, billNameOnCard<String>
# OUT: Number of unique people in a transaction.
def countUniqueNames(billFirstName, billLastName, shipFirstName, shipLastName, billNameOnCard):
    # ~ Stage 0
    # Create Fullname strings for Bill && Ship
    b_name = billFirstName + " " + billLastName
    s_name = shipFirstName + " " + shipLastName
    card = ""
    c_first = ""
    c_last = ""
    temp_card = billNameOnCard.split(" ")
    if len(temp_card) != 1:
        # Check typos in billNameOnCard, solves problems like "Jack S Bob"->"Jack Bob"
        #                                                     "JackBob"->"Jack Bob"
        for name in billNameOnCard.split(" "):
            if len(name) >= 2:
                card += name + " "
        c_first = card.split(" ")[0]
        c_last = card.split(" ")[1]
    else:
        temp_num = 0
        index_char = 0
        for char in billNameOnCard:
            if char.isupper():
                temp_num = temp_num + 1
            if temp_num == 2:
                c_first = billNameOnCard[:index_char]
                c_last = billNameOnCard[index_char:]
                break
            index_char = index_char + 1
    r_card = " ".join(card.split(" ")[::-1])
    # ~ Stage 1
    # Check for wrong order of First/Last names
    # There are 8 possible ways
    #   AB  BA  AB  AB  BA  AB  BA  BA
    #   AB  AB  BA  AB  BA  BA  AB  BA
    #   AB  AB  AB  BA  AB  BA  BA  BA
    my_results = []
    # AB AB AB
    my_results.append(
        countUniqueNames_Action(billFirstName, billLastName, shipFirstName, shipLastName, c_first, c_last, card))
    # BA AB AB
    my_results.append(
        countUniqueNames_Action(billLastName, billFirstName, shipFirstName, shipLastName, c_first, c_last, card))
    # AB BA AB
    my_results.append(
        countUniqueNames_Action(billFirstName, billLastName, shipLastName, shipFirstName, c_first, c_last, card))
    # AB AB BA
    my_results.append(
        countUniqueNames_Action(billFirstName, billLastName, shipFirstName, shipLastName, c_last, c_first, r_card))
    # BA BA AB
    my_results.append(
        countUniqueNames_Action(billLastName, billFirstName, shipLastName, shipFirstName, c_first, c_last, card))
    # AB BA BA
    my_results.append(
        countUniqueNames_Action(billFirstName, billLastName, shipLastName, shipFirstName, c_last, c_first, r_card))
    # BA AB BA
    my_results.append(
        countUniqueNames_Action(billLastName, billFirstName, shipFirstName, shipLastName, c_last, c_first, r_card))
    # BA BA BA
    my_results.append(
        countUniqueNames_Action(billLastName, billFirstName, shipLastName, shipFirstName, c_last, c_first, r_card))
    return min(my_results)

#############################################
####### ORGANIZING THE DATA STRUCTURE #######
# Database of nicknames
with open('nicks.json', 'r') as f:
    list_nick = json.load(f)    # List<String> filled with logic -> [i]==name [i+1]==nickname


dict_nick = {}                  # Dict{name<String>:nicknames[]}
makeDict(list_nick,dict_nick)   # make dict_nick[name] -> [nickname_1,nickname_2,nickname_3.....nickname_i]
result = {}                     # temp

# In all keys, the strings in list will become keys in dictionary. Their value is the list they were in.
for key in dict_nick.keys():
    dict_nick[key].append(key)
    for value in dict_nick[key]:
        util_dict(dict_nick,key,value,result)
# store result in dict_nick
dict_nick = result
#############################################

print str(countUniqueNames("Elii","Liz","Elijah","Liz","Liz Eli")) + "$$$  1"
print str(countUniqueNames("Tomer","Eyzenberg","Revital","Eyzenberg","TomerEyzenberg")) + "$$$  2"
print str(countUniqueNames("Tomer","Eyzenberg","Revital","Eyzenberg","TomrEyzenberg")) + "$$$  2"
print str(countUniqueNames("Tomer","Eyzenberg","Revital","Eyzenberg","Tomer Eyzenberggg")) + "$$$  2"
print str(countUniqueNames("Deborah","Egli","Debie","Egli","Debbie Egli")) + "$$$  1"
print str(countUniqueNames("Deborah","Egni","Deborah","Egli","Deborah Egli")) + "$$$  1"
print str(countUniqueNames("Deboah S","Egli","Deborah","Egli","Eglii Deborah")) + "$$$  1"
print str(countUniqueNames("Tomer","Egli","Deborah","Egli","Michele Egli")) + "$$$  3"
print "Examples"
print str(countUniqueNames("Deborah","Egli","Deborah","Egli","Deborah Egli")) + "$$$  1"
print str(countUniqueNames("Deborah","Egli","Debbie","Egli","Debbie Egli")) + "$$$  1"
print str(countUniqueNames("Deborah","Egni","Deborah","Egli","Deborah Egli")) + "$$$  1"
print str(countUniqueNames("Deborah S","Egli","Deborah","Egli","Egli Deborah")) + "$$$  1"
print str(countUniqueNames("Michele","Egli","Deborah","Egli","Michele Egli")) + "$$$  2"

