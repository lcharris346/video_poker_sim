# Name: Video Poker Simulation
# Date: 02/25/2024
# Author: Larry Campbell Harris, Jr. lcharris346@gmail.com
# Description:
#  -Video Poker Simulation executes games based on initial balance, bet amount, num-hands,
#    algorithm (hold random, hold all, hold none, optimization algorithm, or user input),
#    bonus type (JoB, Double Bonus, or Triple Double Bonus), 
#    multiplier type (Ultimate-X, Super-Time-Pay or None), and
#    exit condition (time, return, profit, or empty balance)
#  -Stats and Plots can be generated for analysis.

usage: Video Poker Simulation [-h] [-d] [-r] [-p] [-z MCRUNS] [-a {s1,r,d,k,i}] [-g {job,db,tdb}] [-m {None,ultx,supt}] [-s STACK] [-b BET_DENOM] [-n HANDS]

                              [-e {t,r,b}]



Simulation, Analyze, and Play Video Poker.



optional arguments:

  -h, --help            show this help message and exit

  -d, --debug           Debug

  -r, --reduce_bet      Reduce Bet based on Balance

  -p, --plot            Create Anaylsis Plots

  -z MCRUNS, --mcruns MCRUNS

                        Run Z Monte Carlo Sims

  -a {s1,r,d,k,i}, --alg {s1,r,d,k,i}

                        Algorithm choice. r=random, k=hold all, d = discard all, i = user input, s1 = optimizate

  -g {job,db,tdb}, --game {job,db,tdb}

                        Game. job: Jacks or Better, db: Double Bonus, tdb: Tripler Double Bonus

  -m {None,ultx,supt}, --multi {None,ultx,supt}

                        Multiplier Type. ultx: Ultimate X, supt: Super Times Pay

  -s STACK, --stack STACK

                        Enter balance in $

  -b BET_DENOM, --bet_denom BET_DENOM

                        Enter bet amount in $

  -n HANDS, --hands HANDS

                        Enter number of hands

  -e {t,r,b}, --exit {t,r,b}

                        Exit Condition. t: num-bets = 720, r:return >= 25*bet-amount, b: 0.8*stack < balance < 1.8*stack
