from PIL import Image
import random
from numba import njit

size: int = 10  # размер изображения, определяет ширину и высоту изображения
final_scale: int = 1000  # окончательный масштаб изображения после его создания, определяет его новый размер в пикселях


@njit
def to_hex(rgb: tuple) -> str:
    """Преобразует rgb в hex"""
    return '#' + ''.join('%02x' % i for i in rgb).upper()


@njit
def random_color():
    """Генерирует случайный цвет в формате RGB"""
    r = lambda: random.randint(0, 255)
    return [r(), r(), r()]


def gradient(start: tuple, end: tuple, steps: int) -> tuple:
    """
        Генерирует градиент цветов между двумя заданными точками.

        Аргументы:
        - start: начальный цвет в формате RGB (кортеж из трех целых чисел)
        - end: конечный цвет в формате RGB (кортеж из трех целых чисел)
        - steps: количество шагов между начальным и конечным цветами

        Возвращает:
        - кортеж цветов, представляющих градиент от start до end

        Пример использования:
        start_color = (255, 0, 0)  # красный цвет
        end_color = (0, 0, 255)    # синий цвет
        gradient_colors = gradient(start_color, end_color, 10)
        # генерирует градиент из 10 цветов от красного до синего
        """
    diff_r = ((end[0] - start[0]) / steps)
    diff_g = ((end[1] - start[1]) / steps)
    diff_b = ((end[2] - start[2]) / steps)

    colors = list()
    colors.append(tuple(start))
    for i in range(1, steps - 1):
        color = list()
        color.append(int(start[0] + i * diff_r))
        color.append(int(start[1] + i * diff_g))
        color.append(int(start[2] + i * diff_b))
        colors.append(tuple(color))
    colors.append(tuple(end))
    return tuple(colors)


def main():
    upleft = random_color()
    downleft = random_color()
    upright = random_color()
    downright = random_color()

    output = tuple()
    first_row = gradient(upleft, downleft, size)
    last_row = gradient(upright, downright, size)

    for i in range(0, size):
        top_color = first_row[i]
        bottom_color = last_row[i]
        output = output + gradient(top_color, bottom_color, size)

    img_name = ''.join(random.choice('0123456789ABCDEF') for _ in range(16))
    im = Image.new('RGB', (size, size))
    im.putdata(tuple(output))
    im = im.resize((final_scale, final_scale))
    im.save(img_name + '.png')
    print('Сохранено как: ' + img_name + '.png')


if __name__ == '__main__':
    main()
