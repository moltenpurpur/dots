import pygame_textinput
import pygame
import sys

from dots.save import Saver


class EndMenu:
    def __init__(self, win, win_size):
        self.win_size = win_size
        self.win = win
        self.font = pygame.font.Font(None, 40)

    def start_end_menu(self, score):
        textinput = pygame_textinput.TextInputVisualizer()
        leaderboard = (sorted(Saver.load_leaderboard().items(),
                              key=lambda x: x[1])[::-1])
        self.win = pygame.display.set_mode((500, 500))
        name = ""
        while True:
            self.win.fill((225, 225, 225))
            events = pygame.event.get()
            textinput.update(events)
            if len(textinput.value) <= 14:
                name = textinput.value
            textinput.value = name
            for e in events:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        self.save_score(leaderboard, name, score)
                        pygame.quit()
                        sys.exit()
            self.print_leaderboard(leaderboard)

            self.win.blit(self.font.render("Write your name", 1,
                                           (0, 0, 0)),
                          (140,
                           420))
            pygame.draw.rect(self.win, (0, 0, 0), (140, 450, 210, 40), 1)
            self.win.blit(textinput.surface, (150, 450))
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            pygame.display.update()

    def print_leaderboard(self, leaderboard):
        self.win.blit(self.font.render("Leaderboard:", 1,
                                       (0, 0, 0)),
                      (50,
                       25))
        offset = 30
        ld = leaderboard
        if len(ld) > 10:
            ld = ld[0:10]

        for item in ld:
            name = str(item[0])
            score = str(item[1])
            strL = len(name)
            st = name + (15 - strL) * " " + score
            v = len(st)
            self.win.blit(self.font.render(name, 1,
                                           (0, 0, 0)),
                          (50,
                           30 + offset))
            self.win.blit(self.font.render(score, 1,
                                           (0, 0, 0)),
                          (250,
                           30 + offset))
            offset += 30

    def save_score(self, leaderboard, name, score):
        leaderboard = dict(sorted(Saver.load_leaderboard().items(),
                                  key=lambda x: x[1])[::-1])
        leaderboard[name] = int(score)
        Saver.save_leaderbiard(leaderboard)
