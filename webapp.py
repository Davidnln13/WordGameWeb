from flask import Flask,flash, render_template, request, session

app = Flask(__name__)

import random
from datetime import datetime
from operator import itemgetter
#list of all words
words = []
#list of big words
bigWords = []
#list of small words
smallWords = []
wordsOriginal = open('words.txt')

# puts words.txt in list words
with wordsOriginal as inputfile:
    for line in inputfile:
        addWord = line.split()
        words.append(addWord.pop())

# seperates list into two lists of big words and small words
for word in words:
    if len(word) >= 7:
        bigWords.append(word)
    else:
        smallWords.append(word)


# print(randomBigWord)
#start timer

## guitarist = 'unknown'
## why = 'unknown'


@app.route('/Rules')
def get_and_display_Rules():
    return render_template('Rules.html',
                           the_title="Here are the Rules", )


@app.route('/Game', methods=["GET"])
def play_the_game():
     session["mistakes"] = 0
     # output random word from big words
     session["startTime"] = datetime.now()
     session["randomBigWord"] = random.choice(bigWords)
     return render_template('WordGame.html',
                            the_title="Play",
                            the_word=session["randomBigWord"],)


@app.route('/Results', methods=["POST"])
def check_words():
    session["endTime"] = datetime.now()
    session["totalTime"] = (session["endTime"] - session["startTime"]).total_seconds()
    session["totalTime"] = str(round(session["totalTime"], 2))
    session["allValid"] = True
    session["seven_words"] = request.form["seven_words"].split()
    session["seven_words_copy"] = session["seven_words"]
    session["printmessage"] = "";
    checkValidity(session["seven_words"], session["randomBigWord"], session["totalTime"], session["mistakes"])
    if session["allValid"] == True:
        return render_template("ResultsTrue.html",
                                the_title="Here are your results",
                                the_words=session["seven_words"],
                                the_message=session["printmessage"])
    else:
        return render_template("Results.html",
                                the_title="Here are your results",
                                the_words=session["seven_words"],
                                mistakes=session["mistakes"],
                                the_message=session["printmessage"])

@app.route('/Highscore', methods=['POST'])
def  display_highscores():
     session["name"] = request.form['playername']
     session["playerposition"] = ""
     session["length"] = ""
     highscoreOutput = []
     allValidWork(highscoreOutput)
     return render_template('Highscores.html',
                            the_title="Highscores",
                            the_position=session["playerposition"],
                            the_length=session["length"],
                            the_output=highscoreOutput)


def checkValidity(checkWords,randomBigWordIn,totalTimeIn,mistakes):
    randomBigWord = randomBigWordIn
    totalTime = totalTimeIn
    allValid = True
    duplicates = set()
    mistakes = 0
    if len(checkWords) != 7:
        flash("<b>You must provide seven words</b>")
        allValid = False

    for word in checkWords:
        #first validity check is the word at least 3 letters
        # if word == "":
        #     allValid = False
        #     tempWordRemove = checkWords.index(word)
        #     flash("*EMPTY* is not a valid word it is empty")
        #     checkWords[tempWordRemove] = -1 #to symbolise empty
        #     mistakes+=1

        #second validity check is the word at least 3 letters
        if len(word) < 3:
            allValid = False
            tempWordRemove = checkWords.index(word)
            flash(f"<b>{word}</b> is not a valid word it has less than three letters")
            checkWords[tempWordRemove] = -1
            mistakes+=1

        else:
            #third test check if all of the letters are in the word
            #makes sure checking is done in the same case
            letterInWord = list(word.lower())
            bigWordLetters = list(randomBigWord.lower())

            # for every letter in the word check if that letter is in the random word if it is remove it
            letterInWordSuccessful = True
            for letter in letterInWord:
                if letter not in bigWordLetters:
                    letterInWordSuccessful = False
                    allValid = False
                    tempWordRemove = checkWords.index(word)
                    flash(f"<b>{word}</b> is not a valid word it uses characters not in the word")
                    checkWords[tempWordRemove] = -1
                    mistakes+=1
                    break
                else:
                    if(letterInWord.count(letter) > bigWordLetters.count(letter)):
                        letterInWordSuccessful = False
                        allValid = False
                        tempWordRemove = checkWords.index(word)
                        flash(f"<b>{word}</b> is not a valid word it uses a letter more times than it appears in the word")
                        checkWords[tempWordRemove] = -1
                        mistakes+=1
                        break
                    else:
                        letterInWordSuccessful = True


            #fourth test is the word in the dictionary
            if letterInWordSuccessful == True:
                if word not in words:
                    allValid = False
                    tempWordRemove = checkWords.index(word)
                    flash(f"<b>{word}</b> is not a valid word it is not in the dictionary")
                    checkWords[tempWordRemove] = -1
                    mistakes+=1
                else:
                    #fifth test checking for duplicates

                    if word not in duplicates:
                        duplicates.add(word)

                        #sixth check if the word is the same as the source word
                        if word == randomBigWord:
                            allValid = False
                            tempWordRemove = checkWords.index(word)
                            flash(f"<b>{word}</b> is not a valid word it is the same as the source word")
                            checkWords[tempWordRemove] = -1
                            mistakes+=1
                        else:
                            flash(f"<b>{word}</b> is a valid word")

                    else:
                        allValid = False
                        tempWordRemove = checkWords.index(word)
                        flash(f"<b>{word}</b> is not a valid word it is a duplicate")
                        checkWords[tempWordRemove] = -1
                        mistakes+=1

    #print time if all words were valid
    if allValid == True:
         print()
         session["printmessage"] = f"{totalTime} seconds"
    else:
        session["printmessage"] = "Invalid Time"
        print()
        if mistakes > 6:
            mistakes = "7 mistakes you're an idiot"
        elif mistakes > 5:
            mistakes = "6 mistakes get your shit together"
        elif mistakes > 4:
            mistakes = "5 mistakes you bring shame to your family"
        elif mistakes > 3:
            mistakes = "4 mistakes learn to English"
        elif mistakes > 2:
            mistakes = "3 mistakes are you okay?"
        elif mistakes > 1:
            mistakes ="2 mistakes it's not too bad I guess"
        elif mistakes > 0:
            mistakes = "1 mistake meh"
        elif mistakes == 0:
            mistakes = ""

    #restart()
    session["mistakes"] = mistakes
    session["allValid"] = allValid
    #output time if words are valid
def allValidWork(highscoreOutput):

        highscore = open("TopScorersList2","a")
        inputString = session["name"] + "," + session["totalTime"]
        #write our result to the highscore table
        highscore.write(inputString)
        #close and reopen because doesnt work otherwise
        highscore.close()
        manageHighscores()
        highscore = open("TopScorersList2", "r")
        playerPosition = 1
        fullLength = 0
        stopIncrementing = False

        for line in highscore:
            line = line.strip()
            if inputString == line:
                stopIncrementing = True
            if stopIncrementing == False:
                playerPosition +=1
            fullLength+=1
        session["playerposition"] = playerPosition
        session["length"] = fullLength
        highscore.close()
        highscore = open("TopScorersList2","r+")
        #print("HIGHSCORE")
        tenPrints = 0
        for line in highscore:
            if tenPrints < 10:
                line = line.strip()
                lineList = line.split(",")
                key,value = lineList
                print(key,value)
                highscoreOutput.append(key + " "+ value + "\n")

                tenPrints+=1
        highscore.close()
def manageHighscores():
    kList = []
    vList = []
    vStrList = []
    highscore = open("TopScorersList2","r+")

    # for each line in the file strip it and split it
    # change the value to a number for sorting
    # add back to a dictionary and sort them by the value

    for line in highscore:
        line = line.strip()
        lineList = line.split(",")
        key,value = lineList
        value = float(value)
        kList.append(key)
        vList.append(value)
    doubleList = [list(x) for x in zip(*sorted(zip(vList, kList), key=itemgetter(0)))]
    kList = doubleList[1]
    vList = doubleList[0]
    highscore.close()

    # now put them into to seperate lists
    # change the value back to a string
    kList = list(kList)

    for v in vList:
        vStrList.append(str(v))
    #vStrList = list(vStrList)
    #the lists are only 10 wide because we only need to remember 10 highscores
    #del kList[10:]
    #del vStrList[10:]

    finalOutputList = []
    listOutputNum = 0
    tempList = list(vStrList)

    vStrList = []
    for sublist in tempList:
            sublist = str(sublist)
            vStrList.append(sublist)

    open("TopScorersList2", 'w').close()

    highscore = open("TopScorersList2","r+")

    # make a string of first index of the two lists
    #add that string to a final list
    #write that list line by line to the file
    while listOutputNum < len(kList):
        inputStringK = str(kList[listOutputNum])
        inputStringV = str(vStrList[listOutputNum])
        inputString = inputStringK + "," + inputStringV + "\n"
        finalOutputList.append(inputString)
        highscore.write(finalOutputList[listOutputNum])
        listOutputNum+=1
    #does not seem to work without closing and reopening file
    highscore.close()


if __name__ == '__main__':
    app.secret_key = "lfvDLFKgDFKGdfgadfLKhndFjAgdaFAHdfgj:DFAjhhjhjhdfLJ"
    app.run(debug=True)
