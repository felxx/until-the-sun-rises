from src.core.animation_cache import AnimationCache


class Animation:
    def __init__(self, anim_data: AnimationCache, fps=12, loop=True):
        self.data = anim_data
        self.fps = fps
        self.frame_duration = 1.0 / fps if fps > 0 else 0
        self.current_time = 0.0
        self.current_frame = 0
        self.loop = loop
        self.is_finished = False

    def update(self, dt, is_playing=True):
        if self.data.frame_count <= 1 or not is_playing or self.frame_duration == 0:
            return

        self.current_time += dt
        if self.current_time >= self.frame_duration:
            frames_to_advance = int(self.current_time / self.frame_duration)
            self.current_time -= frames_to_advance * self.frame_duration

            if not self.loop and self.current_frame + frames_to_advance >= self.data.frame_count - 1:
                self.current_frame = self.data.frame_count - 1
                self.is_finished = True
            else:
                self.current_frame = (self.current_frame + frames_to_advance) % self.data.frame_count

    def get_image(self, angle=0):
        return self.data.get_frame(self.current_frame, angle)