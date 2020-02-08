# piece encoding

#  1000  8  white
# 10000 16  black

# 001  1  pawn +
# 010  2  pawn -
# 011  3  king
# 100  4  knight
# 101  5  bishop
# 110  6  rook
# 111  7  queen

# 1000 | 001 = 1001   9  white pawn
# 1000 | 011 = 1011  11  white king
# 1000 | 100 = 1100  12  white knight
# 1000 | 101 = 1101  13  white bishop
# 1000 | 110 = 1110  14  white rook
# 1000 | 111 = 1111  15  white queen

# 10000 | 010 = 10010  18 black pawn
# 10000 | 011 = 10011  19 black king
# 10000 | 100 = 10100  20 black knight
# 10000 | 101 = 10101  21 black bishop
# 10000 | 110 = 10110  22 black rook
# 10000 | 111 = 10111  23 black queen

# 0x88 board representation + piece square scores
board = [
	22, 20, 21, 23, 19, 21, 20, 22,  0, 0, 0, 0, 0, 0, 0, 0,
    18, 18, 18, 18, 18, 18, 18, 18,  0, 0, 0, 0, 0, 0, 0, 0,
     0,  0,  0,  0,  0,  0,  0,  0,  0, 0, 0, 0, 0, 0, 0, 0,
     0,  0,  0,  0,  0,  0,  0,  0,  0, 0, 0, 0, 0, 0, 0, 0,
     0,  0,  0,  0,  0,  0,  0,  0,  0, 0, 0, 0, 0, 0, 0, 0,
     0,  0,  0,  0,  0,  0,  0,  0,  0, 0, 0, 0, 0, 0, 0, 0,
     9,  9,  9,  9,  9,  9,  9,  9,  0, 0, 0, 0, 0, 0, 0, 0,
    14, 12, 13, 15, 11, 13, 12, 14,  0, 0, 0, 0, 0, 0, 0, 0
]

notation = [
	'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',   'i8', 'j8', 'k8', 'l8', 'm8', 'n8', 'o8', 'p8',
    'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',   'i7', 'j7', 'k7', 'l7', 'm7', 'n7', 'o7', 'p7',
    'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',   'i6', 'j6', 'k6', 'l6', 'm6', 'n6', 'o6', 'p6',
    'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',   'i5', 'j5', 'k5', 'l5', 'm5', 'n5', 'o5', 'p5',
    'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',   'i4', 'j4', 'k4', 'l4', 'm4', 'n4', 'o4', 'p4',
    'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',   'i3', 'j3', 'k3', 'l3', 'm3', 'n3', 'o3', 'p3',
    'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',   'i2', 'j2', 'k2', 'l2', 'm2', 'n2', 'o2', 'p2',
    'a2', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1',   'i1', 'j1', 'k1', 'l1', 'm1', 'n1', 'o1', 'p1',
]

move_offsets = [
   15,  16,  17,   0,                           # black pawns
  -15, -16, -17,   0,                           # white pawns
    1,  16,  -1, -16,   0,                      # rooks
    1,  16,  -1, -16,  15, -15, 17, -17,  0,    # queens, kings and bishops
   14, -14,  18, -18,  31, -31, 33, -33,  0,    # knights
    3,  -1,  12,  21,  16,   7, 12              # starting indexes for each piece type in order:
                                                #     white pawns, black pawns, kings, knights, bishops, rooks, queens
]

# 1001 & 1111 = 1001  9  white pawn
# 1110 & 1111 = 1110 14  white rook
pieces = '.-pknbrq-P-KNBRQ'

def print_board():
    index = 0
    while index < 128:
        # sq is on board
        if (index & 0x88) == 0:
            piece = board[index]
            print(pieces[piece & 15], end=' ')
            index += 1
        # sq is offboard
        else:
            print()
            index += 8
            
def search(side):
    # move generator
    index = 0
    
    # loop over board squares
    while index < 128:
        if (index & 0x88) == 0:
            piece = board[index]
            
            if piece & side:
                piece_type = piece & 7
                directions = move_offsets[piece_type + 30]
                directions += 1
                
                # loop over move offsets
                while move_offsets[directions]:
                    step_vector = move_offsets[directions]
                    directions += 1
                    
                    source_square = index
                    target_square = source_square
                    
                    captured_piece = 0
                    
                    # loop over slider ray
                    while captured_piece == 0:
                        target_square += step_vector
                        captured_square = target_square
                        
                        if target_square & 0x88:
                            break
                        
                        captured_piece = board[captured_square]
                        
                        if captured_piece & side:
                            break
                        
                        # pawn moves
                        if (piece_type < 3 and (not (step_vector & 7)) != (not captured_piece)):
                            break

                        
                        print(notation[source_square], notation[target_square], sep='')
                        
                        # fake capture for leapers, e.g. pawns, knights, kings
                        captured_piece += (piece_type < 5)
                        
                        # unfake capture for double pawn move
                        if (piece_type < 3 and (6 * side + (target_square & 0x70) == 0x80)):
                            captured_piece -= 1
                
        index += 1

        
white = 8    #  1000
black = 16   # 10000

search(white)
    
    
    
    
    
