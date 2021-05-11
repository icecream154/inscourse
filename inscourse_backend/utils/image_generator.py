import PIL.Image as Image
import pygame
import random

from project_config import PROJECT_ROOT

back_color = [
    (234, 34, 23),
    (54, 241, 224),
    (227, 235, 81),
    (108, 235, 169),
    (235, 35, 205),
    (235, 130, 81),
    (141, 133, 235),
    (111, 53, 235)
]


# 生成简介图片
def generate_icon(content: str, language: str, background_color: tuple, font_color: tuple, save_path: str):
    pygame.init()
    if language == 'en' and len(content) <= 10:
        en_font_size_list = [
            170,  # 1
            155,  # 2
            135,  # 3
            125,  # 4
            100,  # 5
            85,   # 6
            75,   # 7
            65,   # 8
            55,   # 9
            45    # 10
        ]
        image = Image.new("RGB", (300, 300),
                          background_color)
        font = pygame.font.Font(PROJECT_ROOT + '/inscourse_backend/utils/fonts/Reynatta-2.ttf', en_font_size_list[len(content) - 1])
        ftext = font.render(content, True, font_color,
                            background_color)

        pygame.image.save(ftext, "./tmp.png")
        width, height = pygame.image.load("./tmp.png").get_rect().size

        line = Image.open("./tmp.png")
        image.paste(line, (int(150 - width / 2), int(180 - height / 2)))

        image.save(save_path)
    elif language == 'zh' and len(content) <= 4:
        if len(content) == 4:
            font_size = 100
            image = Image.new("RGB", (300, 300),
                              background_color)
            font = pygame.font.Font(PROJECT_ROOT + '/inscourse_backend/utils/fonts/FangZhengKaiTiJianTi-1.ttf', font_size)
            ftext = font.render(content[0] + ' ' + content[1], True, font_color,
                                background_color)

            pygame.image.save(ftext, "./tmp.png")
            width, height = pygame.image.load("./tmp.png").get_rect().size

            line = Image.open("./tmp.png")
            image.paste(line, (int(150 - width / 2), int(85 - height / 2)))

            ftext = font.render(content[2] + ' ' + content[3], True, font_color,
                                background_color)

            pygame.image.save(ftext, "./tmp.png")
            width, height = pygame.image.load("./tmp.png").get_rect().size

            line = Image.open("./tmp.png")
            image.paste(line, (int(150 - width / 2), int(215 - height / 2)))
            image.save(save_path)

        else:
            zh_font_size_list = [170, 120, 80]
            image = Image.new("RGB", (300, 300),
                              background_color)
            font = pygame.font.Font(PROJECT_ROOT + '/inscourse_backend/utils/fonts/FangZhengKaiTiJianTi-1.ttf', zh_font_size_list[len(content) - 1])
            ftext = font.render(content, True, font_color,
                                background_color)

            pygame.image.save(ftext, "./tmp.png")
            width, height = pygame.image.load("./tmp.png").get_rect().size

            line = Image.open("./tmp.png")
            image.paste(line, (int(150 - width / 2), int(160 - height / 2)))

            image.save(save_path)


if __name__ == '__main__':
    # font_name = "Arial.ttf"
    color_number = random.randint(0, 7)
    pygame.init()

    en_words = [
        'C',
        'C#',
        'C++',
        'Cola',
        'React',
        'Python',
        'Angular',
        'Birthday',
        'Financial',
        'Psychology'
    ]

    for i in range(len(en_words)):
        generate_icon(en_words[i], 'en', back_color[0], (255, 255, 255), './images/' + en_words[i] + '.png')

    zh_words = [
        u'雪',
        u'高数',
        u'法理学',
        u'数学分析'
    ]

    for i in range(len(zh_words)):
        generate_icon(zh_words[i], 'zh', back_color[0], (255, 255, 255), './images/' + zh_words[i] + '.png')
