class AnimationSet:
    def __init__(self):
        self.animations = {}
        self.current_state = None

    def add_animation(self, state_name, animation):
        self.animations[state_name] = animation
        if self.current_state is None:
            self.current_state = state_name

    def set_state(self, state_name):
        if state_name in self.animations and self.current_state != state_name:
            self.current_state = state_name
            self.animations[self.current_state].current_frame = 0
            self.animations[self.current_state].current_time = 0.0
            self.animations[self.current_state].is_finished = False

    def update_and_get_image(self, dt, angle=0, is_playing=True):
        if self.current_state is None:
            return None
            
        current_anim = self.animations[self.current_state]
        current_anim.update(dt, is_playing)
        return current_anim.get_image(angle)