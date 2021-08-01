'''
 This is our main driver, it is responsible for handling the user inputs and displaying the states of game
'''

import numpy as np
import pygame
import puzzleEngine
import time

width = height = 512
demension = 3
SQ_size = height // demension
max_fps = 15
img = {}


def loadImage():
    global img
    pieces = np.array(['1', '2', '3', '4', '5', '6','7', '8'])

    for piece in pieces:
        img[piece] = pygame.transform.scale(pygame.image.load('images/'+piece+'.png'), (SQ_size, SQ_size))
        # We can access to the images with img dictionary


def main():
    pygame.init()
    screen=pygame.display.set_mode((width,height))
    pygame.display.set_caption('8Puzzle')
    clock=pygame.time.Clock()
    screen.fill(pygame.Color("#F2D8B7"))
    gs=puzzleEngine.GameState()
    loadImage()
    sqSelected=()
    playerClicks=[]
    running=True
    gs.start()
    while running:
        
        for e in pygame.event.get():
            if (e.type == pygame.QUIT):
                running=False
            elif (e.type==pygame.MOUSEBUTTONDOWN):
                location=pygame.mouse.get_pos()
                col=location[0]// SQ_size
                row=location[1]// SQ_size

                print(row, col)
                if (sqSelected==(row,col)):
                    sqSelected=()
                    playerClicks=[]
                else:
                    sqSelected=(row,col)
                    playerClicks.append(sqSelected)
                if (len(playerClicks)==2):
                    move=puzzleEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                    # print(move.getChessNotation())
                    gs.makeMove(move)
                    sqSelected=()
                    playerClicks=[]

        # #BFS Searach
        # if(gs.found==None):
        #     gs.bfs()
        #     # time.sleep(1.5)
        # else:
        #     return gs.found

        if(gs.found!=None):
            gs.join()
 

        draw_GameState(screen,gs)
        clock.tick(max_fps)
        # gs.randomize()
        # time.sleep(.5)
        
        pygame.display.flip()
    # print(gs.found)

def draw_GameState(screen,gs):
    draw_board(screen)
    draw_piece(screen,gs.board)

def draw_board(screen):
    Colors=np.array([pygame.Color("#ffffff"),pygame.Color("#ffffff")])

    for i in range(demension):
        for j in range(demension):
            color=Colors[(i+j)%2]
            pygame.draw.rect(screen,color,pygame.Rect(j*SQ_size,i*SQ_size,SQ_size,SQ_size))


def draw_piece(screen,board):
    for i in range(demension):
        for j in range(demension):
            piece =board[i][j]
            if piece!='--':
                screen.blit(img[piece],pygame.Rect(j*SQ_size,i*SQ_size,SQ_size,SQ_size))

if __name__ == '__main__':
    main()