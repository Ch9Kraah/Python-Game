#!/usr/bin/env python3
import sys
import pygame

# === CONFIG ===
BOARD_SIZE = 4
LIGHT_COLOR = (235, 235, 208)
DARK_COLOR = (119, 148, 85)
HIGHLIGHT_COLOR = (255, 255, 0, 80)
WINDOW_TITLE = "Scacchiera con Menu"
INITIAL_SIZE = (800, 640)
FPS = 60


# === CLASSE CELLA SCACCHIERA ===
class Square:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.highlight = False

    def draw(self, surface, square_w, square_h):
        rect = pygame.Rect(
            self.col * square_w,
            self.row * square_h,
            square_w,
            square_h
        )
        pygame.draw.rect(surface, self.color, rect)

        if self.highlight:
            highlight_surf = pygame.Surface((square_w, square_h), pygame.SRCALPHA)
            highlight_surf.fill(HIGHLIGHT_COLOR)
            surface.blit(highlight_surf, rect.topleft)


# === CREAZIONE SCACCHIERA ===
def create_board():
    board = []
    for r in range(BOARD_SIZE):
        row = []
        for c in range(BOARD_SIZE):
            color = LIGHT_COLOR if (r + c) % 2 == 0 else DARK_COLOR
            row.append(Square(r, c, color))
        board.append(row)
    return board


# === DISEGNO SCACCHIERA ===
def draw_board(surface, board, width, height, board_width_ratio=0.75):
    board_width = int(width * board_width_ratio)
    square_w = board_width // BOARD_SIZE
    square_h = height // BOARD_SIZE
    for row in board:
        for square in row:
            square.draw(surface, square_w, square_h)


# === AREA COMANDI A DESTRA ===
def draw_comandi(surface, width, height, board_width_ratio=0.75):
    board_width = int(width * board_width_ratio)
    command_area_x = board_width
    command_area_width = width - board_width
    command_height = height // 4

    rect_color = (180, 180, 180)
    border_color = (60, 60, 60)

    for i in range(4):
        y = i * command_height
        rect = pygame.Rect(command_area_x, y, command_area_width, command_height)
        pygame.draw.rect(surface, rect_color, rect)
        pygame.draw.rect(surface, border_color, rect, 3)


# === GESTIONE HOVER SCACCHIERA ===
def handle_mouse(board, mouse_pos, width, height, board_width_ratio=0.75):
    board_width = int(width * board_width_ratio)
    square_w = board_width // BOARD_SIZE
    square_h = height // BOARD_SIZE

    for row in board:
        for square in row:
            square.highlight = False

    if mouse_pos:
        mx, my = mouse_pos
        if mx < board_width:  # evita area comandi
            col = mx // square_w
            row = my // square_h
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                board[row][col].highlight = True


# === MENU INIZIALE ===
def draw_menu(screen, width, height, font, mouse_pos):
    screen.fill((255, 255, 255))

    base_color = (160, 32, 240)
    hover_color = (200, 100, 255)
    text_color = (255, 255, 255)
    rect_width = 200
    rect_height = 80
    spacing = 20

    center_x = width // 2
    center_y = height // 2

    total_height = 3 * rect_height + 2 * spacing
    start_y = center_y - total_height // 2

    rects = []
    texts = ["Start", "Opzioni", "Esci"]

    for i in range(3):
        rect = pygame.Rect(0, 0, rect_width, rect_height)
        rect.centerx = center_x
        rect.y = start_y + i * (rect_height + spacing)

        # Hover effect
        color = hover_color if rect.collidepoint(mouse_pos) else base_color

        # Rettangolo + bordo
        pygame.draw.rect(screen, color, rect, border_radius=10)
        pygame.draw.rect(screen, (80, 0, 150), rect, 2, border_radius=10)

        # Testo centrato
        text_surf = font.render(texts[i], True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

        rects.append(rect)

    return rects

def draw_giocatori(screen, width, height, font, mouse_pos):
    screen.fill((255, 255, 255))

    base_color = (160, 32, 240)
    hover_color = (200, 100, 255)
    text_color = (255, 255, 255)
    rect_width = 200
    rect_height = 80
    spacing = 20

    center_x = width // 2
    center_y = height // 2

    total_height = 3 * rect_height + 2 * spacing
    start_y = center_y - total_height // 2
    rects = []
    texts=["In quanti volete giocare", "1","2","3","4"]
    j=1 # serve per moltiplicare la y della posizione 3/4 e allinearli

    for i in range(5):
        if i == 0:
            rect = pygame.Rect(0, 0, rect_width*3, rect_height)
            rect.centerx = center_x
            rect.y = start_y + i * (rect_height + spacing)

            # Hover effect
            color = hover_color if rect.collidepoint(mouse_pos) else base_color

            # Rettangolo + bordo
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, (80, 0, 150), rect, 2, border_radius=10)

            # Testo centrato
            text_surf = font.render(texts[i], True, text_color)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

            rects.append(rect)
        elif i>0 and i<=2:
            rect = pygame.Rect(0, 0, rect_width, rect_height)
            rect.centerx = (center_x*2)//3
            rect.y = start_y + i * (rect_height + spacing)

            # Hover effect
            color = hover_color if rect.collidepoint(mouse_pos) else base_color

            # Rettangolo + bordo
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, (80, 0, 150), rect, 2, border_radius=10)

            # Testo centrato
            text_surf = font.render(texts[i], True, text_color)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

            rects.append(rect)
        else:
            
            rect = pygame.Rect(0, 0, rect_width, rect_height)
            rect.centerx = center_x+150
            rect.y = start_y + j * (rect_height + spacing)

            # Hover effect
            color = hover_color if rect.collidepoint(mouse_pos) else base_color

            # Rettangolo + bordo
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, (80, 0, 150), rect, 2, border_radius=10)

            # Testo centrato
            text_surf = font.render(texts[i], True, text_color)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)
            j+=1
            

            rects.append(rect)

    return rects


def draw_scelta_giocatori(screen, width, height, font,font1, mouse_pos):
    screen.fill((255, 255, 255))

    base_color = (160, 32, 240)
    hover_color = (200, 100, 255)
    text_color = (255, 255, 255)
    rect_width = 200
    rect_height = 80
    spacing = 20

    center_x = width // 4
    center_y = height // 4

    total_height = 3 * rect_height + 2 * spacing
    start_y = center_y - total_height // 2
    rects = []
    texts=["Principe","Punti Vita -> 3", "Punti vita massimi -> 3", "Dadi attacco -> 2", "Dadi difesa -> 1", "Dopplegenger","Punti Vita -> 3", "Punti vita massimi -> 3", "Dadi attacco -> 2", "Dadi difesa -> 1"]
    for i in range(4):
        if i == 0:
            rect = pygame.Rect(0, 0, rect_width*1.5, rect_height)
            rect.centerx = center_x
            rect.y = start_y + i * (rect_height + spacing)

            # Hover effect
            color = hover_color if rect.collidepoint(mouse_pos) else base_color

            # Rettangolo + bordo
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, (80, 0, 150), rect, 2, border_radius=10)

            # Testo centrato
            text_surf = font.render(texts[i], True, text_color)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

            rects.append(rect)
        elif i==1:
            rect = pygame.Rect(0, 0, rect_width+75, rect_height*4)
            rect.centerx = center_x
            rect.y = start_y + i * (rect_height)

            # Hover effect
            color = hover_color if rect.collidepoint(mouse_pos) else base_color

            # Rettangolo + bordo
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, (80, 0, 150), rect, 2, border_radius=10)

            # Testo centrato
            for j in range(4):
                text_surf = font1.render(texts[j+1], True, text_color)
                padding = 15  # spazio dal bordo sinistro del rettangolo
                text_rect = text_surf.get_rect(topleft=(rect.x + padding,
                                        rect.y + j * rect_height + (rect_height - text_surf.get_height()) / 2))

                screen.blit(text_surf, text_rect)


            rects.append(rect)
        elif i==2:
            rect = pygame.Rect(0, 0, rect_width*1.5, rect_height)
            rect.centerx = center_x*3
            rect.y = start_y + 0 * (rect_height + spacing)

            # Hover effect
            color = hover_color if rect.collidepoint(mouse_pos) else base_color

            # Rettangolo + bordo
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, (80, 0, 150), rect, 2, border_radius=10)

            # Testo centrato
            text_surf = font.render(texts[i+3], True, text_color)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

            rects.append(rect)
        else:
            rect = pygame.Rect(0, 0, rect_width+75, rect_height*4)
            rect.centerx = center_x*3
            rect.y = start_y + 1 * (rect_height)

            # Hover effect
            color = hover_color if rect.collidepoint(mouse_pos) else base_color

            # Rettangolo + bordo
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, (80, 0, 150), rect, 2, border_radius=10)

            # Testo centrato
            for j in range(4):
                text_surf = font1.render(texts[j+6], True, text_color)
                padding = 15  # spazio dal bordo sinistro del rettangolo
                text_rect = text_surf.get_rect(topleft=(rect.x + padding,
                                        rect.y + j * rect_height + (rect_height - text_surf.get_height()) / 2))

                screen.blit(text_surf, text_rect)



    
    return rects





# === MAIN LOOP ===
def main():
    pygame.init()
    screen = pygame.display.set_mode(INITIAL_SIZE, pygame.RESIZABLE)
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    font1= pygame.font.SysFont(None, 20)

    board = create_board()

    #logica selezione
    show_menu = True
    menu_rects = []

    giocatori_settati=False
    menu_numero_giocatori=[]
    numero_dei_giocatori= None

    scelta_ruoli=False
    menu_scelta_ruoli=[]


    running = True
    while running:
        width, height = screen.get_size()
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if show_menu:
                    for rect in menu_rects:
                        if rect.collidepoint(event.pos):
                            print("Hai cliccato un rettangolo del menu!")
                            if menu_rects.index(rect) == 0:  # Start
                                show_menu = False
                            elif menu_rects.index(rect) == 2:  # Esci
                                running = False
                elif not giocatori_settati:
                    for rect in menu_numero_giocatori:
                        if rect.collidepoint(event.pos):
                            print("Hai scelto il numero di giocatori")
                            if menu_numero_giocatori.index(rect)>0 and menu_numero_giocatori.index(rect)<5:
                                giocatori_settati=True
                                numero_dei_giocatori= menu_numero_giocatori.index(rect)
                                print(numero_dei_giocatori)
                elif not scelta_ruoli:
                    for rect in menu_scelta_ruoli:
                        if rect.collidepoint(event.pos):
                            print("hai scelto il ruolo")
                            scelta_ruoli=True
                            


                    

        if show_menu:
            # Mostra menu principale
            menu_rects = draw_menu(screen, width, height, font, mouse_pos)
        elif not giocatori_settati:
            menu_numero_giocatori= draw_giocatori(screen, width, height, font, mouse_pos)  
        elif not scelta_ruoli:
            menu_scelta_ruoli=draw_scelta_giocatori(screen, width,height, font,font1, mouse_pos)          
        else:
            # Mostra scacchiera + comandi
            handle_mouse(board, mouse_pos, width, height)
            draw_board(screen, board, width, height)
            draw_comandi(screen, width, height)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


# === AVVIO PROGRAMMA ===
if __name__ == "__main__":
    main()
