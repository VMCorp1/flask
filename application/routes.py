from application import *


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html")


@app.route('/')
@app.route('/catalog')
def catalog():
    items = eshop.get_items_from_catalog()
    print(len(items))
    return render_template('catalog.html', items=items, count=g.count)


@app.route('/add2basket/<int:id>/')
def add2basket(id):
    eshop.save2basket(id)
    return redirect(url_for('catalog'))


@app.route('/basket/')
def basket():
    items = eshop.get_items_from_basket()
    return render_template("basket.html", items=items, count=g.count, plural=eshop.plural)


@app.route('/delete_from_basket/<int:id>/')
def delete_from_basket(id):
    eshop.delete_from_basket(id)
    return redirect(url_for('basket'))


@app.route('/order/')
def order(data=[]):
    return render_template("order.html", data=data)


@app.route('/save_order/', methods=['POST'])
def save_order():
    if eshop.save_order(request.form):
        return render_template("save_order.html")
    else:
        return order(request.form)


@app.route('/admin/')
def admin():
    return "Это админка"


@app.route('/admin/add2catalog/')
def add2catalog():
    return render_template('/admin/add2catalog.html')


@app.route('/admin/save2catalog/', methods=['POST'])
def save2catalog():
    eshop.add_item_to_catalog(request.form)
    return redirect(url_for('add2catalog'))


@app.route('/admin/orders/')
def orders():
    return "Это отчёт о заказах"


@app.route('/admin/add_user/', methods=['GET', 'POST'])
def add_user():
    return "Это добавление сотрудника в систему"


@app.route('/login/', methods=['GET', 'POST'])
def login():
    return "Это форма логина в систему"


@app.route('/logout/')
def logout():
    return "Это выход из системы"
