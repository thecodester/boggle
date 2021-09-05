import copy
from permutations import permutation

class Boggle():
    def __init__(self, words, startLetter, startSquare):
        self.startLetter = startLetter
        self.startSquare = startSquare
        self.words = words
        self.grid = [ [' ',' ', ' ', ' '], [' ',' ', ' ', ' '], [' ',' ', ' ', ' '], [' ',' ', ' ', ' ']]
        self.gridType = [ ['corner','side', 'side', 'corner'], ['side','middle', 'middle', 'side'], ['side','middle', 'middle', 'side'], ['corner','side', 'side', 'corner']]
        self.letters = {}
        self. lettersInfo = {}
        self.iterations = 0
        for word in self.words:
            self.dissectWord(word)    
        self.setLetter(startLetter,*startSquare)

    # Get basic information from each word
    def dissectWord(self,word):
        for idx, char in enumerate(word):
            self.lettersInfo.setdefault(char, set())
            if idx == 0: 
                #print(idx, char, ' FIRST')
                self.lettersInfo[char].add(word[idx+1])     
            elif idx == len(word) - 1:
                #print(idx, char, ' LAST')
                self.lettersInfo[char].add(word[idx-1])     
            else:
                #print(idx, char, ' MIDDLE')
                self.lettersInfo[char].add(word[idx-1])     
                self.lettersInfo[char].add(word[idx+1])     
        for k,v in sorted(self.lettersInfo.items()):
            self.letters[k] =  {'found' : False, 'adjacent' : v, 'location': () }
            if (len(v)>5):
                self.letters[k]['type'] = {'middle'}
            elif (len(v)>3):
                self.letters[k]['type'] = {'middle', 'side'}
            else:
                self.letters[k]['type'] = {'middle', 'side','corner'}

    # Put letter in specific place in grid. Can be permanent or temporary
    def setLetter(self,letter,row,col):
        self.grid[row][col] = letter
        #letters = {letter : {'found' : True, 'adjacent' : ['b'], 'location': square }}
        self.letters[letter]['found'] = True
        self.letters[letter]['location'] = (row,col)

        #######################################################
        # Key function that does all the work. Takes a filled
        # position in the grid and tries to find its neighbor
        # 
        # For each call it:
        # - Finds the letters unfilled neighborhood squares
        # - Finds the letters adjacent letters not yet entered into grid
        # - Goes through all the permutations for putting those remaining
        #   letters in the grid and then calls the function recursively
        # 
        #######################################################

    def placeNeighbors(self,row,col):
        self.iterations += 1

        #print('place neighbors',grid[row][col],row,col)

        # If the letter is empty, we got here by mistake and we don't want
        # to place letters and just report all is fine
        if (self.grid[row][col] == ' '):
            return True
        # Get surrounding squares and adjacent letters
        mySurroundingSquares = self.surroundingSquares(row,col)
        myAdjacentLetters = self.adjacentLetters(self.grid[row][col])

        #print(mySurroundingSquares)
        #print(myAdjacentLetters)

        # If there are no adjacent letters not placed, then check if all
        # the adjacent letters for this letter have been placed in adjacent squares
        if len(myAdjacentLetters) == 0: return self.check(row,col)

        # Check all permutations for placing letters, though first check if there are
        # enough squares for for all letters
        if  (len(mySurroundingSquares) >= len(myAdjacentLetters)):
            for p in permutation(mySurroundingSquares):
                # Save previous state if this permutation doesn't work
                #print("p",p)
                oldGrid  = copy.deepcopy(self.grid)
                oldLetters = copy.deepcopy(self.letters)
                fit = True    

                # Put each letter in, and check that the type of square needed for this letter is OK
                for idx, letter in enumerate(myAdjacentLetters):
                    self.setLetter(letter,p[idx][0],p[idx][1])
                    fit = fit and self.gridType[p[idx][0]][p[idx][1]] in self.letters[letter]['type']

                if (not fit): 
                    self.grid = copy.deepcopy(oldGrid)
                    self.letters = copy.deepcopy(oldLetters)
                    continue

                # If able to place letters, then call this function recursively for all adjacent squares
                print(self.grid)
                allOK = True
                for square in p:
                    if (not self.placeNeighbors(*square)):
                        allOK = False
                        break

                    # if (all(map(placeNeighbors,[a_tuple[0] for a_tuple in p],[a_tuple[1] for a_tuple in p]))):
                    #     #print("True",row,col)
                    #     return True
                    # If not, restore previous state and try next permutation
                if (allOK):
                    #print(grid)
                    return True
                else:
                    self.grid = copy.deepcopy(oldGrid)
                    self.letters = copy.deepcopy(oldLetters)
                    continue
        # print("False",row,col)
        # If we get to here, we did not find a way to enter letters
        return False

# Give square, get its surrounding squares
# 
# all = False, return only if the square is not yet filled
# all = True, return all
    def surroundingSquares(self,row,col,all=False):
        surrounding = []

        i = row-1
        while i <= row+1:
            j = col -1
            while j <= col+1:
                if i>=0 and i<=3 and j>=0 and j<=3 and (all or self.grid[i][j]==' '):
                    surrounding.append((i,j))
                j =j + 1
            i=i + 1
        return surrounding

    # Given letter, return list of letters not yet in the grid
    def adjacentLetters(self,letter):
        OKLetters = []
        for checkLetter in self.letters[letter]['adjacent']:
            if not self.letters[checkLetter]['found']:
                #print(letter,letters[checkLetter]['found'],checkLetter)
                OKLetters.append(checkLetter)
        #printLetters()
        return OKLetters

    # Given square coordinates, check if that letter's adjacent letters are in fact
    # in adjacent squares
    def check(self,row,col):
        mySurroundingSquares = self.surroundingSquares(row,col,True)
        #print(mySurroundingSquares)
        for letter in self.letters[self.grid[row][col]]['adjacent']:
            if not (self.letters[letter]['location'] in mySurroundingSquares): return False
        return True

#######################################################
#   Helper print functions
#######################################################
def printGrid(grid):
    print('\n------ Grid ---------')
    for i in grid:
            print(i)
    print('---------------------\n')

def printLetters(letters):
    #print(letters)
    print('\n------ Letters ---------')
    for letter, value in  letters.items():
            print(letter,' -- ',len(value['adjacent'])," -- ",value)
    print('---------------------\n')

#######################################################
#   Main function
#######################################################
def main():
    print('start')
    words = {"barks","befog","blare","brights","frats","girl","lair","pore","rife","ship","skat","skip","stun","ulnar"}
    myBoggle = Boggle(words, 'b', (0,2))
    myBoggle.placeNeighbors(0,2)
    printGrid(myBoggle.grid)
    print("ITERATIONS", myBoggle.iterations)
    print('end')


    # print("\n-------------\n")
    # for k,v in sorted(lettersInfo.items(), key=lambda item: len(item[1])):
    #     print(len(v),"--",k,v)

    # # Set the first letter and start the process
    # if (placeNeighbors(*startSquare)):
    #     printGrid()
    # else:
    #     print("No solution")

    # # Display how many times the main function was called
    # print("ITERATIONS: ",placeNeighborsCount)
    # return placeNeighborsCount
    # sideLetters = set(dict(filter(lambda elem: len(elem[1]) > 3, lettersInfo.items())).keys())


if __name__ == "__main__":
    main()