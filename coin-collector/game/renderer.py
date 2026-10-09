"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (35, 45, 35)
COLOR_PLAYER = (80, 180, 255)
COLOR_TEXT = (255, 255, 255)
COLOR_COIN_OUTLINE = (20, 20, 20)
COLOR_OBSTACLE = (210, 60, 60)


def draw_scene(surface, player, coins, obstacles=(), player_visible=True):
    surface.fill(COLOR_BG)
    for obstacle in obstacles:
        pygame.draw.rect(surface, COLOR_OBSTACLE, obstacle.get_rect(), border_radius=6)
    for coin in coins:
        center = (int(coin.x), int(coin.y))
        pygame.draw.circle(surface, coin.color, center, coin.radius)
        pygame.draw.circle(surface, COLOR_COIN_OUTLINE, center, coin.radius, width=2)
    if player_visible:
        pygame.draw.rect(surface, COLOR_PLAYER, player.get_rect(), border_radius=4)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surf = font.render(text, True, color)
    # Dark translucent box so the text stays readable over obstacles.
    box = pygame.Surface((surf.get_width() + 8, surf.get_height() + 2), pygame.SRCALPHA)
    box.fill((0, 0, 0, 150))
    surface.blit(box, (pos[0] - 4, pos[1] - 1))
    surface.blit(surf, pos)


def draw_banner(surface, font, text):
    # Dim the whole scene so the banner reads clearly on top of it.
    shade = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    shade.fill((0, 0, 0, 170))
    surface.blit(shade, (0, 0))
    surf = font.render(text, True, (255, 220, 80))
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    pygame.draw.rect(surface, (20, 20, 20), rect.inflate(32, 20), border_radius=8)
    pygame.draw.rect(surface, (255, 220, 80), rect.inflate(32, 20), width=2, border_radius=8)
    surface.blit(surf, rect)


def draw_legend(surface, font, coin_types):
    """Top-right key: a colored dot and point value for each coin type."""
    labels = [(font.render(f"{kind} = {value}", True, COLOR_TEXT), color)
              for kind, (value, color) in coin_types.items()]
    x = surface.get_width() - max(label.get_width() for label, _ in labels) - 10
    y = 10
    for label, color in labels:
        pygame.draw.circle(surface, color, (x - 14, y + label.get_height() // 2), 7)
        surface.blit(label, (x, y))
        y += label.get_height() + 4
