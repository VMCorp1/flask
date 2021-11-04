from application import *


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html")


@app.route('/')
@app.route('/catalog')
def catalog():
    return "Это каталог товаров"


@app.route('/add2basket/<int:id>/')
def add2basket(id):
    return "Это добавление в корзину"


@app.route('/basket/')
def basket():
    return "Это корзина покупателя"


@app.route('/delete_from_basket/<int:id>/')
def delete_from_basket(id):
    return "Это удаление из корзины"


@app.route('/order/')
def order():
    return "Это оформление заказа"


@app.route('/save_order/', methods=['POST'])
def save_order():
    return "Это сохранение заказов"


@app.route('/admin/')
def admin():
    return "Это админка"


@app.route('/admin/add2catalog/')
def add2catalog():
    return "Это добавление товара в каталог"


@app.route('/admin/save2catalog/', methods=['POST'])
def save2catalog():
    return "Это сохранение товара в каталог"


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
