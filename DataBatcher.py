from collections import deque

class DataBatcher:
    
    def __init__(self, keyFunc, valFunc=None):
        self.keyFunc = keyFunc
        self.valFunc = valFunc
        self.prevKey = None
        self.batches = deque()
        self.batch = None

    def addData(self, data):
        key = self.keyFunc(data)
        if key == None:
            raise Exception('Batching Key cannot be None')
        if key != self.prevKey:
            if self.batch != None:
                self.batches.append({ self.prevKey: self.batch })
            self.batch = []
            self.prevKey = key
        self.batch.append(self.valFunc(data) if self.valFunc else data)
        
    def endBatch(self):
        self.batches.append({ self.prevKey: self.batch })
        self.prevKey = None
        self.batch = None

    def getBatches(self):
        while(self.batches):
            yield self.batches.popleft()

    def getBatchesCount(self):
        return len(self.batches)
    


        
    

