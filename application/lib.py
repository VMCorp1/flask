from application import *
import time, datetime


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

    if not data or g.delete_basket:
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


def delete_from_basket(id):
    if type(id) == int and id > 0:
        id = str(id)
        if id in list(g.basket.keys()):
            del g.basket[id]
            g.save_basket = True
        else:
            g.save_basket = False


def plural(n, form1, form2, form5):
    if 10 < n % 100 < 20:
        return form5
    if n % 10 == 1:
        return form1
    if 1 < n % 10 < 5:
        return form2
    if n % 10 >= 5:
        return form5
    if n % 10 == 0:
        return form5


def save_order(data):
    name = clear_str(data['name'])
    email = clear_str(data['email'])
    phone = clear_str(data['phone'])
    address = clear_str(data['address'])
    error = False
    if name == '':
        flash('Заполните поле имя!', 'error')
        error = True
    if email == '':
        flash('Заполните поле email!', 'error')
        error = True
    if phone == '':
        flash('Заполните поле номер телефона!', 'error')
        error = True
    if address == '':
        flash('Заполните поле адрес!', 'error')
        error = True
    if not error:
        try:
            order = Order(name, email, phone, address, g.basket['orderid'], int(time.time()))
            db.session.add(order)
            items = get_items_from_basket()
            for item in items:
                db.session.add(OrderItem(item.title, item.author, item.pubyear, item.price, item.quantity, order.id))
            db.session.commit()
            flash("Ваш заказ принят.")
            g.delete_basket = True
            return True
        except:
            db.session.rollback()
            flash("Произошла ошибка!")
            return False
    return False


def get_orders():
    all_orders = []
    format = '%d-%m-%Y %H:%M:%S'
    for order in db.session.query(Order):
        order_info = {}

        order_info['name'] = order.name
        order_info['email'] = order.email
        order_info['phone'] = order.phone
        order_info['address'] = order.address
        order_info['orderid'] = order.orderid
        created = datetime.datetime.fromtimestamp(order.created).strftime(format)
        order_info['created'] = created

        items = db.session.query(OrderItem).filter(OrderItem.orderid == order.id).all()
        order_info['items'] = items

        all_orders.append(order_info)

    return all_orders


def add_user(data):
    login = clear_str(data["login"])
    password = clear_str(data["password"])
    if not login or not password:
        flash("Заполните все поля формы!")
        return
    try:
        password = generate_password_hash(password)
        db.session.add(User(login, password))
        db.session.commit()
        flash("Пользователь " + login + " успешно добавлен в систему")
    except:
        db.session.rollback()
        flash("Пользователь с таким именем существует!")


def login(data):
    login = clear_str(data["login"])
    password = clear_str(data["password"])
    if not login or not password:
        flash("Заполните все поля формы!")
        return False
    user = User.query.filter(User.login == login).first()
    if not user:
        flash("Логин или пароль не верны!")
        return False
    if not check_password_hash(user.password, password):
        flash("Логин или пароль не верны!")
        return False
    session["logged"] = True
    return True


def logout():
    session["logged"] = False
