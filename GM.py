from TicTacToe import TicTacToe


class GM:

    def __init__(self):
        self.game = TicTacToe()
        self.step_game = 0

    def game_start(self):
        self.game.init()

        while self.game:
            self.game.show()

            if self.step_game % 2 == 0:
                self.game.human_go()

            else:
                print('#########')
                self.game.computer_go()

            self.step_game += 1

        self.game.show()

    def game_over(self):
        if self.game.is_human_win:
            print("Поздравляем! Вы победили!")
        elif self.game.is_computer_win:
            print("Все получится, со временем")
        else:
            print("Ничья.")
