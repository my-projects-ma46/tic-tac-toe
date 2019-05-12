import tkinter as tk
import os

BLANK = 0
CROSS = 1
CIRCLE = 2
WIN = 3
LOSE = 4

image = {
    CROSS:'X',
    CIRCLE:'O',
    BLANK:'.',
    WIN:'win',
    LOSE:'lose'
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
        # fix debug
        print("novo estado do grid ",self.grid)
    
    def getRowCol(self, row, col):
        return self.grid[row*3+col]

class Bttn:
    def __init__(self, i, j, currentGridState, gridFrame, turnOf, game): # turnOf
        self.i = i
        self.j = j
        
        self.bttnImageTxt = tk.StringVar()
        
        self.buttonState = currentGridState.getRowCol(i, j)
        
        self.bttn = tk.Button(gridFrame, textvariable=self.bttnImageTxt,
         command=lambda: self.markButton(currentGridState, game))
        
        self.bttn.grid(row=self.i,column=self.j)
    
    def markButton(self, currentGridState, game):
        temp = currentGridState.getRowCol(self.i, self.j)
        if((temp != CROSS) and (temp != CIRCLE)):
            self.buttonState = game.turnOf
            currentGridState.setRowCol(self.i, self.j, self.buttonState)
            self.bttnImageTxt.set(image[self.buttonState])
            #self.bttnImageTxt = image[turnOf]
        else:
            # fix tirar isso depois
            self.buttonState = BLANK
            currentGridState.setRowCol(self.i, self.j, self.buttonState)
            self.bttnImageTxt.set(image[self.buttonState])





class GridButtons:
    def __init__(self, currentGridState, gridFrame, turnOf, game):
        
        self.buttons = []

        for i in range(3):
            for j in range(3):
                #try:
                self.buttons.append(
                    Bttn(i, j, currentGridState, gridFrame, turnOf, game)
                )
                #except:
                #    print("n deu pra criar botão {}, i={}, j={}".format(i*3+j,i,j))
    
    def getButtonState(self, i, j):
        # fix
        tent = -1
        try:
            tent = self.buttons[i*3+j].buttonState
        except:
            print("[i*3+j] deu {}, i={}, j={}".format(i*3+j,i,j))
            print("estado ",end='')
            print(tent)
        return tent
    
    '''def setButton(self, i, j, newButtonState):
        # fix isso funciona?
        self.buttons[i*3+j].buttonState = newButtonState'''
    

class Game:
    def __init__(self, root, turnOf=None, state=None):
        if state is None:
            self.currentGridState = GridState(turnOf)
        else:
            self.currentGridState = GridState(turnOf, state)
        
        if turnOf is None:
            self.turnOf = startingTurnOf
        else:
            self.turnOf = turnOf
        

        self.winner = BLANK
        self.winnerLine = "--"

        

        self.gridFrame = tk.Frame(root)
        self.outputText = tk.StringVar()
        self.output = tk.Label(root, textvariable=self.outputText)
        
        self.buttons = GridButtons(self.currentGridState, self.gridFrame, self.turnOf, self)
        
        self.output.grid(row=1,column=0)
        self.gridFrame.grid(row=2,column=0)
        self.updateTurnOfTxt()

        while(not self.isFinished()):
            pass
            # fix lupi


    def updateTurnOfTxt(self):
        self.outputText.set("Vez de {}".format(image[self.turnOf]))
    
    def switchTurn(self):
        if(self.turnOf == CROSS):
            self.turnOf = CIRCLE
        else:
            self.turnOf = CROSS
        self.updateTurnOfTxt()
    
    #def markButton(self, i,j):
    #    self.buttons[]
    
    def isFinished(self):
        
        finished = True
        for i in range(3):
            self.winner = self.buttons.getButtonState(i, 0)
            for j in range(3):
                finished = finished and (self.winner == self.buttons.getButtonState(i, j))
                # fix break quebra tudo?
                if(not finished):
                    break
            if(finished):
                self.winnerLine = "{}r".format(i)
                return True
        
        for j in range(3):
            self.winner = self.buttons.getButtonState(0, j)
            for i in range(3):
                finished = finished and (self.winner == self.buttons.getButtonState(i, j))
                # fix break quebra tudo?
                if(not finished):
                    break
            if(finished):
                self.winnerLine = "{}c".format(i)
                return True

        self.winner = BLANK
        self.winnerLine = "--"
        return False
        

def run():
    os.system("clear")

    root = tk.Tk()
    root.title("Jogo da Velha")
    root.geometry("400x400+200+200")
    
    optionsFrame = tk.Frame(root)
    
    optionsFrame.grid(row=0,column=0)
    
    g = Game(root)

    change = tk.Button(optionsFrame, text='mudar vez',
      command=lambda: g.switchTurn())

    change.grid()
    root.mainloop()

if(__name__ == '__main__'):
    run()