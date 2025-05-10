import pygame
from engine.field.zones import ZoneType, Side
import time

ZONE_WIDTH = 180
ZONE_HEIGHT = 120
ZONE_GAP = 5

zone_x = {
    ZoneType.DEFENSE: 0,
    ZoneType.AFTER_DEFENSE: 1,
    ZoneType.CENTER: 2,
    ZoneType.PRE_ATTACK: 3,
    ZoneType.ATTACK: 4
}

side_y = {
    Side.LEFT: 2,
    Side.CENTER: 1,
    Side.RIGHT: 0
}

class Visualizer:
    def __init__(self, context, engine, width=1000, height=400):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Football Manager Match Visualizer")
        self.clock = pygame.time.Clock()
        self.context = context
        self.engine = engine
        self.running = True
        self.last_ball_pos = None

    def zone_to_pixel(self, zone):
        x = zone_x[zone.zone_type] * (ZONE_WIDTH + ZONE_GAP) + ZONE_WIDTH // 2
        y = side_y[zone.side] * (ZONE_HEIGHT + ZONE_GAP) + ZONE_HEIGHT // 2
        return x, y

    def draw_field(self):
        self.screen.fill((34, 139, 34))  # green background
        for zt in ZoneType:
            for s in Side:
                x = zone_x[zt] * (ZONE_WIDTH + ZONE_GAP)
                y = side_y[s] * (ZONE_HEIGHT + ZONE_GAP)
                pygame.draw.rect(self.screen, (0, 100, 0), (x, y, ZONE_WIDTH, ZONE_HEIGHT), 2)

    def draw_players(self):
        for player in self.context.all_players:
            zone = self.context.zone_tracker.get_player_zone(player)
            if not zone:
                continue
            x, y = self.zone_to_pixel(zone)
            color = (255, 0, 0) if self.context.ball.holder == player else (0, 0, 255)
            pygame.draw.circle(self.screen, color, (x, y), 15)
            label = player.first_name[:2]
            self.draw_text(label, x, y - 20, 14, (255, 255, 255))

    def draw_ball_animation(self, start_pos, end_pos, steps=10):
        for step in range(1, steps + 1):
            inter_x = start_pos[0] + (end_pos[0] - start_pos[0]) * step / steps
            inter_y = start_pos[1] + (end_pos[1] - start_pos[1]) * step / steps

            self.draw_field()
            self.draw_players()
            pygame.draw.circle(self.screen, (255, 255, 0), (int(inter_x), int(inter_y)), 8)  # Ball
            pygame.display.flip()
            self.clock.tick(60)

    def draw_text(self, text, x, y, size=20, color=(255, 255, 255)):
        font = pygame.font.SysFont(None, size)
        img = font.render(text, True, color)
        rect = img.get_rect(center=(x, y))
        self.screen.blit(img, rect)

    def run(self, ticks=10):
        for _ in range(ticks):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

            # Get previous ball position
            if self.context.ball.holder:
                zone = self.context.zone_tracker.get_player_zone(self.context.ball.holder)
                if zone:
                    new_ball_pos = self.zone_to_pixel(zone)
                else:
                    new_ball_pos = self.last_ball_pos or (0, 0)
            else:
                new_ball_pos = self.last_ball_pos or (0, 0)

            self.engine.tick()

            if self.last_ball_pos and new_ball_pos != self.last_ball_pos:
                self.draw_ball_animation(self.last_ball_pos, new_ball_pos)
            else:
                self.draw_field()
                self.draw_players()
                if new_ball_pos:
                    pygame.draw.circle(self.screen, (255, 255, 0), new_ball_pos, 8)  # Ball
                pygame.display.flip()

            self.last_ball_pos = new_ball_pos
            self.clock.tick(60)
            time.sleep(1.0)

        pygame.time.wait(2000)
        pygame.quit()
