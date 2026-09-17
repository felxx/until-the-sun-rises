import cv2
import numpy as np
import pygame

from src.core.constants import BACKGROUND_FALLBACK


class VideoPlayer:
    def __init__(self, path, target_width, target_height, blur_strength=8):
        self.target_width = target_width
        self.target_height = target_height
        self.blur_strength = max(1, blur_strength)

        self.current_time = 0.0
        self._fallback_surface = pygame.Surface((target_width, target_height))
        self._fallback_surface.fill(BACKGROUND_FALLBACK)

        self.cap = cv2.VideoCapture(path)
        self.available = self.cap.isOpened()

        if self.available:
            native_fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
            self.frame_duration = 1.0 / native_fps

            native_w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            native_h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self._compute_cover_rect(native_w, native_h)

            self._current_surface = self._fallback_surface
            self._advance_one_frame()
        else:
            self._current_surface = self._fallback_surface

    def _compute_cover_rect(self, native_w, native_h):
        scale = max(self.target_width / native_w, self.target_height / native_h)
        self._scaled_w = max(1, round(native_w * scale))
        self._scaled_h = max(1, round(native_h * scale))
        self._crop_x = (self._scaled_w - self.target_width) // 2
        self._crop_y = (self._scaled_h - self.target_height) // 2

    def update(self, dt):
        if not self.available:
            return

        self.current_time += dt
        if self.current_time >= self.frame_duration:
            steps = int(self.current_time / self.frame_duration)
            self.current_time -= steps * self.frame_duration
            for _ in range(steps):
                self._advance_one_frame()

    def _advance_one_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
            if not ret:
                return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self._scaled_w, self._scaled_h), interpolation=cv2.INTER_AREA)
        frame = frame[
            self._crop_y:self._crop_y + self.target_height,
            self._crop_x:self._crop_x + self.target_width,
        ]
        frame = np.ascontiguousarray(frame)

        surface = pygame.image.frombuffer(frame.tobytes(), (self.target_width, self.target_height), "RGB")
        self._current_surface = self._apply_blur(surface)

    def _apply_blur(self, surface):
        small_size = (
            max(1, self.target_width // self.blur_strength),
            max(1, self.target_height // self.blur_strength),
        )
        small = pygame.transform.smoothscale(surface, small_size)
        return pygame.transform.smoothscale(small, (self.target_width, self.target_height))

    def get_frame(self):
        return self._current_surface

    def release(self):
        if self.available:
            self.cap.release()
            self.available = False
