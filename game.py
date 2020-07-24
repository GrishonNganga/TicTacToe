from itertools import permutations
list_of_possible_wins = [
    [1,2,3],
    [4,5,6],
    [7,8,9],
    [1,4,7],
    [2,5,8],
    [3,6,9],
    [3,5,7],
    [1,5,9]
]

def game(wins):
    player_one = []
    player_two = []
    played_moves = []
    for i in range(1,10):
        if i % 2 != 0:
            repeat = True
            while True:
                print('Player 1 play.')
                inp = input()
                try:
                    if type(inp) != 'int':
                        print("Input should be a number.")    
                    if int(inp) in played_moves:
                        print('Move already played. Play again player 1.')  
                except TypeError as e:
                    print(e)
                except ValueError as e:
                    print(e)       
                else:
                    repeat = False
                    played_moves.append(int(inp))
                    player_one.append(int(inp))           
                    print(player_one)
                    all = list(permutations(player_one, 3))
                    for i in all:
                        for j in wins:
                            i = set(i)
                            j = set(j)
                            if i == j:
                                print('Caught')
                                print(i)
                                return
                    break
        else:
            repeat = True
            while True:
                print('Player 2 play.')
                inp = input()
                if int(inp) in played_moves:
                    print('Move already played. Play again player 2.')     
                else:
                    repeat = True
                    played_moves.append(int(inp))
                    player_two.append(int(inp))
                    print(player_two)
                    all = list(permutations(player_two, 3))
                    for i in all:
                        for j in wins:
                            i = set(i)
                            j = set(j)
                            if i == j:
                                print("Caught")
                                return
                    break
                        


if __name__ == '__main__':
    game(list_of_possible_wins)