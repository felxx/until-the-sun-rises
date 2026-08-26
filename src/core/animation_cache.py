import pygame


class AnimationCache:

    def __init__(self, frames):
        self.frames_dict = {i: frame for i, frame in enumerate(frames)}
        self.frame_count = len(self.frames_dict)
        self.rotation_cache = {i: {} for i in range(self.frame_count)}

    def get_frame(self, frame_index, angle=0):
        approx_angle = int(angle // 5) * 5
        if approx_angle not in self.rotation_cache[frame_index]:
            base_image = self.frames_dict[frame_index]
            rotated = pygame.transform.rotate(base_image, approx_angle)
            self.rotation_cache[frame_index][approx_angle] = rotated
        return self.rotation_cache[frame_index][approx_angle]