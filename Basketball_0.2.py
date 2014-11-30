#David Ramanauskas, Nathan King
#IT262
#11/9/2014
#Preliminary prototype of basketball scoring system.

import os

#Main menu function.
def menu(gameObj):
    
    # Clear screen
    os.system('cls') # Windows
    #os.system('clear') # Linux
    
    #Displays main menu
    print('\n----Welcome to IT262 Basketball Scoring System-----\n')

    print('\t1. Insert score\n')
    print('\t2. View team data\n')
    print('\t3. Next quarter (cur: '+str(gameObj.getQuarter())+')\n')
    print('\t4. Exit\n')

    x = int(input('Please select an option: '))

    #Input validation loop
    while ((x > 4) | (x < 1)):
        x = int(input('Please enter a valid choice: '))
    
    #Menu descision structure
    if x == 1:
        gameObj.score()
    elif x == 2:
        gameObj.viewScore()
    elif x == 3:
        return gameObj.nextQuarter();
    elif x == 4:
        print('Exiting...')
        exit()
    
    return True

class Game:
    
    # Setup the game
    def __init__(self, homeTeam, awayTeam):
        self.__currentQuarter = 1
        self.__players = {} # Dictionary to hold players. Using dict
                            # here so that custom player numbers may
                            # later be added (currently 1,2,...,12)
        
        self.__homeTeam = Team(homeTeam, 1);
        self.__awayTeam = Team(awayTeam, 2);
        
        # Setup home team
        for i in range(1,12):
            self.__players[i] = Player(i, self.__homeTeam.getId())
        
        # Setup away team
        for i in range(13,24):
            self.__players[i] = Player(i, self.__awayTeam.getId())
        
    
    # Increment the quarter
    def nextQuarter(self):
        self.__currentQuarter += 1
        if(self.__currentQuarter > 4):
            self.endGame();
            return False
        
        return True
    
    def getQuarter(self):
        return self.__currentQuarter

    # Logic for incrementing team scores
    def score(self):
        repeat = True

        while(repeat):

            os.system('cls')
            #os.system('clear')

            #Displays menu and accepts user score and team who scored. 
            print('\n-----Scoring-----\n')

            score = int(input('Enter score: '))

            while ((score > 3) | (score < 1)): #Input validation for score
                score = int(input("Please enter a valid score: "))

            team = int(input('\nWhich team scored? Bulls(1) or Lakers(2): '))

            while ((team > 2) | (team < 1)): #Input validation for team
               team = int(input('\nPlease enter a valid team. Bulls(1) or Lakers(2): '))
            
            # Ask for which player scored, and list players
            if(team == 1):
                teamPlayers = self.__homeTeam.getPlayers(self.__players)
            else:
                teamPlayers = self.__awayTeam.getPlayers(self.__players)
            
            playersString = "";
            playersList = [];
            for i in teamPlayers:
                playersString += " " + str(teamPlayers[i].getPlayerId())
                playersList.append(teamPlayers[i].getPlayerId());
            
            player = int(input('\nWhich player scored (players:'+playersString+')? '))
            
            while player not in playersList: #Input validation
                player = int(input('\nPlease enter a valid choice (players:'+playersString+'): '))
            
            # Award points to player
            self.__players[player].addScore(score)

            #Awards score to the proper team
            if (team == 1):
                self.__homeTeam.incrementScore(score)
            else:
                self.__awayTeam.incrementScore(score)

            #Asks user to if they wish to enter another score    
            choice = str(input('\nScore recorded. Enter another? (y/n): '))

            while choice not in ["y", "n"]: #Input validation
                choice = str(input('\nPlease enter a valid choice. Enter another score? (y/n): '))

            #Loops if yes, breaks if no
            if (choice == 'y'):
                repeat = True
            else:
                repeat = False

        menu(gameObj)

    #Displays team scores for now. Will later display both team and individual player scores/stats
    def viewScore(self, gameEnd):
        os.system('cls')
        if(gameEnd):
             print('\n-----Final Scores-----\n')
        else:
            print('\n-----Scores-----\n')
        print(self.__homeTeam.getTeamName() + ': ' + str(self.__homeTeam.getScore()) + '\t' + self.__awayTeam.getTeamName() + ': ' + str(self.__awayTeam.getScore()) + '\n' )
        
        if(gameEnd):
            if(self.__homeTeam.getScore() > self.__awayTeam.getScore()):
                print(self.__homeTeam.getTeamName() + " win!");
            elif(self.__homeTeam.getScore() < self.__awayTeam.getScore()):
                print(self.__awayTeam.getTeamName() + " win!");
            else:
                print("The game ended in a tie");
        
        print('\n-----Player Data-----\n')
        
        print('Team\tPlayer\tTwo\tThree\tFree\tTotal')
        
        for playerId in self.__players:
            cPlayer = self.__players[playerId]
            if(cPlayer.getTeam() == 1):
                team = "Bulls"
            else:
                team = "Lakers"
            print(team+"\t"+str(cPlayer.getPlayerId())+"\t"+str(cPlayer.getTwoPoint())+"\t"+str(cPlayer.getThreePoint())+"\t"+str(cPlayer.getFreeThrows())+"\t"+str(cPlayer.getTotalScore()))

        #Pauses the system
        input('Press <enter> to continue...')

    
    def endGame(self):
        self.viewScore(True)


#Defines the Team class    
class Team:

    def __init__(self, teamName, teamId):
        self.__score = 0
        self.__teamId = teamId
        self.__teamName = teamName

    def getScore(self):
        return self.__score

    def getTeamName(self):
        return self.__teamName

    def getId(self):
        return self.__teamId

    def incrementScore(self, score):
        self.__score += score
    
    def getPlayers(self, playerDict):
        returnDict = {}
        for i in playerDict:
            if playerDict[i].getTeam() == self.__teamId:
                returnDict[i] = playerDict[i]
        
        return returnDict
                

#Defines the Player class
class Player:

    def __init__(self, playerId, team):
        self.__playerId = playerId
        self.__team = team
        self.__threePoint = 0
        self.__twoPoint = 0
        self.__freeThrows = 0
        self.__totalScore = 0

    def getPlayerId(self):
        return self.__playerId

    def getThreePoint(self):
        return self.__threePoint

    def getTwoPoint(self):
        return self.__twoPoint

    def getFreeThrows(self):
        return self.__freeThrows
        
    def getTotalScore(self):
        return self.__totalScore

    def getTeam(self):
        return self.__team
        
    def addScore(self, score):
        if(score == 1):
            self.__freeThrows += 1
        elif(score == 2):
            self.__twoPoint += 1
        elif(score == 3):
            self.__threePoint += 1
        
        self.__totalScore += score
        
        

        
#Main method. Checks to see if file is being run as itself or called by another python module
if __name__ == '__main__':
    gameObj = Game("Bulls", "Lakers")
    while menu(gameObj):
        continue
