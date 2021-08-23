import time
import board
import touchio
yellow = touchio.TouchIn(board.A2)
green = touchio.TouchIn(board.A5)
red = touchio.TouchIn(board.A6)
blue = touchio.TouchIn(board.A10)
while True:
    if yellow.value:
        print('yellow left back A2 on')
    else:
        print('yellow left back A2 off')

    if green.value:
        print('green left front A5 on')
    else:
        print('green left front A5 off')

    if red.value:
        print('red back right A6 on')
    else:
        print('red back right A6 off')
        
    if blue.value:
        print('blue front right A10 on')
    else:
        print('blue front right A10 off')

    time.sleep(0.5)
