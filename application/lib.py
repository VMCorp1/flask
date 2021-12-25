from application import *


def clear_str(input_str):
    input_str = Markup(input_str).striptags().strip()
    # summary = Markup.escape(request.form["summary"])
    return input_str


def clear_int(input_str):
    input_str = clear_str(input_str)
    try:
        return int(input_str)
    except ValueError:
        return 0


def add_item_to_catalog(data):
    title = clear_str(data['title'])
    author = clear_str(data['author'])
    pubyear = clear_int(data['pubyear'])
    price = clear_int(data['price'])
    # answer = title+author+str(pubyear)+str(price)
    if title == '' or author == '' or pubyear == 0 or price == 0:
        flash('Заполните все поля*', "error")
    else:
        catalog_item = Catalog(title, author, pubyear, price)
        db.session.add(catalog_item)
        db.session.commit()
        flash('Успешно добавлено!')
        flash('Название: {0}'.format(title))
        flash('Автор: {0}'.format(author))
        flash('Год издания: {0}'.format(pubyear))
        flash('Цена: {0}'.format(price))


def get_items_from_catalog():
    return Catalog.query.all()


import base64, uuid, json


def stringToBase64(s):
    '''Упаковывает строку s алгоритмом base64 для целостности данных'''
    return base64.b64encode(s.encode('utf-8'))


def base64ToString(b):
    '''Распаковывает base64 строку b в строку'''
    return base64.b64decode(b).decode('utf-8')


def basket_init():
    # Вызывается при каждом запросе.
    # Проверяет, первый ли раз пришёл пользователь.
    # Если пользователь пришёл первыё раз, то
    # создаётся корзина и генерируется уникальный
    # идентификатор заказа.
    # Иначе, корзина распаковывается в словарь basket
    data = request.cookies.get("basket", None)

    if not data:
        g.count = 0  # количество товара в корзине
        g.basket = {}
        g.basket["orderid"] = str(uuid.uuid1())
        g.save_basket = True  # надо ли сохранять корзину в куки
    else:
        g.basket = json.loads(base64ToString(data))
        g.count = len(g.basket) - 1
        g.save_basket = False


def basket_serialize():
    '''Сериализует корзину в формат JSON и оборачивает base64'''

    return stringToBase64(json.dumps(g.basket))


def save2basket(id):
    if type(id) == int and id > 0:
        id = str(id)
        if id not in list(g.basket.keys()):
            g.basket[id] = 0
        print(g.basket.keys())
        g.basket[id] += 1
        g.save_basket = True
    else:
        g.save_basket = False


def get_items_from_basket():
    ids = list(g.basket.keys())
    ids.remove('orderid')
    items = []
    if len(ids) > 0:
        for item in Catalog.query.filter(Catalog.id.in_(ids)):
            item.quantity = g.basket[str(item.id)]
            items.append(item)
    return items
