import urllib.request
from io import BytesIO
from math import floor
from datetime import timedelta, datetime
from itertools   import takewhile, dropwhile, islice
from PIL import Image, ImageEnhance

from provider.utils import get_filtered_fb_post, create_img, days_lower, get_fb_cover_url, skip_empty_lines

FB_PAGE = "https://www.facebook.com/pg/gilicekonyha/posts/"
FB_ID = "910845662306901"

def cutimage(url, day):
    with urllib.request.urlopen(url) as response:
        r = response.read()
        menu_img = Image.open(BytesIO(r))

        WIDTH = 370
        HEIGHT = 123
        X = 110
        Y = 67
        Y = Y + (HEIGHT * day)
        dailybox = (X, Y, X + WIDTH, Y + HEIGHT)

        menu = menu_img.crop(dailybox)

        new_im = Image.new('L', (WIDTH, HEIGHT))
        new_im.paste(menu, (0, 0))

        enhancer = ImageEnhance.Contrast(new_im)
        new_im = enhancer.enhance(0.85)

        new_im = new_im.point(lambda i: i > 90 and 255)
        new_im = new_im.resize((WIDTH, floor(HEIGHT * 0.56)), Image.BOX)
        new_im = new_im.convert('1')

        f = BytesIO()
        new_im.save(f, format="png", optimize=True, compress_level=9, bits=4)
        return create_img(f)

def getFBMenu(today):
    day = today.weekday()
    menu = ''
    try:
        if day < 5:
            is_this_week = lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').date() > today.date() - timedelta(days=7)
            menu_filter = lambda post: is_this_week(post['created_time']) and "jelmagyarázat" in post['message'].lower()
            menu = get_filtered_fb_post(FB_ID, menu_filter)
            post_parts = menu.split("HETI MENÜ")
            if len(post_parts) > 1:
                weekly_menu = post_parts[1]
                menu = weekly_menu.strip().split("\n")
                menu = islice(dropwhile(lambda l: days_lower[day] not in l, menu), 1, None)
                menu = takewhile(lambda l: not any(day in l for day in days_lower), menu)
                menu = '<br>'.join(skip_empty_lines(menu))
            else:
                menu = f'<a href="{get_fb_cover_url(FB_ID)}">heti menü</a>'
    except:
        pass

    return menu

def getMenu(today):
    if today.weekday() < 5:
        menu = getFBMenu(today)
    else:
        menu = ""

    return {
        'name': 'Gólya',
        'url': FB_PAGE,
        'menu': menu
    }

if __name__ == "__main__":
    print(getMenu(datetime.today()))
