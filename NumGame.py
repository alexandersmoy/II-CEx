#!/usr/bin/env python3

# Random Integer Game
# Instructions
print('''Welcome to the number game! \n
In this game, you think of a number from 1 through n and I will try
to guess what it is.  After each guess, enter h if my guess is too
high, l if too low, or c if correct. \n''')

# Init variables
n, games, guess_total, play = 0, 0, 0, 'y'
# Try/Catch --
# n must be an integer; n must be greater than 1
while(n < 2):
    try:
        n = int(input('Please enter a number n:'))
        if (n < 2):
            print('Please enter an integer greater than 1')
    except ValueError:
        print('Please enter an integer greater than 1')

# Main Loop -- for multiple runs of the Game
while(play == 'y'):
    # Increment for each game
    games += 1
    # Init variables for each new round
    guess_num, guess_min, guess_max, response = 0, 0, n+1, ''
    # Game Loop -- for each guess
    while(response != 'c'):
        guess = (guess_min + guess_max) // 2
        # Debugging
        # print('--- guess = %d; min = %d; max = %d' %
        #       (guess, guess_min, guess_max))
        # If only one value between min/max than guess = number
        if (guess_max - guess_min == 2 or
                guess == 1 or guess == n):
            response = 'c'
        else:
            response = input('%d?' % (guess)).lower()
        # Evaluate response and act accordingly
        if (response == 'l'):
            guess_num += 1
            guess_min = guess
        elif (response == 'h'):
            guess_num += 1
            guess_max = guess
        elif (response == 'c'):
            guess_num += 1
            print('Your number is %d' % (guess))
            print('It took me %d guesses.' % (guess_num))
            guess_total += guess_num
            print('I averaged %s guesses per game for %d game(s).' %
                  (round(guess_total/games, 2), games))
            # Debugging
            # print('--- games: %d; total_guesses: %d' % (games, guess_total))
        else:
            print('Please enter h if my guess is too high, l if too low' +
                  ', or c if correct.')
    play = input('Play again (y/n)?').lower()
