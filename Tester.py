from BoggleClass import Boggle,printGrid 
import os,sys

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

print('start')
words = {"barks","befog","blare","brights","frats","girl","lair","pore","rife","ship","skat","skip","stun","ulnar"}
myBoggle = Boggle(words, 'b', (0,2))
myBoggle.placeNeighbors(0,2)
printGrid(myBoggle.grid)
print("ITERATIONS", myBoggle.iterations)
print('end')



print('start')
words = {"clef","flag","flanks","futile","glance","glitz","glut","kale","lieu","scald","site","skim","smote","soil","ticks"}
myBoggle2 = Boggle(words, 'k', (1,0))
myBoggle2.placeNeighbors(1,0)
printGrid(myBoggle2.grid)
print("ITERATIONS", myBoggle2.iterations)
print('end')

print('start')
words = {"barks","befog","blare","brights","frats","girl","lair","pore","rife","ship","skat","skip","stun","ulnar"}
myBoggle3 = Boggle(words, 'b', (0,2))
myBoggle3.placeNeighbors(0,2)
printGrid(myBoggle3.grid)
print("ITERATIONS", myBoggle3.iterations)
print('end')


# Count = 0
# for i in range(2):
#     print('start')
#     words = {"barks","befog","blare","brights","frats","girl","lair","pore","rife","ship","skat","skip","stun","ulnar"}
#     myBoggle = Boggle(words, 'b', (0,2))
#     blockPrint()
#     myBoggle.placeNeighbors(0,2)
#     enablePrint()
#     printGrid(myBoggle.grid)
#     print("ITERATIONS", myBoggle.iterations)
#     print('end')
# #     iterations = main()
# #     Count = Count + iterations
# #     print(iterations,Count)


