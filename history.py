class History:
    def __init__(self):
        self.clear()
        
    def clear(self):
        self.undo_list = []
        self.redo_list = []        
        
    def update(self, row, col, num, oldnum):
        action = (row, col, num, oldnum)
        self.undo_list.append(action)
        self.redo_list.clear()

    def undo(self):
        if not self.undo_list:
            return None
        action = self.undo_list.pop()
        self.redo_list.append(action)
        return action

    def redo(self):
        if not self.redo_list:
            return None
        action = self.redo_list.pop()
        self.undo_list.append(action)
        return action

"""
if __name__ == "__main__":
    hist = History()
    hist.update("1", "1", "1", "0")
    hist.update("1", "2", "2", "0")
    hist.update("1", "3", "3", "0")
    print(hist.undo())
    print(hist.undo())
    print(hist.redo())
    print(hist.undo())
    hist.update("1", "4", "4", "0")

    pass
"""