import sys
import pygame as pg
import requests
import math


class Map:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Map')
        self.size = self.width, self.height = 600, 600
        self.screen = pg.display.set_mode(self.size)
        self.display = pg.display

        self.fps = 100
        self.x, self.y = 50, 50
        self.format = 'map'
        self.z = 5
        self.x1, self.y1 = None, None
        self.base_font = pg.font.Font(None, 32)
        self.user_text = ''

        self.input_rect = pg.Rect(50, 475, 140, 32)
        self.color_active = pg.Color('#75c1ff')
        self.color_passive = pg.Color('#b3b3b3')
        self.color = self.color_passive

        self.ob = pg.font.Font(None, 32)
        self.ob_text = 'Схема'

        self.ob_rect = pg.Rect(220, 475, 80, 32)

        self.ob2 = pg.font.Font(None, 32)
        self.ob2_text = 'Спутник'

        self.ob2_rect = pg.Rect(310, 475, 100, 32)

        self.ob3 = pg.font.Font(None, 32)
        self.ob3_text = 'Гибрид'

        self.ob3_rect = pg.Rect(420, 475, 100, 32)

        self.ob4 = pg.font.Font(None, 32)
        self.ob4_text = 'Сброс поискового результата'

        self.ob4_rect = pg.Rect(50, 520, 140, 32)

        self.active = False
        self.clock = pg.time.Clock()
        self.requests()
        self.run()
        pg.quit()

    def writ(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.user_text = ''
                self.active = True
            if self.ob_rect.collidepoint(event.pos):
                self.format = 'map'
                print(self.search_params)
                self.requests()
            if self.ob2_rect.collidepoint(event.pos):
                self.format = 'sat'
                print(self.search_params)
                self.requests()
            if self.ob3_rect.collidepoint(event.pos):
                self.format = 'sat,skl'
                print(self.search_params)
                self.requests()
            if self.ob4_rect.collidepoint(event.pos):
                del self.search_params['pt']
                self.user_text = ''
                self.x1, self.y1 = None, None
                self.requests()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={self.user_text}&format=json"
                t = str(requests.get(geocoder_request).json()["response"]["GeoObjectCollection"]["featureMember"][0][
                            "GeoObject"][
                            "Point"]["pos"]).split(' ')
                print(t)
                self.x, self.y = [float(i) for i in t]
                self.x1, self.y1 = t
                self.requests()
                self.active = False
            if self.active:
                if event.key == pg.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                else:
                    self.user_text += event.unicode

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
                    if event.key == pg.K_LEFT:
                        self.x -= 0.026 * math.pow(2, 15 - self.z)
                        self.requests()
                    if event.key == pg.K_RIGHT:
                        self.x += 0.026 * math.pow(2, 15 - self.z)
                        self.requests()
                    if event.key == pg.K_UP and self.y < 85:
                        self.y += 0.0135 * math.pow(2, 15 - self.z)
                        self.requests()
                    if event.key == pg.K_DOWN and self.y > -85:
                        self.y -= 0.0135 * math.pow(2, 15 - self.z)
                        self.requests()
                self.writ(event)
            self.draw()
            self.clock.tick(self.fps)
            self.display.flip()

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(pg.image.load('map.png'), (0, 0))
        if self.active:
            self.color = self.color_active
        else:
            self.color = self.color_passive
        pg.draw.rect(self.screen, self.color, self.input_rect)
        pg.draw.rect(self.screen, self.color_passive, self.ob_rect)
        pg.draw.rect(self.screen, self.color_passive, self.ob2_rect)
        pg.draw.rect(self.screen, self.color_passive, self.ob3_rect)
        pg.draw.rect(self.screen, self.color_passive, self.ob4_rect)
        text_surface = self.base_font.render(self.user_text, True, (255, 255, 255))
        text_surface1 = self.base_font.render(self.ob_text, True, (255, 255, 255))
        text_surface2 = self.base_font.render(self.ob2_text, True, (255, 255, 255))
        text_surface3 = self.base_font.render(self.ob3_text, True, (255, 255, 255))
        text_surface4 = self.base_font.render(self.ob4_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.screen.blit(text_surface1, (self.ob_rect.x + 5, self.ob_rect.y + 5))
        self.screen.blit(text_surface2, (self.ob2_rect.x + 5, self.ob2_rect.y + 5))
        self.screen.blit(text_surface3, (self.ob3_rect.x + 5, self.ob3_rect.y + 5))
        self.screen.blit(text_surface4, (self.ob4_rect.x + 5, self.ob4_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)
        self.ob4_rect.w = max(100, text_surface4.get_width() + 10)


    def requests(self):
        map_request = f"http://static-maps.yandex.ru/1.x/"
        self.search_params = {
            "ll": f'{self.x},{self.y}',
            "z": str(self.z),
            "l": self.format
        }
        if self.x1 != None:
            self.search_params["pt"] = "{0},pm2dgl".format(f'{self.x1},{self.y1}')
        response = requests.get(map_request, self.search_params)
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

