from random import shuffle
from collections import Counter, defaultdict
from sys import exit


class Domino:

    def __init__(self):
        self.status = ''
        self.player, self.computer, self.snake = [list() for _ in range(3)]
        self.stock = [[x, y] for x in range(0, 7) for y in range(x, 7)]

        self.new_game()
        self.who_is_first()
        self.game_info()

    def new_game(self):
        shuffle(self.stock)
        for _ in range(7):
            self.player.append(self.stock.pop())
            self.computer.append(self.stock.pop())

    # Seeking high pair and taking it to snake
    def who_is_first(self):
        for num in range(6, 0, -1):
            if [num, num] in self.player:
                self.status = 'computer'
                self.snake.append(self.player.pop(self.player.index([num, num])))
                break
            elif [num, num] in self.computer:
                self.status = 'player'
                self.snake.append(self.computer.pop(self.computer.index([num, num])))
                break
        if self.status == '':
            self.reshuffle()
            self.new_game()
        return

    def reshuffle(self):
        self.stock.extend(self.player)
        self.player.clear()
        self.stock.extend(self.computer)
        self.computer.clear()

    def info(self):
        print('=' * 70)
        print(f'Stock size: {len(self.stock)}')
        print(f'Computer pieces: {len(self.computer)}\n')
        if len(self.snake) >= 6:
            print(*self.snake[:3], '...', *self.snake[-3:], '\n')
        else:
            print(*self.snake, '\n')
        print('Your pieces:')
        [print(f'{i}:{domino}') for i, domino in enumerate(self.player, start=1)]
        print('')

    def game_info(self):
        while not self.game_over():
            self.info()
            self.players_move() if self.status == 'player' else self.computers_move()

    def game_over(self):
        # before computer move: if player has no dominoes - player won
        if self.status == 'computer' and len(self.player) == 0:
            self.info()
            print('Status: The game is over. You won!')
            return exit()
        # visa versa
        elif self.status == 'player' and len(self.computer) == 0:
            self.info()
            print('Status: The game is over. The computer won!')
            return exit()
        elif 7 in Counter([value for domino in self.snake for value in domino]).values():
            self.info()
            print("Status: The game is over. It's a draw!")
            return exit()
        return False

    def players_move(self):
        print("Status: It's your turn to make a move. Enter your command.")
        move = None
        # we need to get value from player: sigh '-' if player
        # want to put domino to the left side of the snake and '+' to the right side of
        # the snake and number of domino in sequence
        # 0 - player taking 1 domino from stock and skips the turn
        while True:
            while True:
                try:
                    move = int(input())
                except ValueError:
                    print('Invalid input. Please try again.')
                    continue

                # move - number of domino from output (index + 1)
                if move in range(-len(self.player), len(self.player) + 1):
                    break
                else:
                    print('Invalid input. Please try again.')
            if move > 0 and self.move_is_legal(self.player, move - 1):
                self.snake.append(self.player.pop(move - 1))
                break
            elif move < 0 and self.move_is_legal(self.player, abs(move) - 1, sign='-'):
                self.snake.insert(0, self.player.pop(abs(move) - 1))
                break
            elif move == 0 and len(self.stock) > 0:
                self.player.append(self.stock.pop(0))
                break
            elif move == 0 and len(self.stock) == 0:
                break
            else:
                print('Illegal move. Please try again')
        self.status = 'computer'
        return

    def computers_move(self):
        input("Status: Computer is about to make a move. Press Enter to continue...")
        domino_set = self.sort_dominoes()
        snake_ends = [self.snake[0][0], self.snake[-1][-1]]
        value_pool = [value for domino in domino_set for value in domino]
        for domino in domino_set:
            if snake_ends[1] in domino:
                if snake_ends[1] == domino[0]:
                    self.snake.append(self.computer.pop(self.computer.index(domino)))
                    break
                else:
                    self.snake.append(self.computer.pop(self.computer.index(domino))[::-1])
                    break
            elif snake_ends[0] in domino:
                if snake_ends[0] == domino[1]:
                    self.snake.insert(0, self.computer.pop(self.computer.index(domino)))
                    break
                else:
                    self.snake.insert(0, self.computer.pop(self.computer.index(domino))[::-1])
                    break
            elif snake_ends[0] not in value_pool or snake_ends[1] not in value_pool:
                if len(self.stock) > 0:
                    self.computer.append(self.stock.pop(0))
                    break
                else:
                    break
            else:
                continue
        self.status = 'player'
        return

    def sort_dominoes(self):
        common_nums = Counter([value for domino in self.computer + self.snake for value in domino])
        rated = defaultdict(list)
        most_favorable = []
        for domino in self.computer:
            rated[common_nums[domino[0]] + common_nums[domino[1]]].append(domino)
        for _ in range(len(rated)):
            for key, value in rated.items():
                if key == max(rated.keys()):
                    most_favorable.extend(value for value in rated[key])
            rated.pop(max(rated.keys()))
        return most_favorable

    def move_is_legal(self, d_list, number, sign=''):
        if sign == '' and number >= 0:
            if self.snake[-1][-1] in d_list[number]:
                if self.snake[-1][-1] == d_list[number][0]:
                    return True
                elif self.snake[-1][-1] != d_list[number][0]:
                    d_list[number] = d_list[number][::-1]
                    return True
        elif sign == '-':
            if self.snake[0][0] in d_list[number]:
                if self.snake[0][0] == d_list[number][1]:
                    return True
                elif self.snake[0][0] != d_list[number][1]:
                    d_list[number] = d_list[number][::-1]
                    return True
        else:
            return False


if __name__ == '__main__':
    game = Domino()
