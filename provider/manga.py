from datetime import datetime as dt, timedelta
from provider.utils import get_dom, on_workdays


URL = "http://mangacowboy.hu/"

@on_workdays
def getMenu(today):
    dom = get_dom(URL)
    date = today.strftime("%Y. %m. %d.")
    menu = dom.xpath(f'//section[@id="weekly_menu"]/ul/li[.//time[contains(text(), "{ date }")]]'
                     '//div[@class="weeklyMenuPreview-content"]')
    if menu:
        menu = list(menu[0].xpath("./p/text()"))
    else:
        menu = []

    return menu

menu = {
    'name': 'Manga',
    'id': 'mc',
    'url': URL,
    'get': getMenu,
    'ttl': timedelta(hours=23),
    'cards': ['szep', 'erzs']
}
