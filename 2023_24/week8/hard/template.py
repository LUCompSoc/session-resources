from lib import Action, Entity, Wall, main


def handle_ai(self: Entity, walls: list[Wall], opponents: list[Entity]) -> Action:
    return Action.SHOOT


if __name__ == "__main__":
    exit(main(handle_ai))
