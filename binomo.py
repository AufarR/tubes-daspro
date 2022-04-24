# Python library imports
import os
import argparse

# Module imports
import reusables
import mainproc

# Global state variable declarations

user_list = []
# list of list of (user_id, username, name, password, role, balance : string)

game_list = []
# list of list of (game_id, name, category, release_year, price, stock: string)

trx_hist = []
# list of list of (game_id, name, price, user_id, purchase_year: string)

own_list = []
# list of list of (game_id, user_id: string)

cwd = os.path.dirname(os.path.abspath(__file__)) # get file location (file location = project main directory)

# Set current user is initial value to logged out (-1)
current_user_id = "-1"

# Get data folder argument
parser = argparse.ArgumentParser()
parser.add_argument("dir", nargs='?', default="", help="data directory")
args = parser.parse_args()

# Initialization
initLists = mainproc.load(cwd, args.dir)
if not initLists[0][0]: # Initialization error
    print(initLists[0][1]) # print error msg
    print("Exiting....")
    exit() # Terminate program
user_list, game_list, trx_hist, own_list = initLists[1][0], initLists[1][1], initLists[1][2], initLists[1][3] # Set all data variables

# Main menu
while True:
    if current_user_id != "-1":
        print("\nSelamat datang di antarmuka Binomo, "+user_list[reusables.get_idx(user_list,current_user_id,0)][2]+"!")
    else:
        print("\nSelamat datang di antarmuka Binomo!")
    menuInput = input("Menu (ketik help untuk bantuan) \n>>> ").lower() # Menu input
    roleCheck = mainproc.role_check(menuInput, current_user_id, user_list)
    if not roleCheck[0]: # Auth check
        print(roleCheck[1]) # Send error message on auth error
    elif menuInput == "register":
        user_list = mainproc.register(user_list)
    elif menuInput == "login":
        current_user_id = mainproc.login(current_user_id,user_list)
    elif menuInput == "tambah_game":
        game_list = mainproc.tambah_game(game_list)
    elif menuInput == "ubah_game":
        game_list = mainproc.ubah_game(game_list)
    elif menuInput == "ubah_stok":
        game_list = mainproc.ubah_stok(game_list)
    elif menuInput == "list_game_toko":
        mainproc.list_game_toko(game_list)
    elif menuInput == "buy_game":
        newLists = mainproc.buy_game(game_list,current_user_id,user_list,own_list,trx_hist)
        user_list, game_list, trx_hist, own_list = newLists[0], newLists[1], newLists[2], newLists[3]
    elif menuInput == "list_game":
        mainproc.list_game(game_list,own_list,current_user_id)
    elif menuInput == "search_my_game":
        mainproc.search_my_game(own_list,game_list,current_user_id)
    elif menuInput == "search_game_at_store":
        mainproc.search_game_at_store(game_list)
    elif menuInput == "topup":
        user_list = mainproc.topup(user_list)
    elif menuInput == "riwayat":
        mainproc.riwayat(trx_hist,current_user_id)
    elif menuInput == "help":
        mainproc.bantuan(roleCheck[1])
    elif menuInput == "kerangajaib":
        print(mainproc.kerangAjaib())
    elif menuInput == "tictactoe":
        print(mainproc.ticTacToe())
    elif menuInput == "save":
        mainproc.save((user_list,game_list,trx_hist,own_list),cwd)
    elif menuInput == "exit":
        if mainproc.exit_prompt(current_user_id):
            mainproc.save((user_list,game_list,trx_hist,own_list),cwd)
        break # ends main menu
    else:
        continue # return to main menu until user chooses to exit
print("Sampai jumpa!") # Exit message