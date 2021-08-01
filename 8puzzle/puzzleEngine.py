'''
    This package stores the state of each piece and computes the next states and next moves .
'''
import numpy as np
import random
import threading
import time
import copy
boardLock = threading.Semaphore()


#Global variable: board

# board = np.array([['1', '2', '3'],['6', '7', '8'],['4', '--', '5']])
# pointer=[2,1]


class Node():
    '''Every puzzle state that was explored will be saved in a Node.'''
    def __init__(self,state,dir):
        self.state = state
        self.dir = dir
        self.g = 0
        self.score = 0


class GameState(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.src=np.array([['--', '1', '2'],['3', '4', '5'],['6','7','8']])
        self.board = self.src
        self.pointer=[0,0]
        self.final_state=np.array([['1', '2', '3'],
                               ['4', '--' ,'5'],
                               ['6', '7', '8']])
        self.final_pointer=[1,1]

#-------We can choose three algorithm to search final state: bfs,ids,bidirectional,A_star
        self.searchAlgorithm='A_star'

#--------------------------

#-------The maximum level that allowed to search in IDS algorithm
        self.max_depth =10
#--------------------------


        self.whitToMove =True
#-------A list of Nodes for loging the move 
        self.moveLog =[]
#--------------------------

#-------Two list of Nodes for loging the move in Bidirectional algorithm 
        self.forward_moveLog =[]
        self.backward_moveLog =[]
#--------------------------

#-------When the final state is found, there is a list of Nodes and moves in 'found' variable
        self.found =None
#--------------------------

#-------Initialize the moveLog for BFS and IDS and A* algorithm
        intialNode =Node([self.board[:],self.pointer[:]],None)
        intialNode.score=intialNode.g+self.heuristic(intialNode.state[0])

        self.moveLog.append([intialNode])
#--------------------------

#-------Initialize the forward_moveLog and backward_moveLog for Bidirectional algorithm
        self.forward_moveLog.append([Node([self.board.copy(),self.pointer.copy()],None)])
        self.backward_moveLog.append([Node([self.final_state.copy(),self.final_pointer.copy()],None)])
#--------------------------

    def run(self):
        if(self.searchAlgorithm=='ids'):
            self.ids()
            self.print_node(self.found)
        elif(self.searchAlgorithm=='bfs'):
            while(self.found==None):
                self.bfs()
            self.print_node(self.found)
        elif(self.searchAlgorithm=='bidirectional'):
            while(self.found==None):
                self.bidirectional()
            self.print_node(self.found)
        elif(self.searchAlgorithm=='A_star'):
            while(self.found==None):
                self.A_star()
            self.print_node(self.found)


#-------for printing the route found
    def print_node(self,node_list):
        for n in node_list:
            if n.dir!=None:
                print(n.dir,end=' ')


    def heuristic(self,board):
        difference=0
        for i in range(1,9):
            num=str(i)
            x_final,y_final=np.where(self.final_state==num)
            x_board,y_board=np.where(board==num)
            difference+=abs((x_board[0]-x_final[0]))+abs((y_board[0]-y_final[0]))
        
        
        return difference

            

    def A_star(self):
        self.moveLog.sort(key=lambda x: x[len(x)-1].score)
        # for i in self.moveLog:
        #     print(i[len(i)-1].score,end=" ")
        # print('\n')   
        temp=self.moveLog.pop(0)
        temp_node=temp[len(temp)-1]
        temp_board=temp_node.state[0].copy()
        temp_pointer=temp_node.state[1].copy()
        self.board=temp_board.copy()
        equal = temp_board==self.final_state
        if(equal.all()==True):
            self.found=temp
        else:

            row=temp_pointer[0]
            col=temp_pointer[1]

            if(row-1>=0):
                up=copy.deepcopy(temp)
                new_node=Node([self.swap(temp_board.copy(),row,col,row-1,col),[row-1,col]],'Up')
                new_node.g=temp_node.g+1
                
                new_node.score=new_node.g+self.heuristic(new_node.state[0])
                up.append(new_node)
                self.moveLog.append(up)
            if(col+1<3):
                right=copy.deepcopy(temp)
                new_node=Node([self.swap(temp_board.copy(),row,col,row,col+1),[row,col+1]],'Right')
                new_node.g=temp_node.g+1
                
                new_node.score=new_node.g+self.heuristic(new_node.state[0])
                right.append(new_node)
                self.moveLog.append(right)
            if(row+1<3):
                down=copy.deepcopy(temp)
                new_node=Node([self.swap(temp_board.copy(),row,col,row+1,col),[row+1,col]],'Down')
                new_node.g=temp_node.g+1
                
                new_node.score=new_node.g+self.heuristic(new_node.state[0])
                down.append(new_node)
                self.moveLog.append(down)
            if(col-1>=0):
                left=copy.deepcopy(temp)
                new_node=Node([self.swap(temp_board.copy(),row,col,row,col-1),[row,col-1]],'Left')
                new_node.g=temp_node.g+1
                
                new_node.score=new_node.g+self.heuristic(new_node.state[0])
                left.append(new_node)
                self.moveLog.append(left)







    def bfs(self):
        temp=self.moveLog.pop(0)
        temp_node=temp[len(temp)-1]
        temp_board=temp_node.state[0].copy()
        temp_pointer=temp_node.state[1].copy()
        self.board=temp_board.copy()
        print(temp_board)
        equal = temp_board==self.final_state
        if(equal.all()==True):
            self.found=temp
        else:

            row=temp_pointer[0]
            col=temp_pointer[1]

            if(row-1>=0):
                up=temp.copy()
                up.append(Node([self.swap(temp_board.copy(),row,col,row-1,col),[row-1,col]],'Up'))
                self.moveLog.append(up)
            if(col+1<3):
                right=temp.copy()
                right.append(Node([self.swap(temp_board.copy(),row,col,row,col+1),[row,col+1]],'Right'))
                self.moveLog.append(right)
            if(row+1<3):
                down=temp.copy()
                down.append(Node([self.swap(temp_board.copy(),row,col,row+1,col),[row+1,col]],'Down'))
                self.moveLog.append(down)
            if(col-1>=0):
                left=temp.copy()
                left.append(Node([self.swap(temp_board.copy(),row,col,row,col-1),[row,col-1]],'Left'))
                self.moveLog.append(left)



    def swap(self,newboard,oldRow,oldCol,newRow,newCol):

        temp=newboard[newRow][newCol]
        newboard[oldRow][oldCol]=temp
        newboard[newRow][newCol]='--'
        
        # print(newboard)
        # print('\n\n\n')

        return newboard






    def ids(self):
        
        for limit in range(self.max_depth):
            self.moveLog=[]
            self.moveLog.append([Node([self.src[:],self.pointer[:]],None)])
            src=self.moveLog.pop(0)
            if self.dls(src.copy(),limit+1)==True:
                return
    

    def dls(self,src, limit):
        temp_node=src[len(src)-1]
        temp_board=temp_node.state[0].copy()
        temp_pointer=temp_node.state[1].copy()
        # print(temp_board)
        with boardLock:
            self.board=temp_board.copy()
        equal = temp_board==self.final_state
        if(equal.all()==True):
            self.found=src
            return True
        
        elif(limit <=0):
            return False
        else:
            row=temp_pointer[0]
            col=temp_pointer[1]

            if(row-1>=0):
                up=src.copy()
                up.append(Node([self.swap(temp_board.copy(),row,col,row-1,col),[row-1,col]],'Up'))
            
                self.moveLog.append(up)
                temp_src=self.moveLog.pop(0)
                if self.dls(temp_src.copy(),limit-1)==True:
                    return True
            if(col+1<3):
                right=src.copy()
                right.append(Node([self.swap(temp_board.copy(),row,col,row,col+1),[row,col+1]],'Right'))
                self.moveLog.append(right)

                temp_src=self.moveLog.pop(0)
                if self.dls(temp_src.copy(),limit-1)==True:
                    return True

            if(row+1<3):
                down=src.copy()
                down.append(Node([self.swap(temp_board.copy(),row,col,row+1,col),[row+1,col]],'Down'))
                self.moveLog.append(down)

                temp_src=self.moveLog.pop(0)
                if self.dls(temp_src.copy(),limit-1)==True:
                    return True

            if(col-1>=0):
                left=src.copy()
                left.append(Node([self.swap(temp_board.copy(),row,col,row,col-1),[row,col-1]],'Left'))
                self.moveLog.append(left)

                temp_src=self.moveLog.pop(0)
                if self.dls(temp_src.copy(),limit-1)==True:
                    return True

        return False


    def bidirectional(self):
        forward_temp=self.forward_moveLog.pop(0)
        forward_temp_node=forward_temp[len(forward_temp)-1]
        forward_temp_board=forward_temp_node.state[0].copy()
        forward_temp_pointer=forward_temp_node.state[1].copy()
        self.board=forward_temp_board.copy()

        # time.sleep(0.25)
        backward_temp=self.backward_moveLog.pop(0)
        backward_temp_node=backward_temp[len(backward_temp)-1]
        backward_temp_board=backward_temp_node.state[0].copy()
        backward_temp_pointer=backward_temp_node.state[1].copy()
        self.board=backward_temp_board.copy()

        equal = forward_temp_board==backward_temp_board
        equal_forward = forward_temp_board==self.final_state
        equal_backward = backward_temp_board==self.src
        if(equal.all()==True):
            self.found=forward_temp+backward_temp[::-1]
        elif(equal_forward.all()==True):
            self.found=forward_temp
        elif(equal_backward.all()==True):
            self.found=backward_temp[::-1]
        
        else:
            forward_thread=threading.Thread(target=self.forward,args=(forward_temp,forward_temp_board.copy(),forward_temp_pointer.copy(),))
            backward_thread=threading.Thread(target=self.backward,args=(backward_temp,backward_temp_board.copy(),backward_temp_pointer.copy(),))
            forward_thread.start()
            backward_thread.start()

            forward_thread.join()
            backward_thread.join()


        
    def forward(self,temp,temp_board,temp_pointer):
        row=temp_pointer[0]
        col=temp_pointer[1]

        if(row-1>=0):
            up=temp.copy()
            up.append(Node([self.swap(temp_board.copy(),row,col,row-1,col),[row-1,col]],'Up'))
            self.forward_moveLog.append(up)
        if(col+1<3):
            right=temp.copy()
            right.append(Node([self.swap(temp_board.copy(),row,col,row,col+1),[row,col+1]],'Right'))
            self.forward_moveLog.append(right)
        if(row+1<3):
            down=temp.copy()
            down.append(Node([self.swap(temp_board.copy(),row,col,row+1,col),[row+1,col]],'Down'))
            self.forward_moveLog.append(down)
        if(col-1>=0):
            left=temp.copy()
            left.append(Node([self.swap(temp_board.copy(),row,col,row,col-1),[row,col-1]],'Left'))
            self.forward_moveLog.append(left)



    def backward(self,temp,temp_board,temp_pointer):
        row=temp_pointer[0]
        col=temp_pointer[1]

        if(row-1>=0):
            up=temp.copy()
            up.append(Node([self.swap(temp_board.copy(),row,col,row-1,col),[row-1,col]],'Up'))
            self.backward_moveLog.append(up)
        if(col+1<3):
            right=temp.copy()
            right.append(Node([self.swap(temp_board.copy(),row,col,row,col+1),[row,col+1]],'Right'))
            self.backward_moveLog.append(right)
        if(row+1<3):
            down=temp.copy()
            down.append(Node([self.swap(temp_board.copy(),row,col,row+1,col),[row+1,col]],'Down'))
            self.backward_moveLog.append(down)
        if(col-1>=0):
            left=temp.copy()
            left.append(Node([self.swap(temp_board.copy(),row,col,row,col-1),[row,col-1]],'Left'))
            self.backward_moveLog.append(left)





    def check(self,arr1,arr2):
        existing=arr1==arr2
        return existing.all()



    def makeMove(self,move):
        if(self.board[move.endRow][move.endCol]=='--'):
            if((move.endRow==move.startRow+1 and move.startCol==move.endCol) or (move.endRow==move.startRow and move.startCol==move.endCol+1) or (move.endRow==move.startRow-1 and move.startCol==move.endCol) or (move.endRow==move.startRow and move.startCol==move.endCol-1)):
                self.board[move.startRow][move.startCol]='--'
                self.board[move.endRow][move.endCol]=move.pieceMoved
                self.moveLog.append(move)
                self.whitToMove= not self.whitToMove

    def randomList(self):
        np.random.shuffle(self.board)

    
        


class Move():
    ranksToRows={'1':7 , '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}
    rowsToRanks={v:k for k,v in ranksToRows.items()}

    filesToCols={'a':0, 'b':1, 'c':2,'d':3, 'e':4, 'f':5, 'g':6, 'h':7}
    colsToFiles={v:k for k,v in filesToCols.items()}

    def __init__(self,startSq,endSq,board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved=board[self.startRow][self.startCol]
        self.pieceCaptured=board[self.endRow][self.endCol]
    
    def getChessNotation(self):
        return self.getChessRank(self.startRow,self.startCol)+self.getChessRank(self.endRow,self.endCol)

    def getChessRank(self,r,c):
        return self.colsToFiles[c]+self.rowsToRanks[r]


