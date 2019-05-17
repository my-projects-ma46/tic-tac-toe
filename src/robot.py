

class TreeNode:
    def __init__(self, gridState, previousState=None):
        self.gridState = gridState
        self.nextStates = []
        for i in range(10):
            self.nextStates.append(None)
        self.previousState = previousState
        


class TreeStates:
    def __init__(self, game, initialState):
        self.treeRoot = TreeNode(game.currentGridState)
        #self.treeRoot.previousState = None


class Robot:
    def __init__(self, game):
        pass
