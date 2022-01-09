from pyamaze import maze,agent,textLabel
from queue import PriorityQueue

class MazeCell:
    def __init__(self, parent: "MazeCell", position: tuple):
        self.cost = 0
        self.parent = parent
        self.position = position

    def __NE__(self, other: "MazeCell"):
        return self.position != other.position
    def __lt__ (self,other: "MazeCell"):
        return self.position < other.position

def heuristic(cell1,cell2):
    return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])

def aStarPathPlanning(maze):
    start = MazeCell(None,(1,1))
    goal = MazeCell(None,(maze.rows,maze.cols))
    combinedCost={} #Holds the combined cost(cell cost + heuristic cost) based on the position of the maze (NOT object wise)
    cellQueue=PriorityQueue()
    cellQueue.put((heuristic(start.position,goal.position),heuristic(start.position,goal.position),start))
    for cell in maze.grid:
        combinedCost[cell] = float('inf')
    while not cellQueue.empty():
        currCell = cellQueue.get()[2]
        currCellPosition=currCell.position
        if currCellPosition==goal.position:
            goal.parent = MazeCell(currCell,currCellPosition)
            break
        for d in 'ESNW':
            if maze.maze_map[currCellPosition][d]==True:
                # print(d)
                if d=='E':
                    childCellPosition=(currCellPosition[0],currCellPosition[1]+1) 
                if d=='W':
                    childCellPosition=(currCellPosition[0],currCellPosition[1]-1)
                if d=='N':
                    childCellPosition=(currCellPosition[0]-1,currCellPosition[1])
                if d=='S':
                    childCellPosition=(currCellPosition[0]+1,currCellPosition[1])
                tempCost = currCell.cost + 1
                tempTotalCost = tempCost + heuristic(currCellPosition,goal.position)
                if tempTotalCost < combinedCost[childCellPosition]:
                    combinedCost[childCellPosition] = tempTotalCost
                    childCell = MazeCell(currCell,childCellPosition)
                    childCell.cost = tempCost
                    cellQueue.put((tempTotalCost,heuristic(childCellPosition,goal.position),childCell))
    fwdPath={}
    cell=goal
    while cell!=start:
        fwdPath[cell.parent.position]=cell.position
        cell=cell.parent
    print(fwdPath)
    return fwdPath



    



if __name__=='__main__':
    myMaze=maze(12,12)
    myMaze.CreateMaze(12,12,pattern='v',loopPercent=30)
    path=aStarPathPlanning(myMaze)

    a=agent(myMaze,x=1,y=1,footprints=True)
    myMaze.tracePath({a:path})
    l=textLabel(myMaze,'A Star Path Length',len(path)+1)

    myMaze.run()