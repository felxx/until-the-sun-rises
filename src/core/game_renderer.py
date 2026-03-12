class GameRenderer:
    def __init__(self, screen):
        self.screen = screen

    def render(self, all_objects):
        visible_objects = [obj for obj in all_objects if obj.active]
        visible_objects.sort(key=lambda obj: obj.position.y)

        for obj in visible_objects:
            if obj.image and obj.rect:
                self.screen.blit(obj.image, obj.rect)