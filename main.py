import sys
import pygame as pg
import requests


class Map:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Map')
        self.size = self.width, self.height = 600, 450
        self.screen = pg.display.set_mode(self.size)
        self.display = pg.display
        self.screen.fill('black')
        self.fps = 100
        self.x, self.y = 50, 50
        self.z = 5
        self.clock = pg.time.Clock()
        self.requests()
        self.run()
        pg.quit()

    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_PAGEDOWN and self.z > 0:
                        self.z -= 1
                        self.requests()
                    if event.key == pg.K_PAGEUP and self.z < 22:
                        self.z += 1
                        self.requests()
            self.draw()
            self.clock.tick(self.fps)
            self.display.flip()

    def draw(self):
        self.screen.blit(pg.image.load('map.png'), (0, 0))

    def requests(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.x},{self.y}&z={str(self.z)}&l=map"
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)


if __name__ == '__main__':
    game = Map()
    sys.exit()
    