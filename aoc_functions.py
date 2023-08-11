import copy

#main datase [town 1, town 2, path name, distance between town 1 and town 2, pheromone level, probability to choose the path]
mainDataset = [[1,2,1,7,0.01,0],[1,3,2,5,0.01,0],[1,4,3,2,0.01,0],[2,3,4,4,0.01,0],[2,4,5,9,0.01,0],[3,4,6,5,0.01,0]]
afterVisit = [[1,2,1,6,0.01,0],[1,3,2,5,0.01,0],[1,4,3,2,0.01,0],[2,3,4,4,0.01,0],[2,4,5,9,0.01,0],[3,4,6,5,0.01,0]]

alpha = 1
beta = 1
ants = 1
evap = 0.9
numberOfTowns = 4
sumProb = 0 #initial sum of all probabilities
visited = [1]
usedPaths = []
highestProb = []
tempMainDataset = []
pathtoUpdate = []

class aco(object):

    def __init__(self, data):
        self.data = mainDataset

    def run(self):
        for i in range(numberOfTowns - 1):
#            print("Running Self!")
            self.move(visited)
#            print("Self finished.\n")
#            print("Paths to go are: ", usedPaths)
    
    def dataset(self, visited, usedPaths): #Removes entries from original dataset by path visited, not to go through same path
        #create copy of the mainDataset
        if visited[-1] == 1: #Marks start from beginning, take the original dataset
            tempMainDataset = copy.deepcopy(mainDataset)
#            print("New dateset is ", tempMainDataset)
        else:
            tempMainDataset = copy.deepcopy(mainDataset)
            for k in tempMainDataset:
                for j in usedPaths:
                    if k[2] == j:
                        tempMainDataset.remove(k)
#            print("New temp dataset from else is ", tempMainDataset)
        return tempMainDataset

    def sumProbabilities(self, data): #Calculate sum of all probabilities
        global sumProb
        for j in data:
            p = (j[4])**alpha*(1/j[3])**beta
            sumProb = sumProb + p
        #print("Sum of probabilities is: ", sumProb)
        return sumProb

    def calcProbs(self, visited):
        highestProb = []
        set = self.dataset(visited, usedPaths)
#        print("Dataset is", set)
#        print("Visisted[-1] is ", visited[-1])
        visit = visited[-1]
        for l in set:
            if (l[0] == visit or l[1] == visit):
                ni = 1/l[3] #calculate 1/d #calculate ni
                pher = l[4] + (0.001*1/l[3]) #calculate pheromon level
                totalProb = self.sumProbabilities(set) #Get sum of probabilities
                prob = ((pher)**alpha*(ni)**beta)/(totalProb) #calculate new probablity to visit the location
                l[4] = pher
                l[5] = prob
                highestProb.append(l) #write all calculated probabilities in array
#        print("Highestprob is", highestProb)
        return highestProb

    def move(self, visited):
        global mainDataset    
        probabilities = self.calcProbs(visited)
        selectHighestProb = max(probabilities, key=lambda x: x[5]) #Get which list has highest calculated probability
#        print("Highest probability is in ", selectHighestProb)
        pathtoUpdate = selectHighestProb[2] #Get path that needs to be updated
#        print("Path to update is: ", pathtoUpdate)
        for l in mainDataset:
            if l[2] == selectHighestProb[2]:
                l.pop()
                l.append(selectHighestProb[5])
        if selectHighestProb[0] == visited[-1]:
#            print("The town to go to is", selectHighestProb[1], "by moving through path", pathtoUpdate)
            visited.append(selectHighestProb[1])
        else:
#            print("The town to go to is", selectHighestProb[0], "by moving through path", pathtoUpdate)
            visited.append(selectHighestProb[0])
        usedPaths.append(pathtoUpdate)
#        print("Visited places are ", visited, ". Length of Visited is ", len(visited))
        
        if len(visited) == numberOfTowns:   
            for i in mainDataset:
                if i[0] == 1 and i[1] == visited[-1]:
                    pher = i[4] + (0.001*1/i[3]) #calculate pheromon level
                    i[4] = pher
                    i[5] = (i[4])**alpha*(1/i[3])**beta
#                    print("The town to go to is 1 ", "by moving through path", i[2])
                    visited.append(i[0])
                    usedPaths.append(i[2])
        print("Visites places are ", visited, "with used paths", usedPaths)
        return mainDataset


for i in range(1):
    antcolony = aco(mainDataset)
    paths = antcolony.run()
    i = i + 1
    print("END!")