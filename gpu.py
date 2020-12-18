import sys
import pygame
from pygame import gfxdraw

class Gpu:
    def start(self):
        self.base_size = (64, 64)
        self.scale = 8
        self.size = (
            self.base_size[0] * self.scale,
            self.base_size[1] * self.scale
        )

        pygame.init()

        # The screen displayed to the user. Scaled up to look nice.
        self.screen = pygame.display.set_mode(self.size)

        # The logical screen that the program interacts with.
        self.buf = pygame.surface.Surface(self.base_size)

        # Coordinates to draw
        self.x, self.y = 0, 0

    def quit(self):
        pygame.display.quit()

    def update(self):
        '''Return value: whether the window got a signal to quit (e.g. Alt+F4)'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        # Draw to the buf, scale it up, then blit it to the screen
        scaled = pygame.transform.scale(self.buf, self.size)
        self.screen.blit(scaled, (0, 0))
        pygame.display.flip()
        return False

    def set_x(self, i):
        self.x = i

    def set_y(self, i):
        self.y = i

    def draw(self, color):
        # Color is a bitmap: RRGGBB

        mask = 0b11
        b = color & mask

        color = color >> 2
        g = color & mask

        color = color >> 2
        r = color & mask

        def scale(x):
            return {
                0b00: 0x00,
                0b01: 0x55,
                0b10: 0xaa,
                0b11: 0xff,
            }[x]

        b = scale(b)
        g = scale(g)
        r = scale(r)

        gfxdraw.pixel(
            self.buf,
            self.x, self.y,
            (r, g, b)
        )


if __name__ == '__main__':
    gpu = Gpu()
    gpu.start()
    gpu.buf.fill((100, 100, 200))

    gpu.set_x(32)
    gpu.set_y(32)
    gpu.draw(0b110000)

    gpu.set_x(32)
    gpu.set_y(33)
    gpu.draw(0b001100)

    gpu.set_x(33)
    gpu.set_y(32)
    gpu.draw(0b000011)

    gpu.set_x(33)
    gpu.set_y(33)
    gpu.draw(0b110011)

    while True:
        gpu.update()
