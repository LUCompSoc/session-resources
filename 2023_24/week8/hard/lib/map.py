from .wall import Wall

SIZE = WIDTH, HEIGHT = 720, 405

margin = 20
path_width = 30

void_width = WIDTH - 2 * (margin + path_width)


MAP = [
    Wall((margin, margin), (WIDTH - margin, margin)),
    Wall((WIDTH - margin, margin), (WIDTH - margin, HEIGHT - margin)),
    Wall((margin, HEIGHT - margin), (WIDTH - margin, HEIGHT - margin)),
    Wall(
        (margin, HEIGHT - margin),
        (WIDTH - void_width // 3 - path_width // 2, HEIGHT - margin),
    ),
    Wall(
        (WIDTH - margin - path_width, HEIGHT // 2),
        (WIDTH - margin - path_width, HEIGHT // 2 + margin),
    ),
    Wall(
        (WIDTH - margin - path_width, HEIGHT // 2 + margin + path_width),
        (WIDTH - margin - path_width, HEIGHT - margin - path_width),
    ),
    Wall(
        (margin + 2 * path_width, HEIGHT // 2 - path_width),
        (margin + 5 * path_width // 2, HEIGHT // 2 - path_width),
    ),
    Wall(
        (margin + 7 * path_width // 2, HEIGHT // 2 - path_width),
        (margin + path_width // 2 + void_width // 3, HEIGHT // 2 - path_width),
    ),
    Wall(
        (margin + 3 * path_width // 2 + void_width // 3, HEIGHT // 2 - path_width),
        (margin + 7 * path_width // 2 + void_width // 3, HEIGHT // 2 - path_width),
    ),
    Wall(
        (margin + 9 * path_width // 2 + void_width // 3, HEIGHT // 2 - path_width),
        (WIDTH - margin - 5 * path_width // 2, HEIGHT // 2 - path_width),
    ),
    Wall(
        (WIDTH - margin - 3 * path_width // 2, HEIGHT // 2 - path_width),
        (WIDTH - margin, HEIGHT // 2 - path_width),
    ),
    Wall(
        (margin + path_width, HEIGHT // 2),
        (margin + 3 * path_width // 2, HEIGHT // 2),
    ),
    Wall(
        (margin + 5 * path_width // 2, HEIGHT // 2),
        (margin + void_width // 3 - path_width // 2, HEIGHT // 2),
    ),
    Wall(
        (margin + void_width // 3 + path_width // 2, HEIGHT // 2),
        (WIDTH // 2 - path_width // 2, HEIGHT // 2),
    ),
    Wall(
        (WIDTH // 2 + path_width // 2, HEIGHT // 2),
        (WIDTH - margin - path_width, HEIGHT // 2),
    ),
    Wall(
        (margin + path_width, margin + path_width),
        (margin + path_width, HEIGHT - margin - path_width),
    ),
    Wall(
        (margin + 2 * path_width, margin),
        (margin + 2 * path_width, HEIGHT // 2 - path_width),
    ),
    Wall((margin, margin + path_width), (margin + path_width, margin + path_width)),
    Wall(
        (
            margin + 3 * path_width // 2 + void_width // 6,
            HEIGHT - margin - 3 * path_width,
        ),
        (
            margin + path_width + void_width // 3,
            HEIGHT - margin - 3 * path_width,
        ),
    ),
    Wall(
        (margin + path_width, HEIGHT - margin - 3 * path_width),
        (margin + path_width // 2 + void_width // 6, HEIGHT - margin - 3 * path_width),
    ),
    Wall(
        (margin, HEIGHT - margin - path_width),
        (margin + path_width // 2 + void_width // 6, HEIGHT - margin - path_width),
    ),
    Wall(
        (margin + 3 * path_width // 2 + void_width // 6, HEIGHT - margin - path_width),
        (WIDTH - 2 * void_width // 9 - path_width // 2, HEIGHT - margin - path_width),
    ),
    Wall(
        (WIDTH - 2 * void_width // 9 + path_width // 2, HEIGHT - margin - path_width),
        (WIDTH - margin - path_width, HEIGHT - margin - path_width),
    ),
    Wall(
        (margin + 2 * path_width + void_width // 3, margin),
        (margin + 2 * path_width + void_width // 3, HEIGHT // 2 - path_width),
    ),
    Wall(
        (margin + path_width + void_width // 3, HEIGHT // 2),
        (margin + path_width + void_width // 3, HEIGHT - margin - path_width),
    ),
    Wall(
        (margin + path_width + 2 * void_width // 3, HEIGHT // 2),
        (margin + path_width + 2 * void_width // 3, HEIGHT - margin - path_width),
    ),
]
