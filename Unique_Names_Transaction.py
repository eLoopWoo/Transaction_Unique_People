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
list_nick = ["Aaron", "Erin", "Aaron", "Ron", "Aaron", "Ronnie", "Abel", "Ab", "Abel", "Abe", "Abel", "Eb", "Abel", "Ebbie",
         "Abiel", "Ab", "Abigail", "Abby", "Abigail", "Gail", "Abigail", "Nabby", "Abner", "Ab", "Abraham", "Ab",
         "Abraham", "Abe", "Abram", "Ab", "Adaline", "Ada", "Adaline", "Addy", "Adaline", "Delia", "Adaline", "Dell",
         "Adaline", "Lena", "Adelaide", "Addy", "Adelaide", "Adele", "Adelaide", "Dell", "Adelaide", "Della",
         "Adelaide", "Heidi", "Adeline", "Ada", "Adeline", "Addy", "Adeline", "Delia", "Adeline", "Dell", "Adeline",
         "Lena", "Adelphia", "Addy", "Adelphia", "Adele", "Adelphia", "Dell", "Adelphia", "Delphia", "Adelphia",
         "Philly", "Agatha", "Aggy", "Agnes", "Aggy", "Agnes", "Inez", "Agnes", "Nessa", "Aileen", "Allie", "Aileen",
         "Lena", "Alan", "Al", "Albert", "Al", "Albert", "Bert", "Alberta", "Allie", "Alberta", "Bert", "Alberta",
         "Bertie", "Aldo", "Al", "Aldrich", "Rich", "Aldrich", "Riche", "Alexander", "Al", "Alexander", "Alex",
         "Alexander", "Sandy", "Alexandra", "Alex", "Alexandra", "Alla", "Alexandra", "Sandra", "Alexandra", "Sandy",
         "Alfonse", "Al", "Alfred", "Al", "Alfred", "Fred", "Alfred", "Freddy", "Alfreda", "Alfy", "Alfreda", "Freda",
         "Alfreda", "Freddy", "Alfreda", "Frieda", "Alice", "Allie", "Alice", "Elsie", "Alice", "Lisa", "Alicia",
         "Allie", "Alicia", "Elsie", "Alicia", "Lisa", "Allan", "Al", "Allen", "Al", "Allisandra", "Allie", "Almena",
         "Allie", "Almena", "Mena", "Alonzo", "Al", "Alonzo", "Lon", "Alonzo", "Lonzo", "Amanda", "Manda", "Amanda",
         "Mandy", "Amelia", "Amy", "Amelia", "Emily", "Amelia", "Mel", "Amelia", "Millie", "Anderson", "Andy", "Andrew",
         "Andy", "Andrew", "Drew", "Ann", "Annie", "Ann", "Nan", "Ann", "Nana", "Ann", "Nancy", "Ann", "Nanny", "Anne",
         "Annie", "Anne", "Nan", "Anne", "Nana", "Anne", "Nancy", "Anne", "Nanny", "Anthony", "Tony", "Antoinette",
         "Ann", "Antoinette", "Netta", "Antoinette", "Tony", "Antonia", "Ann", "Antonia", "Netta", "Antonia", "Tony",
         "Arabella", "Ara", "Arabella", "Arry", "Arabella", "Bella", "Arabella", "Belle", "Arabelle", "Ara", "Arabelle",
         "Arry", "Arabelle", "Bella", "Arabelle", "Belle", "Archibald", "Archie", "Arlene", "Arly", "Arlene", "Lena",
         "Armena", "Arry", "Armena", "Mena", "Arthur", "Art", "Asahel", "Asa", "Asaph", "Asa", "Asenath", "Assene",
         "Asenath", "Natty", "Asenath", "Sene", "August", "Gus", "Augusta", "Aggy", "Augusta", "Gatsy", "Augusta",
         "Gussie", "Augusta", "Tina", "Augustina", "Aggy", "Augustina", "Gatsy", "Augustina", "Gussie", "Augustina",
         "Tina", "Augustine", "August", "Augustine", "Austin", "Augustine", "Gus", "Augustine", "Gus", "Augustus",
         "August", "Augustus", "Austin", "Augustus", "Gus", "Azariah", "Aze", "Azariah", "Riah", "Barbara", "Bab",
         "Barbara", "Babs", "Barbara", "Barby", "Barbara", "Bobbie", "Barnabas", "Barney", "Bartholomew", "Bart",
         "Bartholomew", "Bartel", "Bartholomew", "Bat", "Bartholomew", "Mees", "Bartholomew", "Meus", "Beatrice", "Bea",
         "Beatrice", "Trisha", "Beatrice", "Trix", "Beatrice", "Trixie", "Belinda", "Belle", "Belinda", "Linda",
         "Benedict", "Ben", "Benedict", "Bennie", "Benjamin", "Ben", "Benjamin", "Benjy", "Benjamin", "Bennie",
         "Benjamin", "Jamie", "Bernard", "Barney", "Bernard", "Berney", "Bernard", "Bernie", "Bertha", "Bert", "Bertha",
         "Bertie", "Bertha", "Birdie", "Bill", "Fred", "Billy", "Fred", "Bradford", "Brad", "Bradford", "Ford",
         "Bridget", "Biddie", "Bridget", "Biddy", "Bridget", "Bridgie", "Bridget", "Bridie", "Broderick", "Brady",
         "Broderick", "Brody", "Broderick", "Rick", "Broderick", "Ricky", "Calvin", "Cal", "Calvin", "Vin", "Calvin",
         "Vinny", "Cameron", "Cam", "Cameron", "Ron", "Cameron", "Ronny", "Camille", "Cammie", "Camille", "Millie",
         "Carol", "Carrie", "Carol", "Cassie", "Carol", "Lynn", "CarolAnn", "Carol", "CarolAnn", "Carole", "Caroline",
         "Carol", "Caroline", "Carole", "Caroline", "Carrie", "Caroline", "Cassie", "Caroline", "Lynn", "Carolyn",
         "Carrie", "Carolyn", "Cassie", "Carolyn", "Lynn", "Casey", "K.C.", "Cassandra", "Cassie", "Cassandra",
         "Sandra", "Cassandra", "Sandy", "Catherine", "Cassie", "Catherine", "Cathy", "Catherine", "Kathy", "Catherine",
         "Katy", "Catherine", "Kay", "Catherine", "Kit", "Catherine", "Kittie", "Catherine", "Lena", "Catherine",
         "Trina", "Cathleen", "Cassie", "Cathleen", "Cathy", "Cathleen", "Kathy", "Cathleen", "Katy", "Cathleen", "Kay",
         "Cathleen", "Kit", "Cathleen", "Kittie", "Cathleen", "Lena", "Cathleen", "Trina", "Cecilia", "Celia",
         "Cecilia", "Cissy", "Cedric", "Ced", "Cedric", "Rick", "Cedric", "Ricky", "Charles", "Carl", "Charles",
         "Charlie", "Charles", "Chick", "Charles", "Chuck", "Charles", "Chuck", "Charlotte", "Char", "Charlotte",
         "Lotta", "Charlotte", "Lottie", "Charlotte", "Sherry", "Chauncey", "Chan", "Chester", "Chet", "Christa",
         "Chris", "Christian", "Chris", "Christian", "Chris", "Christian", "Kit", "Christiana", "Ann", "Christiana",
         "Chris", "Christiana", "Christy", "Christiana", "Crissy", "Christiana", "Kris", "Christiana", "Kristy",
         "Christiana", "Tina", "Christina", "Chris", "Christina", "Christy", "Christina", "Crissy", "Christina", "Kris",
         "Christina", "Kristy", "Christina", "Tina", "Christina", "Tina", "Christine", "Chris", "Christine", "Chrissy",
         "Christine", "Crissy", "Christine", "Kris", "Christine", "Kristy", "Christine", "Tina", "Christopher", "Chris",
         "Christopher", "Kit", "Clarence", "Clair", "Clarence", "Clare", "Clarinda", "Clara", "Clarissa", "Cissy",
         "Clarissa", "Clara", "Clement", "Clem", "Clement", "Clem", "Clifford", "Cliff", "Clifford", "Ford", "Clifton",
         "Cliff", "Clifton", "Tony", "Columbus", "Clum", "Conrad", "Con", "Conrad", "Conny", "Constance", "Connie",
         "Cordelia", "Cordy", "Cordelia", "Delia", "Cornelia", "Cornie", "Cornelia", "Corny", "Cornelia", "Nelia",
         "Cornelia", "Nelle", "Cornelia", "Nelly", "Cornelius", "Con", "Cornelius", "Conny", "Cornelius", "Corny",
         "Cornelius", "Niel", "Courtney", "Court", "Courtney", "Curt", "Curtis", "Curt", "Cynthia", "Cindy", "Cynthia",
         "Cindy", "Cynthia", "Cintha", "Cyrenius", "Cene", "Cyrenius", "Cy", "Cyrenius", "Renius", "Cyrenius", "Serene",
         "Cyrenius", "Swene", "Dal", "Dahl", "Dalton", "Dahl", "Daniel", "Dan", "Daniel", "Danny", "Darlene", "Darry",
         "Darlene", "Lena", "David", "Dave", "David", "Davey", "David", "Day", "Debora", "Deb", "Debora", "Debbie",
         "Debora", "Debby", "Deborah", "Deb", "Deborah", "Debbie", "Deborah", "Debby", "Debra", "Deb", "Debra",
         "Debbie", "Delbert", "Bert", "Delbert", "Del", "Deliverance", "Della", "Deliverance", "Delly", "Deliverance",
         "Dilly", "Delores", "Dee", "Delores", "Dell", "Delores", "Della", "Delores", "Lola", "Delores", "Lolly",
         "Dennis", "Denny", "Dennison", "Denny", "Derrick", "Eric", "Derrick", "Rick", "Derrick", "Rick", "Derrick",
         "Ricky", "Dicey", "Dicie", "Domenic", "Dom", "Dominic", "Dom", "Donald", "Don", "Donald", "Donnie", "Donald",
         "Donny", "Donald", "Dony", "Dorcus", "Darkey", "Dorothy", "Dolly", "Dorothy", "Dortha", "Dorothy", "Dot",
         "Dorothy", "Dotty", "Ebenezer", "Eb", "Ebenezer", "Ebbie", "Ebenezer", "Eben", "Edgar", "Ed", "Edgar", "Eddie",
         "Edgar", "Eddy", "Edith", "Edie", "Edith", "Edie", "Edith", "Edye", "Edmond", "Ed", "Edmond", "Eddie",
         "Edmond", "Eddy", "Edmund", "Ed", "Edmund", "Ed", "Edmund", "Eddie", "Edmund", "Eddy", "Edmund", "Ned",
         "Edmund", "Ted", "Eduardo", "Ed", "Eduardo", "Eddie", "Eduardo", "Eddy", "Edward", "Ed", "Edward", "Eddie",
         "Edward", "Eddy", "Edward", "Ned", "Edward", "Ted", "Edward", "Teddy", "Edwin", "Ed", "Edwin", "Eddie",
         "Edwin", "Eddy", "Edwin", "Ned", "Edwin", "Win", "Edyth", "Edie", "Edyth", "Edye", "Edythe", "Edie", "Edythe",
         "Edye", "Elbert", "Albert", "Eleanor", "Elaine", "Eleanor", "Ellen", "Eleanor", "Ellen", "Eleanor", "Ellie",
         "Eleanor", "Lanna", "Eleanor", "Lenora", "Eleanor", "Nelly", "Eleanor", "Nora", "Eleazer", "Lazar", "Elias",
         "Eli", "Elias", "Lee", "Elias", "Lias", "Elijah", "Eli", "Elijah", "Lige", "Eliphalet", "Left", "Elisha",
         "Eli", "Elisha", "Lish", "Elizabeth", "Bess", "Elizabeth", "Bessie", "Elizabeth", "Beth", "Elizabeth", "Betsy",
         "Elizabeth", "Betty", "Elizabeth", "Eliza", "Elizabeth", "Lib", "Elizabeth", "Libby", "Elizabeth", "Lisa",
         "Elizabeth", "Liz", "Elizabeth", "Liza", "Elizabeth", "Lizzie", "Ellswood", "Elsey", "Elmira", "Ellie",
         "Elmira", "Elly", "Elmira", "Mira", "Elouise", "Louise", "Elsie", "Elsey", "Elswood", "Elsey", "Elwood",
         "Woody", "Elze", "Elsey", "Emanuel", "Manny", "Emanuel", "Manuel", "Emeline", "Em", "Emeline", "Emily",
         "Emeline", "Emma", "Emeline", "Emmy", "Emeline", "Milly", "Emily", "Emma", "Emily", "Emmy", "Emily", "Millie",
         "Epaphroditius", "Dite", "Epaphroditius", "Ditus", "Epaphroditius", "Dyce", "Epaphroditius", "Dyche",
         "Epaphroditius", "Eppa", "Ephraim", "Eph", "Eric", "Rick", "Eric", "Ricky", "Ernest", "Ernie", "Estella",
         "Essy", "Estella", "Stella", "Estelle", "Essy", "Estelle", "Stella", "Eugene", "Gene", "Evaline", "Eva",
         "Evaline", "Eve", "Evaline", "Lena", "Ezekiel", "Ez", "Ezekiel", "Zeke", "Ezra", "Ez", "Faith", "Fay",
         "Feltie", "Felty", "Ferdinand", "Ferdie", "Ferdinand", "Fred", "Ferdinand", "Freddie", "Ferdinand", "Freddy",
         "Fidelia", "Delia", "Florence", "Flo", "Florence", "Flora", "Florence", "Flossy", "Frances", "Cissy",
         "Frances", "Fanny", "Frances", "Fran", "Frances", "Francie", "Frances", "Frankie", "Frances", "Frannie",
         "Frances", "Franniey", "Frances", "Sis", "Francine", "Fran", "Francine", "Francie", "Francine", "Frannie",
         "Francine", "Franniey", "Francis", "Fran", "Francis", "Fran", "Francis", "Frank", "Francis", "Frankie",
         "Franklin", "Fran", "Franklin", "Frank", "Franklind", "Frank", "Frederick", "Fred", "Frederick", "Fred",
         "Frederick", "Freddie", "Frederick", "Freddy", "Frederick", "Freddy", "Frederick", "Fritz", "Fredericka",
         "Freda", "Fredericka", "Freddy", "Fredericka", "Frieda", "Fredericka", "Ricka", "Frieda", "Fred", "Frieda",
         "Freddie", "Frieda", "Freddy", "Gabriel", "Gabby", "Gabriel", "Gabe", "Gabriella", "Ella", "Gabriella",
         "Gabby", "Gabrielle", "Ella", "Gabrielle", "Gabby", "Genevieve", "Eve", "Genevieve", "Jean", "Genevieve",
         "Jenny", "Geoffrey", "Geoff", "Geoffrey", "Jeff", "Gerald", "Gerry", "Gerald", "Jerry", "Geraldine", "Dina",
         "Geraldine", "Gerrie", "Geraldine", "Gerry", "Geraldine", "Jerry", "Gertrude", "Gert", "Gertrude", "Gertie",
         "Gertrude", "Trudy", "Gilbert", "Bert", "Gilbert", "Bert", "Gilbert", "Gil", "Gilbert", "Wilber", "Gwendolyn",
         "Gwen", "Gwendolyn", "Wendy", "Hannah", "Anna", "Hannah", "Nan", "Hannah", "Nanny", "Harold", "Hal", "Harold",
         "Harry", "Harriet", "Hattie", "Helen", "Ella", "Helen", "Ellen", "Helen", "Ellie", "Helen", "Lena", "Helene",
         "Ella", "Helene", "Ellen", "Helene", "Ellie", "Helene", "Lena", "Heloise", "Eloise", "Heloise", "Elouise",
         "Heloise", "Lois", "Henrietta", "Etta", "Henrietta", "Etty", "Henrietta", "Hank", "Henrietta", "Nettie",
         "Henrietta", "Retta", "Henry", "Hal", "Henry", "Hank", "Henry", "Harry", "Hephsibah", "Hipsie", "Hepsibah",
         "Hipsie", "Herbert", "Bert", "Herbert", "Herb", "Hermione", "Hermie", "Hester", "Esther", "Hester", "Hessy",
         "Hester", "Hetty", "Hezekiah", "Hez", "Hezekiah", "Hy", "Hezekiah", "Kiah", "Hiram", "Hy", "Hopkins", "Hop",
         "Hopkins", "Hopp", "Horace", "Horry", "Hubert", "Bert", "Hubert", "Bert", "Hubert", "Hub", "Hubert", "Hugh",
         "Ignatius", "Iggy", "Ignatius", "Nace", "Ignatius", "Nate", "Ignatius", "Natius", "Irene", "Rena", "Irving",
         "Irv", "Isaac", "Ike", "Isaac", "Zeke", "Isabel", "Bell", "Isabel", "Bella", "Isabel", "Belle", "Isabel", "Ib",
         "Isabel", "Issy", "Isabel", "Nib", "Isabel", "Nibby", "Isabel", "Tibbie", "Isabella", "Bella", "Isabella",
         "Belle", "Isabella", "Ib", "Isabella", "Issy", "Isabella", "Nib", "Isabella", "Nibby", "Isabella", "Tibbie",
         "Isabelle", "Bella", "Isabelle", "Belle", "Isabelle", "Ib", "Isabelle", "Issy", "Isabelle", "Nib", "Isabelle",
         "Nibby", "Isabelle", "Tibbie", "Isadora", "Dora", "Isadora", "Issy", "Isidore", "Izzy", "Jacob", "Jaap",
         "Jacob", "Jake", "Jacob", "Jay", "Jacob", "Jay", "Jacobus", "Jacob", "James", "Jamie", "James", "Jem", "James",
         "Jim", "James", "Jimmie", "James", "Jimmy", "Jane", "Janie", "Jane", "Jean", "Jane", "Jennie", "Jane",
         "Jessie", "Janet", "Jan", "Janet", "Jan", "Janet", "Jessie", "Janice", "Jan", "Jean", "Jane", "Jean",
         "Jeannie", "Jeanette", "Janet", "Jeanette", "Jean", "Jeanette", "Jessie", "Jeanette", "Nettie", "Jeanne",
         "Jane", "Jeanne", "Jeannie", "Jedidiah", "Jed", "Jefferson", "Jeff", "Jefferson", "Sonny", "Jeffrey", "Geoff",
         "Jeffrey", "Jeff", "Jeffrey", "Jeff", "Jehiel", "Hiel", "Jemima", "Mima", "Jennifer", "Jennie", "Jeremiah",
         "Jereme", "Jeremiah", "Jerry", "Jessica", "Jessie", "Joan", "Jo", "Joan", "Nonie", "Joann", "Jo", "Joanna",
         "Hannah", "Joanna", "Jo", "Joanna", "Joan", "Joanna", "Jody", "Joanne", "Jo", "Johanna", "Jo", "Johannah",
         "Hannah", "Johannah", "Joan", "Johannah", "Jody", "Johannah", "Nonie", "John", "Jack", "John", "Jock", "John",
         "Johnny", "Jon", "John", "Jon", "Nathan", "Jonathan", "John", "Jonathan", "Nathan", "Joseph", "Jody", "Joseph",
         "Joe", "Joseph", "Joey", "Joseph", "Jos", "Josephine", "Fina", "Josephine", "Jo", "Josephine", "Jody",
         "Josephine", "Joey", "Josephine", "Josey", "Joshua", "Jos", "Joshua", "Josh", "Josiah", "Jos", "Joyce", "Joy",
         "Juanita", "Nettie", "Juanita", "Nita", "Judson", "Jud", "Judson", "Sonny", "Julia", "Jill", "Julia", "Julie",
         "Julian", "Jule", "Julias", "Jule", "Junior", "JR", "Junior", "June", "Junior", "Junie", "Kasey", "K.C.",
         "Katelin", "Kate", "Katelin", "Kay", "Katelin", "Kaye", "Katelyn", "Kate", "Katelyn", "Kay", "Katelyn", "Kaye",
         "Katherine", "Cassie", "Katherine", "Cathy", "Katherine", "Kate", "Katherine", "Kathy", "Katherine", "Katy",
         "Katherine", "Kay", "Katherine", "Kaye", "Katherine", "Kit", "Katherine", "Kittie", "Katherine", "Lena",
         "Katherine", "Trina", "Kathleen", "Cassie", "Kathleen", "Cathy", "Kathleen", "Kathy", "Kathleen", "Kathy",
         "Kathleen", "Katy", "Kathleen", "Kay", "Kathleen", "Kit", "Kathleen", "Kittie", "Kathleen", "Lena", "Kathleen",
         "Trina", "Kathryn", "Kathy", "Kendall", "Ken", "Kendall", "Kenny", "Kenneth", "Ken", "Kenneth", "Kendrick",
         "Kenneth", "Kenny", "Kent", "Ken", "Kent", "Kendrick", "Kent", "Kenny", "Keziah", "Kizza", "Keziah", "Kizzie",
         "Kimberley", "Kim", "Kimberly", "Kim", "Kingsley", "King", "Kingston", "King", "Kristen", "Chris", "Kristin",
         "Chris", "Kristine", "Chris", "Kristine", "Christy", "Kristine", "Crissy", "Kristine", "Kris", "Kristine",
         "Kristy", "Kristine", "Tina", "Kristy", "Chris", "Lafayette", "Fate", "Lafayette", "Laffie", "Lamont", "Monty",
         "Laurence", "Larry", "Laurence", "Lon", "Laurence", "Lonny", "Laurence", "Lorne", "Laurence", "Lorry",
         "Lavina", "Ina", "Lavina", "Vina", "Lavina", "Viney", "Lavinia", "Ina", "Lavinia", "Vina", "Lavinia", "Viney",
         "Lawrence", "Larry", "Lawrence", "Lon", "Lawrence", "Lonny", "Lawrence", "Lorne", "Lawrence", "Lorry",
         "Lemuel", "Lem", "Lenora", "Lee", "Lenora", "Nora", "Leonard", "Len", "Leonard", "Lenny", "Leonard", "Leo",
         "Leonard", "Leon", "Leonard", "Lineau", "LeRoy", "L.R.", "LeRoy", "Lee", "LeRoy", "Roy", "Leslie", "Les",
         "Lester", "Les", "Letitia", "Lettice", "Letitia", "Lettie", "Letitia", "Tish", "Letitia", "Titia", "Levi",
         "Lee", "Lidia", "Lyddy", "Lillah", "Lil", "Lillah", "Lilly", "Lillah", "Lily", "Lillah", "Lolly", "Lillian",
         "Lil", "Lillian", "Lilly", "Lillian", "Lolly", "Lincoln", "Link", "Linda", "Lindy", "Linda", "Lynn", "Lisa",
         "Alice", "Lisa", "Melissa", "Lois", "Louise", "Lorenzo", "Loren", "Loretta", "Etta", "Loretta", "Lorrie",
         "Loretta", "Retta", "Lorraine", "Lorrie", "Louisa", "Eliza", "Louisa", "Lois", "Louisa", "Lou", "Louise",
         "Eliza", "Louise", "Lois", "Louise", "Lou", "Lucas", "Luke", "Lucias", "Luke", "Lucille", "Cille", "Lucille",
         "Lou", "Lucille", "Lu", "Lucille", "Lucy", "Lucinda", "Cindy", "Lucinda", "Lou", "Lucinda", "Lu", "Lucinda",
         "Lucy", "Luella", "Ella", "Luella", "Lu", "Luella", "Lula", "Luther", "Luke", "Lydia", "Lyddy", "Lyndon",
         "Lindy", "Lyndon", "Lynn", "Madeline", "Lena", "Madeline", "Maddy", "Madeline", "Madge", "Madeline", "Magda",
         "Madeline", "Maggie", "Magdelina", "Lena", "Magdelina", "Madge", "Magdelina", "Magda", "Mahala", "Hallie",
         "Marcus", "Mark", "Margaret", "Daisy", "Margaret", "Gretta", "Margaret", "Madge", "Margaret", "Maggie",
         "Margaret", "Maggy", "Margaret", "Marge", "Margaret", "Margery", "Margaret", "Margie", "Margaret", "Margie",
         "Margaret", "Margy", "Margaret", "Meg", "Margaret", "Midge", "Margaret", "Peg", "Margaret", "Peggy",
         "Margaret", "Peggy", "Margaret", "Rita", "Margaretta", "Daisy", "Margaretta", "Gretta", "Margaretta", "Madge",
         "Margaretta", "Maggie", "Margaretta", "Marge", "Margaretta", "Margery", "Margaretta", "Margie", "Margaretta",
         "Meg", "Margaretta", "Midge", "Margaretta", "Peg", "Margaretta", "Peggy", "Margaretta", "Rita", "Marjorie",
         "Margie", "Marjorie", "Margy", "Martha", "Marty", "Martha", "Mat", "Martha", "Mattie", "Martha", "Patsy",
         "Martha", "Patty", "Martin", "Marty", "Martina", "Tina", "Marvin", "Marv", "Mary", "Mae", "Mary", "Mamie",
         "Mary", "Mitzi", "Mary", "Molly", "Mary", "Polly", "Matilda", "Matty", "Matilda", "Maud", "Matilda", "Tilly",
         "Matthew", "Matt", "Matthew", "Mattie", "Matthew", "Matty", "Matthew", "Thias", "Matthew", "Thys", "Matthias",
         "Matt", "Matthias", "Thias", "Matthias", "Thys", "Maurice", "Morey", "Mehitabel", "Hetty", "Mehitabel",
         "Hitty", "Mehitabel", "Mabel", "Mehitabel", "Mitty", "Melinda", "Linda", "Melinda", "Lindy", "Melinda",
         "Lindy", "Melinda", "Lynn", "Melinda", "Mel", "Melinda", "Mindy", "Melissa", "Lisa", "Melissa", "Lissa",
         "Melissa", "Mel", "Melissa", "Milly", "Melissa", "Missy", "Mervyn", "Merv", "Michael", "Micah", "Michael",
         "Mick", "Michael", "Micky", "Michael", "Mike", "Michelle", "Mickey", "Mildred", "Milly", "Millicent", "Milly",
         "Millicent", "Missy", "Minerva", "Minnie", "Miranda", "Mandy", "Miranda", "Mira", "Miranda", "Randy", "Miriam",
         "Mimi", "Miriam", "Mitzi", "Mitchell", "Mitch", "Montgomery", "Gum", "Montgomery", "Monty", "Morris", "Morey",
         "Nancy", "Ann", "Nancy", "Nan", "Nancy", "Nan", "Napoleon", "Leon", "Napoleon", "Nap", "Napoleon", "Nappy",
         "Natalie", "Natty", "Natalie", "Nettie", "Nathan", "Nat", "Nathan", "Nate", "Nathaniel", "Nat", "Nathaniel",
         "Nate", "Nathaniel", "Nathan", "Nathaniel", "Natty", "Nathaniel", "Than", "Nicholas", "Claas", "Nicholas",
         "Claes", "Nicholas", "Nick", "Norbert", "Bert", "Norbert", "Norby", "Obadiah", "Diah", "Obadiah", "Dyer",
         "Obadiah", "Obed", "Obadiah", "Obie", "Olive", "Livia", "Olive", "Nollie", "Olive", "Ollie", "Oliver", "Ollie",
         "Olivia", "Livia", "Olivia", "Nollie", "Olivia", "Ollie", "Oswald", "Ossy", "Oswald", "Ozzy", "Oswald",
         "Waldo", "Pamela", "Pam", "Parmelia", "Amelia", "Parmelia", "Melia", "Parmelia", "Milly", "Patience", "Pat",
         "Patience", "Patty", "Patricia", "Pat", "Patricia", "Patsy", "Patricia", "Patty", "Patricia", "Tricia",
         "Patrick", "Paddy", "Patrick", "Pat", "Patrick", "Pate", "Patrick", "Patsy", "Patrick", "Peter", "Paula",
         "Lina", "Paula", "Polly", "Paulina", "Lina", "Paulina", "Polly", "Pelegrine", "Perry", "Penelope", "Penny",
         "Percival", "Percy", "Peter", "Pate", "Peter", "Pete", "Peter", "Pete", "Peter", "Pete", "Philetus", "Leet",
         "Philetus", "Phil", "Philinda", "Linda", "Philinda", "Lindy", "Philinda", "Lynn", "Philip", "Phil", "Phillip",
         "Phil", "Phillip", "Phil", "Prescott", "Pres", "Prescott", "Scott", "Prescott", "Scotty", "Priscilla", "Cilla",
         "Priscilla", "Cissy", "Priscilla", "Prissy", "Prudence", "Prudy", "Prudence", "Prue", "Rachel", "Shelly",
         "Rafaela", "Rafa", "Randolph", "Dolph", "Randolph", "Randy", "Raphael", "Ralph", "Raymond", "Ray", "Raymond",
         "Ray", "Raymond", "Ray", "Rebecca", "Becca", "Rebecca", "Beck", "Rebecca", "Becky", "Rebecca", "Reba",
         "Regina", "Gina", "Regina", "Reggie", "Reginald", "Naldo", "Reginald", "Reg", "Reginald", "Reggie", "Reginald",
         "Renny", "Relief", "Leafa", "Reuben", "Rube", "Ricardo", "Rick", "Ricardo", "Ricky", "Richard", "Dick",
         "Richard", "Dickie", "Richard", "Dickon", "Richard", "Dicky", "Richard", "Rich", "Richard", "Rick", "Richard",
         "Rick", "Richard", "Rick", "Richard", "Ricky", "Richard", "Ricky", "Robert", "Bob", "Robert", "Bobby",
         "Robert", "Dob", "Robert", "Dobbin", "Robert", "Hob", "Robert", "Hobkin", "Robert", "Rob", "Robert", "Rob",
         "Roberta", "Bert", "Roberta", "Bertie", "Roberta", "Birdie", "Roberta", "Bobbie", "Roberta", "Bobbie",
         "Roberta", "Robbie", "Rodger", "Bobby", "Rodger", "Hodge", "Rodger", "Robby", "Rodger", "Robin", "Rodger",
         "Rod", "Rodger", "Roge", "Rodger", "Rupert", "Roger", "Bobby", "Roger", "Hodge", "Roger", "Robby", "Roger",
         "Robin", "Roger", "Rod", "Roger", "Roge", "Roger", "Rupert", "Roland", "Lanny", "Roland", "Orlando", "Roland",
         "Rollo", "Roland", "Rolly", "Ronald", "Naldo", "Ronald", "Ron", "Ronald", "Ron", "Ronald", "Ron", "Ronald",
         "Ronny", "Ronald", "Ronny", "Ronald", "Ronny", "Rosabel", "Belle", "Rosabel", "Rosa", "Rosabel", "Rose",
         "Rosabel", "Roz", "Rosabella", "Belle", "Rosabella", "Rosa", "Rosabella", "Rose", "Rosabella", "Roz",
         "Rosalinda", "Linda", "Rosalinda", "Rosa", "Rosalinda", "Rose", "Rosalinda", "Roz", "Rosalyn", "Linda",
         "Rosalyn", "Rosa", "Rosalyn", "Rose", "Rosalyn", "Roz", "Roseann", "Ann", "Roseann", "Rose", "Roseann",
         "Rosie", "Roseann", "Roz", "Roseanna", "Ann", "Roseanna", "Rose", "Roseanna", "Rosie", "Roseanna", "Roz",
         "Roseanne", "Ann", "Roxanna", "Ann", "Roxanna", "Rose", "Roxanna", "Roxie", "Roxanne", "Ann", "Roxanne",
         "Rose", "Roxanne", "Roxie", "Rudolph", "Dolph", "Rudolph", "Olph", "Rudolph", "Rolf", "Rudolph", "Rudy",
         "Rudolphus", "Dolph", "Rudolphus", "Olph", "Rudolphus", "Rolf", "Rudolphus", "Rudy", "Russell", "Russ",
         "Russell", "Russ", "Russell", "Rusty", "Sabrina", "Brina", "Samuel", "Sam", "Samuel", "Sam", "Samuel", "Sammy",
         "Samuel", "Sammy", "Sandra", "Cassandra", "Sandra", "Sandy", "Sarah", "Sadie", "Sarah", "Sally", "Serena",
         "Rena", "Seymour", "Morey", "Seymour", "See", "Shelton", "Shel", "Shelton", "Shelly", "Shelton", "Tony",
         "Sheridan", "Dan", "Sheridan", "Danny", "Sheridan", "Sher", "Shirley", "Lee", "Shirley", "Sherry", "Shirley",
         "Shirl", "Sidney", "Sid", "Sidney", "Syd", "Silas", "Si", "Simeon", "Si", "Simeon", "Sion", "Simon", "Si",
         "Simon", "Sion", "Smith", "Smitty", "Solomon", "Sal", "Solomon", "Salmon", "Solomon", "Saul", "Solomon", "Sol",
         "Solomon", "Solly", "Solomon", "Zolly", "Sophia", "Sophie", "Stephan", "Steve", "Stephen", "Steph", "Stephen",
         "Steve", "Steven", "Steph", "Steven", "Steve", "Stuart", "Stu", "Submit", "Mitty", "Sullivan", "Sully",
         "Sullivan", "Van", "Susan", "Hannah", "Susan", "Sue", "Susan", "Sukey", "Susan", "Susie", "Susan", "Suzie",
         "Susannah", "Hannah", "Susannah", "Sue", "Susannah", "Sukey", "Susannah", "Susie", "Sylvester", "Si",
         "Sylvester", "Sly", "Sylvester", "Sy", "Sylvester", "Syl", "Sylvester", "Vessie", "Sylvester", "Vester",
         "Sylvester", "Vet", "Tabitha", "Tabby", "Terence", "Terry", "Teresa", "Terry", "Thaddeus", "Thad", "Theodore",
         "Ted", "Theodore", "Ted", "Theodore", "Teddy", "Theodore", "Teddy", "Theodore", "Theo", "Theresa", "Terry",
         "Theresa", "Tess", "Theresa", "Tessa", "Theresa", "Tessie", "Theresa", "Thirza", "Theresa", "Thursa",
         "Theresa", "Tracy", "Thom", "Tom", "Thom", "Tommy", "Thomas", "Thom", "Thomas", "Thom", "Thomas", "Tom",
         "Thomas", "Tom", "Thomas", "Tom", "Thomas", "Tommy", "Thomas", "Tommy", "Thomas", "Tommy", "Timothy", "Tim",
         "Timothy", "Tim", "Timothy", "Tim", "Timothy", "Timmy", "Timothy", "Timmy", "Timothy", "Timmy", "Tobias",
         "Bias", "Tobias", "Toby", "Tryphena", "Phena", "Uriah", "Riah", "Valentine", "Felty", "Valeri", "Val",
         "Valerie", "Val", "Valerie", "Val", "Valerie", "Val", "Vanessa", "Essa", "Vanessa", "Nessa", "Vanessa",
         "Vanna", "Veronica", "Franky", "Veronica", "Frony", "Veronica", "Ron", "Veronica", "Ronie", "Veronica",
         "Ronna", "Veronica", "Ronnie", "Veronica", "Ronnie", "Veronica", "Vonnie", "Victor", "Vic", "Victoria",
         "Torie", "Victoria", "Tory", "Victoria", "Vic", "Victoria", "Vicki", "Victoria", "Vicky", "Vincent", "Vic",
         "Vincent", "Vin", "Vincent", "Vince", "Vincent", "Vinnie", "Vincent", "Vinny", "Vincenzo", "Vic", "Vincenzo",
         "Vin", "Vincenzo", "Vinnie", "Vincenzo", "Vinny", "Vinson", "Vinny", "Virginia", "Ginger", "Virginia", "Ginny",
         "Virginia", "Jane", "Virginia", "Jennie", "Virginia", "Virgy", "Wallace", "Wally", "Walter", "Wally", "Walter",
         "Walt", "Washington", "Wash", "Wilber", "Bert", "Wilber", "Will", "Wilbur", "Willie", "Wilbur", "Willy",
         "Wilfred", "Fred", "Wilfred", "Will", "Wilfred", "Willie", "Wilhelmina", "Mina", "Wilhelmina", "Minnie",
         "Wilhelmina", "Willie", "Wilhelmina", "Wilma", "Will", "Fred", "William", "Bela", "William", "Bell", "William",
         "Bill", "William", "Billy", "William", "Will", "William", "Willie", "William", "Willy", "Willie", "Fred",
         "Wilson", "Will", "Wilson", "Willie", "Wilson", "Willy", "Winfield", "Field", "Winfield", "Win", "Winfield",
         "Winny", "Winifred", "Freddie", "Winifred", "Winnet", "Winifred"]               # List<String> filled with logic -> [i]==name [i+1]==nickname

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
