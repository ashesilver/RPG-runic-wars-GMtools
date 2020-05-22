import socket
### Main server specs
"""
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((socket.gethostname(),19999))
s.listen(10)"""


#socket exemple :
"""
while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    clientsocket.send(bytes("Hey there!!!","utf-8"))"""

def var(*str):
    res =[]
    for x in str :
        try :
            res.append(globals()[x])
        except KeyError:
            globals()[x]=None
            res.append(globals()[x])
    return res

def await_data_from_client(s):
    data= None
    while data == None:
        data = s.recv(1024)

    return data.decode("utf-8")

def wincheck(grid):
    fullslots = [[l,n] for l in ["A","B","C"] for n in ["1","2","3"]]
    Xslots = [x for x in fullslots if grid[fullslots.index(x)] is "X"];Oslots = [x for x in fullslots if grid[fullslots.index(x)] is "O"]
    for i in range (3):
        if (fullslots[3*i] in Xslots and fullslots[3*i+1] in Xslots and fullslots[3*i+2] in Xslots) or (fullslots[i] in Xslots and fullslots[i+3] in Xslots and fullslots[i+6] in Xslots):
            return (1,0)
        elif (fullslots[3*i] in Oslots and fullslots[3*i+1] in Oslots and fullslots[3*i+2] in Oslots) or (fullslots[i] in Oslots and fullslots[i+3] in Oslots and fullslots[i+6] in Oslots):
            return (0,1)
    if (["A","1"] in Xslots and ["B","2"] in Xslots and ["C","3"] in Xslots) or (["C","1"] in Xslots and ["B","2"] in Xslots and ["A","3"] in Xslots):
        return (1,0)
    elif (["A","1"] in Oslots and ["B","2"] in Oslots and ["C","3"] in Oslots) or (["C","1"] in Oslots and ["B","2"] in Oslots and ["A","3"] in Oslots):
        return (0,1)
    else :
        return (0,0)

def main(clientsockets):
    #base values

    grid = [" "]*9
    turn = 0; winX,winO = False,False

    #test values

    #execution
    while (not (winX or winO)) and turn < 9 :
        #send to players the grid
        #send draw flag
        #draw(grid)

        for x in clientsockets :
            x.send(bytes("GRID"+ str(grid)))
            x.send(b"DRAW")

        #send an await or play flag to clients
        #recieve the updated grid
        #send to the awaiting client the new grid
        #grid = play(1+(turn%2),grid)

        args = (1+(turn%2),grid)
        clientsockets[turn%2].send(bytes("PLAY"+str(args)))
        clientsockets[(turn%2+1)%2].send(b"AWAIT")

        data = await_data_from_client(clientsockets[turn%2])
        if data.startswith("GRID") :
            grid = list(data[4:])
        clientsockets[(turn%2+1)%2].send(bytes("GRID"+ str(grid)))

        winX,winO = wincheck(grid)
        turn+=1
    
    def win_print():
        if winX:
            for x in clientsockets :
                x.send(b"RESplayer 1 wins !","utf-8")
        elif winO :
            for x in clientsockets :
                x.send(b"RESplayer 2 wins !","utf-8")
        else :
            for x in clientsockets :
                x.send(b"RESdraw !","utf-8")
            
    win_print()

try :
    if __name__ == "__main__" :
        __credits__ = "Tersinet Thibault"


        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((socket.gethostname(),19999))
        s.listen(10)

        player_1_s, player_2_s = None, None

        while player_1_s == None or player_2_s == None:
            if player_1_s == None :
                player_1_s, add1 = s.accept()
                print(f"got one : {add1}")
                player_1_s.send(b"Sucessfully connected as player_1!")
            else :
                player_2_s, add2 = s.accept()
                print(f"got both : {add2}")
                player_2_s.send(b"Sucessfully connected as player_2!")


        var("empty", "player_1", "player_2")
        empty = " "; player_1 = "X"; player_2 = "O"

        main((player_1_s,player_2_s))

        for x in (player_1_s,player_2_s) :
            x.send("END",'utf-8')

        for x in (player_1_s,player_2_s) :
            x.close()

        """
        play = True
        while play :
            main()
            kjbhv = input("replay ? (y/n)")
            play = "y" in kjbhv.lower()"""
except :
    import sys
    input(sys.exc_info()[:2])