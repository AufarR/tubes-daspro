# Main program procedures

# Python library imports
import os
import sys
import math
import time
import argparse
import datetime

# Reusable function imports
import reusables

# Initial loading procedure
# Requires base directory, and data directory argument
# Returns a list:
#  First element is a list of status & error msg (if any)
#  Second element is a list of initialized lists, this element is an empty list on error
def load(baseDir, dataDir):
    # Init array of initialized lists
    lists = []
    # Validate data directory
    if dataDir == "":
        return ((False,"Tidak ada nama folder yang diberikan."),lists)
    dataDirFound = False
    for root, dirs, files in os.walk(baseDir):
        for dir in dirs:
            if dataDir == dir:
                dataDirFound = True
    if not dataDirFound:
        return ((False,"Folder "+str(dataDir)+" tidak ditemukan."),lists)
    print("Loading....")
    # Data directory found, parsing tables...
    lists += [reusables.arrSort(reusables.table_parse(baseDir+"/"+dataDir+"/user.csv",";"),0)]
    lists += [reusables.arrSort(reusables.table_parse(baseDir+"/"+dataDir+"/game.csv",";"),0)]
    lists += [reusables.table_parse(baseDir+"/"+dataDir+"/riwayat.csv",";")]
    lists += [reusables.table_parse(baseDir+"/"+dataDir+"/kepemilikan.csv",";")]
    return ((True,""),lists)

# Role check function
# Checks user auth based on menu input and user role
# Returns True and role if authorized and logged in
# Returns True and blank message if authorized but not logged in
# Returns False and error message if unauthorized
def role_check(menu, user_id, userList):
  # Menu list, grouped based on auth level
  menuList = (("register","tambah_game","ubah_game","ubah_stok","topup"),("buy_game","list_game","search_my_game","riwayat"),("list_game_toko","search_game_at_store","help","save","tictactoe","kerangajaib"))
  errMsg = ("Maaf, anda tidak memiliki izin untuk menjalankan perintah berikut. Mintalah ke administrator untuk melakukan hal tersebut.","Maaf, anda harus menjadi user untuk melakukan hal tersebut.") # Error msg list
  if menu == "login" or menu == "exit": # Login and exit is always authorized
    return (True,"")
  elif user_id == "-1":
    role = ""
    # Help function is always authorized
    if menu == "help":
      return (True,role)
    return (False,"Maaf, Anda harus masuk terlebih dahulu untuk mengirim perintah selain 'login', 'help', dan 'exit'")
  # Check user role
  for user in userList:
    if user_id == user[0]:
      role = user[4]
  # Find menu input in menu list
  found = False
  auth = 9 # Init required auth level. 9 means invalid input
  for i in range(3):
    if reusables.isInArr(menuList[i],menu):
        found = True
        auth = i
  # Error if menu input is invalid
  if auth == 9:
    return (False,"Masukan tidak valid. Ketik 'help' untuk mendapatkan bantuan")
  # Menu input found, return values based on auth check  
  if (auth==2) or (auth==1 and role=="User") or (auth==0 and role=="Admin"):
    return (True,role)
  else:
    return (False,errMsg[auth])

# User registration procedure
# Access level: admin
# Requires current user list
# Returns updated user list with new user (if successfully validated)
def register(userList):
    name = input("Masukkan nama Anda: ")
    if name == "": # check if blank
        print("Nama tidak boleh kosong.")
        return userList
    uname = input("Masukkan nama pengguna (username: [a-z, A-Z, 0-9, _, -]): ")
    # username validation
    if uname == "": # check if blank
        print("Nama pengguna tidak boleh kosong.")
        return userList
    for user in userList: # check if used
        if user[1] == uname:
            print("Nama pengguna "+uname+" sudah terpakai. Silakan gunakan nama pengguna lainnya.")
            return userList
    for char in uname: # check username characters
        if not (47<ord(char)<58 or ord(char)==95 or ord(char)==45 or 64<ord(char)<91 or 96<ord(char)<123):
            print("Nama pengguna hanya boleh mengandung karakter-karakter a-z, A-Z, 0-9, _, dan -")
            return userList
    password = input("Masukkan kata sandi: ")
    if password == "": # check if blank
        print("Kata sandi tidak boleh kosong")
        return userList
    uid = reusables.generateID(userList,0) # generate user ID
    return userList + [[str(uid),uname,name,reusables.encrypt(password),"User","0"]]

# Login procedure
# Uses current user list
# Requires current user id & user list
# If authenticated, returns logged in user id. Returns input user id otherwise
def login(currentId, userList):
    uname = input("Masukkan nama pengguna: ")
    password = input("Masukkan kata sandi: ")
    for user in userList: # Credential check
        if uname == user[1] and reusables.encrypt(password) == user[3]:
            return user[0] # If credentials match, return user id
    # Credentials mismatched, return input user id & print error message
    print("Nama pengguna atau kata sandi salah.")
    return currentId

# Help procedure
# Requires current user role
# Print commands list available to the user
# Does not return any specific value
def bantuan(role):
    print("============ HELP ============")
    if role == "Admin":
        print("-> register - Melakukan registrasi pengguna baru")
        print("-> login - Melakukan login ke dalam sistem")
        print("-> tambah_game = Menambah game yang dijual di toko")
        print("-> ubah_game = Mengubah data game yang dijual di toko berdasarkan ID")
        print("-> ubah_stok = Mengubah stok game di toko berdasarkan ID")
        print("-> list_game_toko = Melihat daftar game di toko berdasarkan ID, tahun rilis, dan harga")
        print("-> search_game_at_store = Mencari game di toko dari ID, nama, harga, kategoti, dan tahun rilis")
        print("-> topup = Mengisi saldo pengguna")
        print("-> help = Membuka halaman bantuan ini")
        print("-> save = Menyimpan semua perubahan data")
        print("-> exit = Mengakhiri program")
    elif role == "User":
        print("-> login - Melakukan login ke dalam sistem")
        print("-> list_game_toko = Melihat daftar game di toko berdasarkan ID, tahun rilis, dan harga")
        print("-> buy_game = Membeli game sesuai masukan ID")
        print("-> list_game = Melihat daftar game milik pengguna")
        print("-> search_my_game = Mencari game milik pengguna dari ID dan tahun rilis")
        print("-> search_game_at_store = Mencari game di toko dari ID, nama, harga, kategoti, dan tahun rilis")
        print("-> riwayat = Melihat riwayat pembelian game pengguna")
        print("-> help = Membuka halaman bantuan ini")
        print("-> save = Menyimpan semua perubahan data")
        print("-> exit = Mengakhiri program")
    else:
        print("-> login - Melakukan login ke dalam sistem")
        print("-> help = Membuka halaman bantuan ini")
        print("-> exit = Mengakhiri program")
    return True

# Save to csv procedure
# Access-level: Logged-in
# Requires list of current data lists; and current working directory
# Does not return any specific value
def save(arr,cwd):
    headers = ("id;username;nama;password;role;saldo","id;nama;kategori;tahun_rilis;harga;stok","game_id;nama;harga;user_id;tahun_beli","game_id;user_id") # csv headers
    saveDir = input("Masukkan nama folder penyimpanan: ")
    # Validation & existence check
    for char in saveDir:
        if char == "/" or saveDir == "..": # saving directory must be within the top-level of project root folder
            print("Folder penyimpanan harus setingkat dengan folder utama program")
            return False
    dirExists = False
    for root, dirs, files in os.walk(cwd):
        for file in files:
            if saveDir == file: # Check if file exists with the same name
                print("Terdapat berkas dengan nama yang sama dengan nama folder yang dimasukkan. Tidak dapat menyimpan")
                return False
        for dir in dirs: # Check if directory exists
            if saveDir == dir:
                dirExists = True
    # Input validated, create directory if not exists
    if not dirExists:
        os.mkdir(saveDir)
    # Create csv files
    reusables.array_to_csv(cwd+"/"+saveDir+"/user.csv",reusables.arrSort(arr[0],0),headers[0],";","\n")
    reusables.array_to_csv(cwd+"/"+saveDir+"/game.csv",reusables.arrSort(arr[1],0),headers[1],";","\n")
    reusables.array_to_csv(cwd+"/"+saveDir+"/riwayat.csv",arr[2],headers[2],";","\n")
    reusables.array_to_csv(cwd+"/"+saveDir+"/kepemilikan.csv",arr[3],headers[3],";","\n")

    # Success
    print("Data telah disimpan pada folder "+saveDir+".")
    return True

# Procedure to display all user-owned games
# Access-level: user
# Requires game & ownership data; and current user id
# Does not return any specific value
def list_game(game_list,own_list,userId):
    list = "Daftar game yang dimiliki:" # Initialization
    i = 0 # List number iterator
    for game in own_list: # Find game in ownership list
        if game[1] == userId:
            i += 1
            for entry in game_list: # Get game data from game list
                if game[0] == entry[0]:
                    list += "\n("+str(i)+")\n "+entry[1]+"\n ID: "+entry[0]+"\n "+entry[3]+", "+entry[2]+"\n Harga toko: "+entry[4]
    if i == 0: # No owned games
        print("Maaf, kamu belum membeli game. Ketik perintah beli_game untuk membeli.") # Output
    else: # User owns one or more game
        print(list) # Output list
    return True

# Change game stock
# Access level: admin
# Requires game list data
# Returns updated game list
def ubah_stok(game_list):
    gameId = input("Masukkan ID game: ")
    # Game ID validatoion
    if not reusables.isInArrofArr(game_list,gameId,0): # Existence check
        print("Tidak ada game dengan ID tersebut!")
        return game_list
    i = reusables.get_idx(game_list,gameId,0) # Retrieve game index in list
    num = int(input("Masukkan jumlah: "))
    # Case: stock is not enough
    if (num + int(game_list[i][5])) < 0:
        print("Stok game "+game_list[i][1]+" gagal dikurangi karena stok kurang. Stok sekarang: "+game_list[i][5]+" (<"+str(-num)+")")
        return game_list
    game_list[i][5] = str(int(game_list[i][5]) + num) # Game list update
    # Case: stock is enough
    if num > 0:
        print("Stok game "+game_list[i][1]+" berhasil ditambahkan. Stok sekarang: "+game_list[i][5])
    elif num < 0:
        print("Stok game "+game_list[i][1]+" berhasil dikurangi. Stok sekarang: "+game_list[i][5])
    # Case: stock is not changed
    else: # num == 0
        print("Stok game "+game_list[i][1]+" tidak diubah. Stok sekarang: "+game_list[i][5])
    # Return updated list
    return game_list


# Game purchase procedure
# Access level : user
# Requires game list, current user id, user list, ownership list, and transaction list
# Returns updated user list, ownership list, transaction list, and game list
def buy_game(gameList,userId,userList,ownList,trxList):
    gameId = input("Masukkan ID game: ")
    # Check if game ID exists
    if not reusables.isInArrofArr(gameList,gameId,0):
        print("ID Game tidak ditemukan")
    # Check if game is owned
    elif reusables.isInArr(ownList,[gameId,userId]):
        print("Game sudah dimiliki.")
    # Check if game stock is empty
    elif gameList[reusables.get_idx(gameList,gameId,0)][5] <= "0":
        print("Stok game habis.")
    # Check if user balance is not enough
    elif int(userList[reusables.get_idx(userList,userId,0)][5]) < int(gameList[reusables.get_idx(gameList,gameId,0)][4]):
        print("Saldo Anda tidak mencukupi.")
    else:
        # Deduct user balance
        userList[reusables.get_idx(userList,userId,0)][5] = str(int(userList[reusables.get_idx(userList,userId,0)][5]) - int(gameList[reusables.get_idx(gameList,gameId,0)][4]))
        # Deduct game stock
        gameList[reusables.get_idx(gameList,gameId,0)][5] = str(int(gameList[reusables.get_idx(gameList,gameId,0)][5])-1)
        # Update transaction history & ownership list
        ownList += [[gameId,userId]]
        trxList += [[gameId,gameList[reusables.get_idx(gameList,gameId,0)][1],gameList[reusables.get_idx(gameList,gameId,0)][4],userId,str(datetime.datetime.now().date().year)]]
        print("Game "+gameList[reusables.get_idx(gameList,gameId,0)][1]+" berhasil dibeli!")
    return (userList,gameList,trxList,ownList)

# User balance top-up procedure
# Access level: admin
# Requires current user list
# Returns updated user list
def topup(userList):
    uname = input("Masukkan nama pengguna: ")
    # username validation
    if not reusables.isInArrofArr(userList,uname,1):
        print("Nama pengguna tidak ditemukan")
        return userList
    # get user index in list
    uid = reusables.get_idx(userList,uname,1)
    amount = int(input("Masukkan jumlah penambahan saldo: "))
    if amount <= 0: # Validation: must be positive
        print("Jumlah penambahan saldo harus positif")
        return userList
    # process balance top-up
    userList[uid][5] = str(int(userList[uid][5]) + amount)

    return userList

# Exit prompt procedure
# Requires current user id. Logged out users will have no access to save function
# Returns True if user chooses to save data, False if otherwise
def exit_prompt(userId):
    while True and (userId != "-1"):
        exit = input("Apakah Anda mau melakukan penyimpanan file yang sudah diubah? (y/n) ")
        if (exit=="Y" or exit=="y"):
            return True
        elif (exit=="N" or exit=="n"):
            return False
        else:
            print("Masukan tidak valid. Mohon ulangi")

# User-owned game search procedure
# Access level : user
# Requires game ownership data, game list, and current user id
# Does not return any specific value
def search_my_game(own_list,game_list,userId):
    list = "Daftar game pada inventory yang memenuhi kriteria:" # Output initialization
    print("Kosongkan input di bawah jika ingin tidak ingin membatasi pencarian")
    filters = [] # Filter initialization
    gameId = input("Masukkan ID game: ")
    if gameId != "":
        filters += [[gameId,0]]
    gameRelease = input("Masukkan tahun rilis game: ")
    if gameRelease != "":
        filters += [[gameRelease,3]]
    # All owned games listing
    ownedGameIds = []
    for ownedGame in own_list:
        if (ownedGame[1]==userId):
            ownedGameIds += [ownedGame[0]]
    # Check if no game is owned
    if ownedGameIds == []:
        print("Anda tidak memiliki game di inventory.")
        return False
    # Filter check
    filteredGameIds = reusables.arrFilter(game_list,filters)
    # Add entries to output
    j = 0
    for i in range(reusables.arrLen(filteredGameIds)):
        entry = game_list[filteredGameIds[i]]
        listEntry = "\n "+entry[1]+"\n ID: "+entry[0]+"\n "+entry[3]+", "+entry[2]+"\n Harga toko: "+entry[4]
        if reusables.isInArr(ownedGameIds,entry[0]): # check if filtered game is owned
            j += 1
            list += "\n("+str(j)+")"+listEntry
    # Check if no game matches input criteria
    if reusables.arrLen(filteredGameIds)==0:
        list += "\nTidak ada game pada inventory-mu yang memenuhi kriteria"
    # Output
    print(list)
    return True

# In-store game search procedure
# Access level: logged in
# Requires game list
# Does not return any specific value
def search_game_at_store(game_list):
    list = "Daftar game pada toko yang memenuhi kriteria:" # Output initialization
    print("Kosongkan input di bawah jika ingin tidak ingin membatasi pencarian")
    filters = [] # Filter initialization
    gameId = input("Masukkan ID game: ")
    if gameId != "":
        filters += [[gameId,0]]
    gameName = input("Masukkan nama game: ")
    if gameName != "":
        filters += [[gameName,1]]
    gamePrice = input("Masukkan harga game: ")
    if gamePrice != "":
        filters += [[gamePrice,4]]
    gameCat = input("Masukkan kategori game: ")
    if gameCat != "":
        filters += [[gameCat,2]]
    gameRelease = input("Masukkan tahun rilis game: ")
    if gameRelease != "":
        filters += [[gameRelease,3]]
    # Filter check
    filteredGameIds = reusables.arrFilter(game_list,filters)
    # Add entries to output
    for i in range(reusables.arrLen(filteredGameIds)):
        entry = game_list[filteredGameIds[i]]
        listEntry = "\n "+entry[1]+"\n ID: "+entry[0]+"\n "+entry[3]+", "+entry[2]+"\n Harga toko: "+entry[4]
        list += "\n("+str(i+1)+")"+listEntry
    # Check if no game matches input criteria
    if reusables.arrLen(filteredGameIds)==0:
        list += "\nTidak ada game pada toko yang memenuhi kriteria"
    # Output
    print(list)
    return True

# In-store game listing with sorting options procedure
# Requires game list
# Does not return any specific value
def list_game_toko(game_list):
    print("Pilihan skema pengurutan: harga+, harga-, tahun-, tahun+")
    sortBy = input("Skema pengurutan (input kosong artinya memilih skema pengurutan ID+): ").lower()
    # Input validation
    if sortBy != "" and sortBy != "harga+" and sortBy != "harga-" and sortBy != "tahun+" and sortBy != "tahun-":
        print("Skema sorting tidak valid.")
        return False
    # Sort check
    if sortBy == "tahun+":
        sortedList = reusables.arrSort(game_list,3)
    elif sortBy == "tahun-":
        sortedList = reusables.arrSort(game_list,3,False)
    elif sortBy == "harga+":
        sortedList = reusables.arrSort(game_list,4)
    elif sortBy == "harga-":
        sortedList = reusables.arrSort(game_list,4,False)
    else:
        sortedList = reusables.arrSort(game_list,0)
    list = "\nDaftar game toko:" # Initialization
    
    i = 0 # List number iterator
    for entry in sortedList: # Find game in ownership list
        i += 1
        list += "\n("+str(i)+")\n "+entry[1]+"\n ID: "+entry[0]+"\n "+entry[3]+", "+entry[2]+"\n Harga toko: "+entry[4]+"\n Stok: "+entry[5]
    print(list) # Output list
    return True

# Game data change (by ID) procedure
# Access level: admin
# Requires current game list
# Returns updated game list
def ubah_game(game_list):
    gameId = input("Masukkan ID game: ")
    # ID validation
    if not reusables.isInArrofArr(game_list,gameId,0):
        print("ID game tidak ditemukan")
        return game_list
    gameIdx = reusables.get_idx(game_list,gameId,0)
    new = ["","","",""] # Init changed data container [name,category,release year, price]
    # Print current game data
    print("Data game saat ini:")
    entry = game_list[gameIdx]
    print(entry[1]+"\n ID: "+entry[0]+"\n "+entry[3]+", "+entry[2]+"\n Harga toko: "+entry[4])
    print("Bantuan: kosongkan input jika tidak ingin mengubah data")
    # New data input
    new[0] = input("Masukkan nama baru game: ")
    new[1] = input("Masukkan kategori baru: ")
    new[2] = input("Masukkan tahun rilis baru: ")
    new[3] = input("Masukkan harga baru: ")
    # Game list update
    if new[0] != "":
        game_list[gameIdx][1] = new[0]
    if new[1] != "":
        game_list[gameIdx][2] = new[1]
    if new[2] != "":
        game_list[gameIdx][3] = new[2]
    if new[3] != "":
        game_list[gameIdx][4] = new[3]
    # Output
    return game_list

# New game insertion procedure
# Access level: admin
# Requires current game list
# Returns updated game list
def tambah_game(game_list):
    new = ["","","","", ""] # Init changed data container [name,category,release year, price, stock]
    while True:
        # data input
        new[0] = input("Masukkan nama game: ")
        new[1] = input("Masukkan kategori: ")
        new[2] = input("Masukkan tahun rilis: ")
        new[3] = input("Masukkan harga: ")
        new[4] = input("Masukkan stok awal: ")
        # validation
        for item in new: # check for blanks
            if item == "":
                print("Mohon masukkan semua informasi mengenai game agar dapat disimpan BNMO.")
                continue
        # Price & stock must be non-negative
        if int(new[3]) < 0:
            print("Harga game tidak boleh negatif.")
            continue
        if int(new[4]) < 0:
            print("Stok game tidak boleh negatif")
            continue
        break
    # Game list insert
    game_list += [[str(reusables.generateID(game_list,0)),new[0],new[1],new[2],str(new[3]),str(new[4])]]
    # Output
    return game_list

# User transaction history procedure
# Access level: user
# Requires current user id and transaction history data
# Prints user transaction history on screen
# Does not return any specific value
def riwayat(trx_hist,userId):
    trx_list = "Daftar game:" # Output initialization
    i = 0
    # User transaction lookup
    for trx in trx_hist:
        if trx[3] == userId:
            i += 1
            # Append entry to output:
            trx_list += "\n("+str(i)+")\n "+trx[1]+"\n ID: "+trx[0]+"\n Harga beli: "+trx[2]+"\n Tahun pembelian: "+trx[4]
    # Check if user has no transaction
    if i == 0:
        print("Maaf, kamu tidak ada riwayat pembelian game. Ketik perintah beli_game untuk membeli.")
    else:
        print(trx_list)
    return True

# Magic conch shell/kerang ajaib
# Access level: logged-in
# No parameters required
# Returns one of the following strings pseudo-randomly: "Ya","Tidak","Mungkin"
def kerangAjaib():
    # This function is based on the following equation:
    # n = (a*x + c) % m
    # n is the result, a and c is an integer constant, x is an integer variable based on current unix timestamp
    # m is an integer value based on how many kinds of answers can be generated (example: 3 answers -> m=3)
    input("Apa pertanyaanmu? ")
    # Constant declaration
    answers = ("Ya","Tidak","Mungkin")
    multiplier = 8
    adder = 7
    answerNum = reusables.arrLen(answers) # There are 3 answers
    # Get variable value
    timeStamp = int(time.time())
    # Get generated number
    answer = ( multiplier * timeStamp + adder ) % answerNum
    # Output
    return answers[answer]

# Tic tac toe
# Access level: logged-in
# No parameters required
# Returns game result message
def ticTacToe():
    board = [['#','#','#'],['#','#','#'],['#','#','#']] # Game board init
    print("Legenda:\n# Kosong\nX Pemain 1\nO Pemain 2")
    finished = False # Var to check if game is finished
    p1turn = True # Var to check which player moves in the current round
    while not finished:
        print("\nStatus Papan")
        for row in board: # Board print
            rowString = ""
            for col in row:
                rowString += col
            print(rowString)
        # Check if winner is already determined (or if there's no winner)
        # Row check
        for row in board:
            rowString = ""
            for col in row:
                rowString += col
            if rowString == "XXX" or rowString == "OOO":
                finished = True
                winningString = rowString
        # Column check
        for col in range(3):
            colString = ""
            for row in board:
                colString += row[col]
            if colString == "XXX" or colString == "OOO":
                finished = True
                winningString = colString
        # Stalemate check
        boardFilled = True
        for row in board:
            for col in row:
                if col == '#':
                    boardFilled = False
        if boardFilled:
            finished = True
            winningString = ""
        # Player round
        while not finished:
            if p1turn:
                print('\nGiliran pemain 1 "X"')
            else:
                print('\nGiliran pemain 2 "O"')
            col = int(input("Kolom [1-3]: ")) - 1
            row = int(input("Baris [1-3]: ")) - 1
            # Check if input is out of range
            if col<0 or col>2 or row<0 or row>2:
                print("Masukan tidak valid")
                continue
            # Check if square has already been filled
            if board[row][col] != '#':
                print("Kotak sudah terisi")
                continue
            # Input validated, update board & change turn
            if p1turn:
                board[row][col] = 'X'
                p1turn = False
            else:
                board[row][col] = 'O'
                p1turn = True
            break
        if finished:
            if winningString == "XXX":
                return 'Pemain 1 "X" menang'
            elif winningString == "OOO":
                return 'Pemain 2 "O" menang'
            else: ## winningString == "" -> draw
                return "Tidak ada yang menang"