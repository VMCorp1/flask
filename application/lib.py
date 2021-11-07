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
        catalog_item = eshop.Catalog(title, author, pubyear, price)
        db.session.add(catalog_item)
        flash('Успешно добавлено!')
        flash('Название: {0}'.format(title))
        flash('Автор: {0}'.format(author))
        flash('Год издания: {0}'.format(pubyear))
        flash('Цена: {0}'.format(price))

