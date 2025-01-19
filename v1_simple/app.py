from game import Game

if __name__ == "__main__":
    while True:
        name = input("Please enter your name (1-19 characters): ")
        if 1 <= len(name) <= 19:
            break
        print("Invalid name length. Try again.")

    game = Game(name)
    game.initialize_game()
    game.run()