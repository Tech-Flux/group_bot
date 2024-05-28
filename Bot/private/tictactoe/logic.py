# tictactoe_bot.py
from telebot import TeleBot, types
from .main import TicTacToe
from .gold import get_user_gold, add_user_gold
games = {}

def init_bot(bot, db):
    @bot.message_handler(commands=['tictactoe'])
    def start_tictactoe(message):
        chat_id = message.chat.id
        if message.chat.type != 'private':
            bot.send_message(chat_id, "This command can only be used in private chats.")
            return

        if chat_id in games:
            bot.send_message(chat_id, "A game is already in progress. Use /exit to leave the game.")
            return
        
        games[chat_id] = TicTacToe()
        bot.send_message(chat_id, "Tic-Tac-Toe game started! You are X. Use /move <1-9> to make a move.\n" + render_board(games[chat_id]))

    @bot.message_handler(commands=['move'])
    def move(message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        if chat_id not in games:
            bot.send_message(chat_id, "No game in progress. Use /start_tictactoe to start a new game.")
            return

        try:
            move_pos = int(message.text.split()[1]) - 1
            if move_pos not in range(9):
                raise ValueError
        except (IndexError, ValueError):
            bot.send_message(chat_id, "Invalid move. Use /move <1-9> to make a move.")
            return

        game = games[chat_id]
        if not game.make_move(move_pos, 'X'):
            bot.send_message(chat_id, "Invalid move. The position is already occupied.")
            return
        
        if game.current_winner:
            bot.send_message(chat_id, "Congratulations! You won the game!\n" + render_board(game))
            add_user_gold(user_id, 100, db)
            current_gold = get_user_gold(user_id, db)
            bot.send_message(chat_id, f"You have been awarded 100 gold. Total gold: {current_gold}")
            del games[chat_id]
            return

        if len(game.available_moves()) == 0:
            bot.send_message(chat_id, "It's a tie!\n" + render_board(game))
            del games[chat_id]
            return

        # Let the bot make a move
        bot_move = random.choice(game.available_moves())
        game.make_move(bot_move, 'O')

        if game.current_winner:
            bot.send_message(chat_id, "You lost the game!\n" + render_board(game))
            del games[chat_id]
            return

        if len(game.available_moves()) == 0:
            bot.send_message(chat_id, "It's a tie!\n" + render_board(game))
            del games[chat_id]
            return

        bot.send_message(chat_id, render_board(game))

    @bot.message_handler(commands=['exit'])
    def exit_game(message):
        chat_id = message.chat.id
        if chat_id in games:
            del games[chat_id]
            bot.send_message(chat_id, "You have exited the game.")
        else:
            bot.send_message(chat_id, "No game in progress.")

    def render_board(game):
        return game.print_board()

    def get_user_gold(user_id, db):
        user = db["users"].find_one({"user_id": user_id})
        if user:
            return user.get("gold", 0)
        return 0

    def add_user_gold(user_id, amount, db):
        db["users"].update_one({"user_id": user_id}, {"$inc": {"gold": amount}}, upsert=True)