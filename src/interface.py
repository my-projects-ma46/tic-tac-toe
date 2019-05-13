import tkinter as tk
import os

BLANK = 0
CROSS = 1
CIRCLE = 2
WIN = 3
LOSE = 4

BTTN_SIZE = 1

image = {
    CROSS:'X',
    CIRCLE:'O',
    BLANK:'_',
    WIN:'',
    LOSE:''
}

line = {
    'r':'linha',
    'c':'coluna',
    'a':'diagonal cresc',
    'd':'diagonal decresc'
}

startingTurnOf = CROSS

def updateGridFrame():
    pass

class GridState:
    def __init__(self, turnOf, state=None):

        if state is None:
            self.grid = []
            for i in range(9):
                self.grid.append(BLANK)
            self.grid.append(turnOf)
        else:
            self.grid = state
    
    def setRowCol(self, row, col, symbol):
        self.grid[row*3+col] = symbol
    
    def getRowCol(self, row, col):
        return self.grid[row*3+col]

class Bttn:
    def __init__(self, i, j, game):
        self.i = i
        self.j = j
        
        self.bttnImageTxt = tk.StringVar()
        
        self.buttonState = game.currentGridState.getRowCol(i, j)
        
        self.bttn = tk.Button(game.gridFrame, textvariable=self.bttnImageTxt,
         font=("Helvetica",30), fg='black', height = BTTN_SIZE, width = BTTN_SIZE, command=lambda: self.markButton(game))
        
        self.bttn.grid(row=self.i,column=self.j)
    
    def markButton(self, game):
        temp = game.currentGridState.getRowCol(self.i, self.j)
        if((temp != CROSS) and (temp != CIRCLE)):
            self.buttonState = game.turnOf
            game.markedCells += 1
            self.bttn.config(state=tk.DISABLED)
            game.currentGridState.setRowCol(self.i, self.j, self.buttonState)
            self.bttnImageTxt.set(image[self.buttonState])
            #=== check if someone won
            if(game.isFinished()):
                if(game.winnerLine[1] == 'n'):
                    #no one won
                    game.outputText.set("Ninguém ganhou!")
                else:
                    numline = ''
                    if(game.winnerLine[0] != ' '):
                        numline = str(int(game.winnerLine[0])+1)
                    for b in game.buttons.buttons:
                        b.bttn.config(state=tk.DISABLED)
                    # color the line where player won
                    #game.markLine()
                    game.outputText.set("jogador {} ganhou na {} {}".format(
                        image[game.winner], line[game.winnerLine[1]], numline)
                    )
            else:
                game.switchTurn()

class GridButtons:
    def __init__(self, game):
        
        self.buttons = []

        for i in range(3):
            for j in range(3):
                self.buttons.append(
                    Bttn(i, j, game)
                )

    def getButtonState(self, i, j):
        return self.buttons[i*3+j].buttonState
    
class Game:
    def __init__(self, root, turnOf=None, state=None):
        
        self.currentGridState = GridState(turnOf, state)
        
        if turnOf is None:
            self.turnOf = startingTurnOf
        else:
            self.turnOf = turnOf
        
        self.winner = BLANK
        self.winnerLine = "--"
        self.markedCells = 0

        self.gridFrame = tk.Frame(root)
        self.outputText = tk.StringVar()
        self.output = tk.Label(root, textvariable=self.outputText)
        self.buttons = GridButtons(self)

        self.output.grid(row=1,column=1)
        self.gridFrame.grid(row=2,column=1,sticky=tk.W+tk.E+tk.N+tk.S)
        self.updateTurnOfTxt()

    def updateTurnOfTxt(self):
        self.outputText.set("Vez de {}".format(image[self.turnOf]))
    
    def switchTurn(self):
        if(self.turnOf == CROSS):
            self.turnOf = CIRCLE
        else:
            self.turnOf = CROSS
        self.updateTurnOfTxt()
    
    '''def markLine(self):
        lineToMark = int(self.winnerLine[0])
        direction = self.winnerLine[1]

        if(direction == 'r'):
            for i in range(3):
                self.buttons.buttons.
                if(tempWinner != self.buttons.getButtonState(i, lineToMark)):
                    finished = False
                    break'''

    def isFinished(self):
        tempWinner = BLANK

        # checking rows
        for i in range(3):
            finished = True
            tempWinner = self.buttons.getButtonState(i, 0)
            for j in range(3):
                if(tempWinner != self.buttons.getButtonState(i, j)):
                    finished = False
                    break
            if(finished and ((tempWinner == CROSS) or (tempWinner == CIRCLE))):
                self.winner = tempWinner
                self.winnerLine = "{}r".format(i)
                return True
        
        #checking columns
        for j in range(3):
            finished = True
            tempWinner = self.buttons.getButtonState(0, j)
            for i in range(3):
                if(tempWinner != self.buttons.getButtonState(i, j)):
                    finished = False
                    break
            if(finished and ((tempWinner == CROSS) or (tempWinner == CIRCLE))):
                self.winner = tempWinner
                self.winnerLine = "{}c".format(j)
                return True
        
        #checking ascending diagonal
        finished = True
        tempWinner = self.buttons.getButtonState(2, 0)
        for i in range(3):
                if(tempWinner != self.buttons.getButtonState(2-i, i)):
                    finished = False
                    break
        if(finished and ((tempWinner == CROSS) or (tempWinner == CIRCLE))):
            self.winner = tempWinner
            self.winnerLine = "0a"
            return True

        #checking descending diagonal
        finished = True
        tempWinner = self.buttons.getButtonState(0, 0)
        for i in range(3):
                if(tempWinner != self.buttons.getButtonState(i, i)):
                    finished = False
                    break
        if(finished and ((tempWinner == CROSS) or (tempWinner == CIRCLE))):
            self.winner = tempWinner
            self.winnerLine = "0d"
            return True

        # checking if no one won
        if(self.markedCells == 9):
            self.winner = BLANK
            self.winnerLine = "nn"
            return True
        
        # in case the game isn't finished
        self.winner = BLANK
        self.winnerLine = "--"
        return False
    
def reset(root):
    root.destroy()
    run()

def run():
    os.system("clear")
    width, height = 400, 300
    root = tk.Tk()
    root.title("Jogo da Velha")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    root.geometry("{}x{}+{}+{}".format(
        width, height,
        int((screen_width-width)/2),
        int((screen_height-height)/2)
        )
    )
    
    optionsFrame = tk.Frame(root)
    optionsFrame.grid(row=0,column=0)
    
    g = Game(root)

    change = tk.Button(optionsFrame, text='Nova partida',
      command=lambda: reset(root))
    change.grid()

    root.mainloop()

if(__name__ == '__main__'):
    run()