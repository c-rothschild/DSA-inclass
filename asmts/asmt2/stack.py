class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)
    
    def pop(self):
        return self.stack.pop(-1)
    
    def peek(self):
        return self.stack[-1]
    
    def len(self):
        return len(self.stack)
    
