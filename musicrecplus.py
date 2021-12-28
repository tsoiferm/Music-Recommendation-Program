'''Tyler Soiferman "I pledge my honor that I have abided by the Stevens Honor System"'''

from cs115 import *

preferenceDataFile = 'musicrecplus.txt'        

def loadUsers(fileName):
    '''either loads users from existing file, or creates new file'''
    userMap = {}
    try:
        file = open(fileName, 'r')
        for line in file:
            [userName, bands] = line.strip().split(':')
            bandList = bands.strip().split(',')
            bandList.sort()
            userMap[userName] = bandList
        file.close()
    except FileNotFoundError:
        file = open(fileName, 'w')
    
    return userMap


def getPreferences(userName, userMap):
    '''gets user preferences'''
    newPref = ''
    prefs = []
    newPref = input('Enter an artist that you like (Enter to finish): \n')
    while newPref != '':
        prefs.append(newPref.strip().title())
        newPref = input('Enter an artist that you like (Enter to finish): \n')
    prefs.sort()
    userMap[userName] = prefs 
    return prefs
        
def saveUserPrefs(userName, prefs, userMap, fileName):
    '''saves user preferences'''
    userMap[userName] = prefs
    userList = list(userMap.keys())
    userList.sort()
    file = open(fileName, "w")
    for user in userList:
        toSave = str(user)+':'+','.join(userMap[user])+"\n"
        file.write(toSave)
    file.close()

def getRecommendations(currUser, prefs, userMap):
    '''gets recommendations for the current user'''
    bestUser = findBestUser(currUser, prefs, userMap)
    if bestUser == None:
        print("No recommendations available at this time.")
    else:
        recommendations = drop(prefs, userMap[bestUser])
        return recommendations

def drop(list1, list2):
    '''Return a new list that contains only the elements in list2 that were NOT in list1'''
    list3 = []
    i = 0
    j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            list3.append(list2[j])
            j += 1
    while j < len(list2):
        list3.append(list2[j])
        j += 1
    return list3

def numMatches(list1,list2):
    '''returns the number of elements that match between the two sorted lists'''
    matches = 0
    i = 0
    j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            matches += 1
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            j += 1
    return matches
    

def findBestUser(currUser, prefs, userMap):
    '''finds the user with the most similar tastes to the current user, returns his or her name'''
    bestUser = None
    bestScore = -1
    for user in userMap.keys():
        if '$' not in user:
            score = numMatches(prefs, userMap[user])
            if score > bestScore and currUser != user and len(drop(prefs, userMap[user])) != 0: 
                bestScore = score
                bestUser = user
    return bestUser

def popHelp(userMap):
    '''compiles/returns a dictionary of the artists in userMap and the number of people who prefer him or her'''
    artistDict = {}
    index = 0
    for user in list(userMap):
        if '$' not in user:
            for artist in userMap[user]:
                if artist not in artistDict:
                    score = 0
                    for otherUser in list(userMap)[(index+1):]:
                        if '$' not in otherUser and artist in userMap[otherUser]:
                            score += 1
                    artistDict[artist] = score + 1
        index += 1
    return artistDict

def mostPopularArtist(userMap):
    '''gets the top three most popular artists'''
    if userMap == {}:
        print("Sorry, no artists found.")
    else:
        artistDict = popHelp(userMap)
        first = None
        second = None
        third = None
        firstScore = 0
        secondScore = 0
        thirdScore = 0
        for artist in list(artistDict):
            if artistDict[artist] > firstScore:
                thirdScore = secondScore
                secondScore = firstScore
                firstScore = artistDict[artist]
                third = second
                second = first
                first = artist
            elif artistDict[artist] > secondScore:
                thirdScore = secondScore
                secondScore = artistDict[artist]
                third = second
                second = artist
            elif artistDict[artist] > thirdScore:
                thirdScore = artistDict[artist]
                third = artist
        return [first, second, third]

def howPopular(userMap):
    '''returns how popular the most popular artist is'''
    if len(list(userMap)) == 0:
        print("Sorry, no artists found.")
    else:
        artistDict = popHelp(userMap)
        first = None
        second = None
        third = None
        firstScore = 0
        secondScore = 0
        thirdScore = 0
        for artist in list(artistDict):
            if artistDict[artist] > firstScore:
                thirdScore = secondScore
                secondScore = firstScore
                firstScore = artistDict[artist]
                third = second
                second = first
                first = artist
            elif artistDict[artist] > secondScore:
                thirdScore = secondScore
                secondScore = artistDict[artist]
                third = second
                second = artist
            elif artistDict[artist] > thirdScore:
                thirdScore = artistDict[artist]
                third = artist
        return firstScore
                

def userLikesMost(userMap):
    '''gets the user with the most likes'''
    userArtNum = {}
    for user in list(userMap):
        if '$' not in user:
            score = 0
            for i in userMap[user]:
                score += 1
            userArtNum[user] = score
    first = None
    firstScore = 0
    for user in list(userArtNum):
        if userArtNum[user] > firstScore:
            firstScore = userArtNum[user]
            first = user
    return first
                      
def main():
    '''The main recommendation function'''
    userMap = loadUsers(preferenceDataFile)

    userName = str(input("Enter your name (put a $ symbol after your name if you wish your preferences to remain private): \n"))
    if userName in userMap:
        prefs = userMap[userName]
    else:
        prefs = getPreferences(userName, userMap)
        
        
    print('Enter a letter to chose an option:') 
    print('e - Enter preferences')
    print('r - Get recommendations') 
    print('p - Show most popular artists')
    print('h - How popular is the most popular') 
    print('m - Which user has the most likes') 
    print('q - Save and quit')

    userInp = input('')

    while userInp != 'q':
        if userInp == 'e':
            prefs = getPreferences(userName, userMap)
            userMap[userName] = prefs
        elif userInp == 'r':
            recs = getRecommendations(userName, prefs, userMap)
            if recs != None:
                for artist in recs:
                    print(artist)
        elif userInp == 'p':
            pop = mostPopularArtist(userMap)
            for i in pop:
                print(i)
        elif userInp == 'h':
            print(howPopular(userMap))
        elif userInp == 'm':
            print(userLikesMost(userMap))
        print('Enter a letter to chose an option:') 
        print('e - Enter preferences')
        print('r - Get recommendations') 
        print('p - Show most popular artists')
        print('h - How popular is the most popular') 
        print('m - Which user has the most likes') 
        print('q - Save and quit')

        userInp = input('')

    saveUserPrefs(userName, prefs, userMap, preferenceDataFile)

if __name__ == '__main__': main()
    

    
    
    
    
