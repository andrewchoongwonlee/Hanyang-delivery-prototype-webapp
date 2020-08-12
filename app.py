from flask import Flask, render_template, request, jsonify, redirect, send_from_directory
import psycopg2 as pg
import psycopg2.extras
import json
import datetime
import time
import os

app = Flask(__name__)

session = {'name': None, 'uid': None, 'password': None, 'role' : None, 'seller_id': None}
customer_cart = {}

db_connector = {'host' : 'localhost', 'user' : 'postgres', 'dbname' : 'postgres', 'port' : '5432', 'password':'p@s$W0rd'}

connect_string = "host={host} user={user} dbname={dbname} password={password} port={port}".format(**db_connector)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/search_ajax')
def search_ajax():
    search_type = request.args.get('type')
    if search_type == 'name':
        value = request.args.get('value')
        stores = {}
        if value == '':
            return jsonify(stores)

        conn = pg.connect(connect_string)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = f"SELECT * FROM stores WHERE sname LIKE '%{value}%'"
        print(sql)
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            stores[row[0]] = {
                'sname':row[2],
                'address':row[1],
                'latlng':[row[3], row[4]],
                'phone_nums':json.loads(row[5]),
                'schedule': json.loads(row[6]),
                'seller_id':row[7]
            }

            today = datetime.datetime.today()
            week = int(today.strftime('%w'))
            currtime = int(today.strftime('%H%M'))
            if stores[row[0]]['schedule'][week]['holiday'] == True:
                stores[row[0]]['open'] = 'CLOSED'
            else:
                tempOpen = int(stores[row[0]]['schedule'][week]['open'])
                tempClosed = int(stores[row[0]]['schedule'][week]['closed'])
                if tempOpen >= tempClosed:
                    tempClosed += 2400
                
                if currtime >= tempOpen and currtime <= tempClosed:
                    stores[row[0]]['open'] = 'OPEN'
                else:
                    stores[row[0]]['open'] = 'CLOSED'
                
        

        conn.close()
        return jsonify(stores)

    elif search_type == 'sid':
        value = request.args.get('value')

        conn = pg.connect(connect_string)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = f"SELECT * FROM stores WHERE sid ='{value}'"
        cur.execute(sql)
        row = cur.fetchall()[0]
        stores = {
            'sname':row[2],
            'address':row[1],
            'latlng':[row[3], row[4]],
            'phone_nums':json.loads(row[5]),
            'schedule': json.loads(row[6]),
            'seller_id':row[7]
        }

        today = datetime.datetime.today()
        week = int(today.strftime('%w'))
        currtime = int(today.strftime('%H%M'))
        if stores['schedule'][week]['holiday'] == True:
            stores['open'] = 'CLOSED'
        else:
            tempOpen = int(stores['schedule'][week]['open'])
            tempClosed = int(stores['schedule'][week]['closed'])
            if tempOpen >= tempClosed:
                tempClosed += 2400
            
            if currtime >= tempOpen and currtime <= tempClosed:
                stores['open'] = 'OPEN'
            else:
                stores['open'] = 'CLOSED'

        conn.close()
        return jsonify(stores)

    elif search_type == 'address':
        value = request.args.get('value')
        print(value)
        stores = {}
        if value == '':
            return jsonify(stores)

        conn = pg.connect(connect_string)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = f"SELECT * FROM stores WHERE address LIKE '%{value}%' LIMIT 100"
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            stores[row[0]] = {
                'sname':row[2],
                'address':row[1],
                'latlng':[row[3], row[4]],
                'phone_nums':json.loads(row[5]),
                'schedule': json.loads(row[6]),
                'seller_id':row[7]
            }

            today = datetime.datetime.today()
            week = int(today.strftime('%w'))
            currtime = int(today.strftime('%H%M'))
            if stores[row[0]]['schedule'][week]['holiday'] == True:
                stores[row[0]]['open'] = 'CLOSED'
            else:
                tempOpen = int(stores[row[0]]['schedule'][week]['open'])
                tempClosed = int(stores[row[0]]['schedule'][week]['closed'])
                if tempOpen >= tempClosed:
                    tempClosed += 2400
                
                if currtime >= tempOpen and currtime <= tempClosed:
                    stores[row[0]]['open'] = 'OPEN'
                else:
                    stores[row[0]]['open'] = 'CLOSED'
        conn.close()
        return jsonify(stores)

    elif search_type == 'tags':
        value = request.args.get('value')
        print(value)
        stores = {}
        if value == '':
            return jsonify(stores)

        conn = pg.connect(connect_string)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = f"SELECT * FROM stores WHERE tags LIKE '%{value}%' LIMIT 100"
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            stores[row[0]] = {
                'sname':row[2],
                'address':row[1],
                'latlng':[row[3], row[4]],
                'phone_nums':json.loads(row[5]),
                'schedule': json.loads(row[6]),
                'seller_id':row[7]
            }

            today = datetime.datetime.today()
            week = int(today.strftime('%w'))
            currtime = int(today.strftime('%H%M'))
            if stores[row[0]]['schedule'][week]['holiday'] == True:
                stores[row[0]]['open'] = 'CLOSED'
            else:
                tempOpen = int(stores[row[0]]['schedule'][week]['open'])
                tempClosed = int(stores[row[0]]['schedule'][week]['closed'])
                if tempOpen >= tempClosed:
                    tempClosed += 2400
                
                if currtime >= tempOpen and currtime <= tempClosed:
                    stores[row[0]]['open'] = 'OPEN'
                else:
                    stores[row[0]]['open'] = 'CLOSED'
        conn.close()
        return jsonify(stores)

    elif search_type == 'near':
        num = request.args.get('num')
        lat = request.args.get('lat')
        lng = request.args.get('lng')

        stores = []
        conn = pg.connect(connect_string)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = f"SELECT sid, sname, address, lat, lng, phone_nums, schedules, ({lat}-lat)^2 + ({lng}-lng)^2 AS length FROM stores ORDER BY 8 limit {num}"
        cur.execute(sql)
        rows = cur.fetchall()

        for row in rows:
            temp = {
                'sid':row[0],
                'sname':row[1],
                'address':row[2],
                'latlng':[row[3], row[4]],
                'phone_nums':json.loads(row[5])
            }

            today = datetime.datetime.today()
            week = int(today.strftime('%w'))
            schedule = json.loads(row[6])

            currtime = int(today.strftime('%H%M'))
            if schedule[week]['holiday'] == True:
                temp['open'] = 'CLOSED'
            else:
                tempOpen = int(schedule[week]['open'])
                tempClosed = int(schedule[week]['closed'])
                if tempOpen >= tempClosed:
                    tempClosed += 2400
                
                if currtime >= tempOpen and currtime <= tempClosed:
                    temp['open'] = 'OPEN'
                else:
                    temp['open'] = 'CLOSED'

            stores.append(temp)
        conn.close()
        return jsonify(stores)

    elif search_type == "cart":
        return jsonify(customer_cart)
    
    elif search_type == "unprocessed_orders":
        uid = request.args.get('uid')
        orders = []
        conn = pg.connect(connect_string)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = f"SELECT O.time, S.sname, O.menu, O.sid FROM unprocessed_orders O, stores S WHERE O.uid='{uid}' and O.sid = S.sid"
        cur.execute(sql)
        rows = cur.fetchall()


        for row in rows:
            tempmenu = list(row[2][0].keys())[0] + '(' + row[2][0][list(row[2][0].keys())[0]] + ')'
            if len(row[2]) > 1:
                tempmenu += ' 외' + str(len(row[2])-1)
            orders.append({'timestamp':row[0], 'sname':row[1], 'menu': tempmenu, 'sid':row[3]})

        return jsonify(orders)

    elif search_type == "unprocessed_orders_s":
        sid = request.args.get('sid')
        print(sid)
        orders = []
        conn = pg.connect(connect_string)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = f"SELECT O.time, S.sname, O.menu, O.sid FROM unprocessed_orders O, stores S WHERE O.sid='{sid}' and O.sid = S.sid"
        cur.execute(sql)
        rows = cur.fetchall()
        print(rows)

        for row in rows:
            tempmenu = list(row[2][0].keys())[0] + '(' + row[2][0][list(row[2][0].keys())[0]] + ')'
            if len(row[2]) > 1:
                tempmenu += ' 외' + str(len(row[2])-1)
            orders.append({'timestamp':row[0], 'sname':row[1], 'menu': tempmenu, 'sid':row[3]})

        return jsonify(orders)

    elif search_type == "processing_orders_s":
        sid = request.args.get('sid')
        orders = []
        conn = pg.connect(connect_string)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = f"SELECT O.time, S.sname, O.menu, O.sid FROM processing_orders O, stores S WHERE O.sid='{sid}' and O.sid = S.sid"
        cur.execute(sql)
        rows = cur.fetchall()


        for row in rows:
            tempmenu = list(row[2][0].keys())[0] + '(' + row[2][0][list(row[2][0].keys())[0]] + ')'
            if len(row[2]) > 1:
                tempmenu += ' 외' + str(len(row[2])-1)
            orders.append({'timestamp':row[0], 'sname':row[1], 'menu': tempmenu, 'sid':row[3]})

        return jsonify(orders)

@app.route("/login", methods=['POST', 'GET'])
def login():
    if session['uid'] != None:
        return redirect("/")
    else:
        if request.method == 'POST':
            local, domain = request.form.get('uid').split('@')
            password = request.form.get('password')
            
            conn = pg.connect(connect_string)
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            login_info = []
            for role in ['sellers', 'customers', 'delivery']:
                sql = f"SELECT name FROM {role} WHERE local='{local}' and domain='{domain}' and passwd='{password}'"
                cur.execute(sql)
                rows = cur.fetchall()
                if len(rows) == 0:
                    print(role)
                else:
                    login_info.append([role, rows[0][0]])
            

            if len(login_info) == 0:
                return render_template("/login.html", session=session)
            else:
                login_info = login_info[0]
                role = login_info[0]
                name = login_info[1]

                uid = local + '@' + domain
                session['uid'] = uid
                session['password'] = password

                session['role'] = role
                session['name'] = name

                print(f'{role} | {name} - {uid}:{password}')
                return redirect("/")
        else:
            return render_template("/login.html", session=session)
        

@app.route("/logout", methods=['POST'])
def logout():
    if session['uid'] == None:
        return redirect("/")
    else:
        for key in session.keys():
            session[key] = None
        customer_cart = []

        return redirect("/")

@app.route("/near", methods=['GET'])
def near():
    if session['uid'] == None:
        return redirect("/")
    else:
        return render_template("near.html", session=session)

@app.route("/")
def index():
    return render_template("index.html", session=session)

@app.route("/search/byname")
def search_name():
    return render_template("search_name.html", session=session)

@app.route("/search/byaddress")
def search_address():
    conn = pg.connect(connect_string)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "SELECT address FROM stores"
    cur.execute(sql)
    rows = cur.fetchall()
    loc = list(set([row[0].split(" ")[0] + "_" + row[0].split(" ")[1] for row in rows]))

    print(loc)
    return render_template("search_address.html", session=session, loc=loc)

@app.route("/search/bytags")
def search_tags():
    return render_template("search_tags.html", session=session)

@app.route("/store")
def store():
    if request.args.get('sid') == None or session['uid'] == None:
        return redirect("/")
    else:
        value = request.args.get('sid')
        data = {}
        conn = pg.connect(connect_string)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = f"SELECT * FROM stores WHERE sid ='{value}'"
        print(sql)
        try:
            cur.execute(sql)
            row = cur.fetchall()[0]
        except:
            return redirect("/")
        else:
            data[value] = {
                'sname':row[2],
                'address':row[1],
                'latlng':[row[3], row[4]],
                'phone_nums':json.loads(row[5]),
                'schedule': json.loads(row[6]),
                'seller_id': row[7],
                'description' : row[8],
                'tags' : row[9]
            }
            today = datetime.datetime.today()
            week = int(today.strftime('%w'))
            currtime = int(today.strftime('%H%M'))
            if data[value]['schedule'][week]['holiday'] == True:
                data[value]['open'] = 'CLOSED'
            else:
                tempOpen = int(data[value]['schedule'][week]['open'])
                tempClosed = int(data[value]['schedule'][week]['closed'])
                if tempOpen >= tempClosed:
                    tempClosed += 2400
                
                if currtime >= tempOpen and currtime <= tempClosed:
                    data[value]['open'] = 'OPEN'
                else:
                    data[value]['open'] = 'CLOSED'

            
            sql = f"SELECT * FROM menu WHERE sid ='{value}'"
            print(sql)
            cur.execute(sql)
            rows = cur.fetchall()
            menu = [row[0] for row in rows]

            menu = json.dumps(menu)
            conn.close()

            return render_template("store.html", session=session, sid=value, data=data, menu=menu)

@app.route("/mypage/info/auth", methods=['GET'])
def info_edit_auth():
    uid = request.args.get('uid')
    return render_template("edit_auth.html", session=session, uid=uid)

@app.route("/mypage/info/edit", methods=['POST'])
def info_edit():
    posttype = request.form.get('type')
    if posttype == 'auth':
        uid = request.form.get('uid')
        local, domain = uid.split('@')
        password = request.form.get('password')

        if password != session['password'] or uid != session['uid']:
            return render_template("edit_auth.html", session=session, uid=uid)
        else:
            conn = pg.connect(connect_string)
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql = f"SELECT name, phone, local, domain, passwd FROM {session['role']} WHERE local ='{local}' and domain ='{domain}' and passwd ='{password}'"
            cur.execute(sql)
            data = cur.fetchall()[0]

            return render_template("edit_info.html", session=session, data=data)

@app.route("/mypage/info/auth", methods=['POST'])
def editaction():
    local = request.form.get('local')
    domain = request.form.get('domain')
    password = request.form.get('password')
    name = request.form.get('name')
    phone = request.form.get('phone')
    uid = local +'@' + domain

    conn = pg.connect(connect_string)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = f"UPDATE {session['role']} SET passwd='{password}', name='{name}', phone='{phone}' WHERE local='{local}' and domain='{domain}'"
    cur.execute(sql)
    conn.commit()
    conn.close()    

    return render_template("edit_auth.html", session=session, uid=uid)


@app.route("/cartaction", methods=['POST'])
def cartaction():
    global customer_cart

    params = dict(request.form)
    action = params['action'][0]

    if action == 'add':
        sid = params['sid'][0]
        params.pop('action')
        params.pop('sid')
        customer_cart[sid] = [[item, int(params[item][0])] for item in params.keys() if int(params[item][0]) != 0]
        return redirect(f"/store?sid={sid}")
    
    elif action == 'delete':
        customer_cart = {}
        return redirect("/mypage/customer/cart?uid=" + session['uid'])

    else:
        return redirect("/")

@app.route("/mypage/customer/cart", methods=['GET'])
def cart():
    uid = request.args.get('uid')
    if session['uid'] != uid:
        return redirect("/")
    else:
        return render_template("cart.html", session=session, customer_cart=customer_cart)

@app.route("/order", methods=['POST'])
def order():
    params = dict(request.form)
    print(params)
    sid = params['sid'][0]
    params.pop('sid')

    orderlist = [[item, int(params[item][0])] for item in params.keys()]

    customer_info = {}
    local, domain = session['uid'].split('@')
    conn = pg.connect(connect_string)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = f"SELECT phone, payments FROM customers WHERE local ='{local}' and domain ='{domain}' and passwd ='{session['password']}'"
    print(sql)
    cur.execute(sql)
    row = cur.fetchall()[0]
    phone = row[0]
    paymentstemp = row[1]
    payments = []
    for payment in paymentstemp:
        if payment['type'] == 'account':
            sql = f"SELECT name FROM bank WHERE bid = '{payment['data']['bid']}'"
            cur.execute(sql)
            bank = cur.fetchall()[0][0]
            payments.append([bank, payment['data']['acc_num']])
        elif payment['type'] == 'card':
            payments.append(['카드', payment['data']['card_num']])

    sql = f"SELECT address FROM customers WHERE local='{local}'and domain='{domain}' and passwd='{session['password']}'" 
    cur.execute(sql)
    address = cur.fetchall()[0][0]
    print(address)
    if address != None:
        if type(address) == str:
            address = json.loads(address)
    else:
        address = []
    
    print(address)

    conn.close()
    return render_template("order.html", session=session, orderlist=orderlist, sid=sid, phone=phone ,payments=payments, address=address)

@app.route("/mypage/customer/order", methods=['GET'])
def orderlist():
    uid = session['uid']
    return render_template("orderlist.html", session=session, uid=uid)

@app.route("/orderaction", methods=['POST'])
def orderaction():
    params = dict(request.form)
    print(params)
    sid = params['sid'][0]
    params.pop('sid')
    name = params['name'][0]
    params.pop('name')
    uid = params['uid'][0]
    params.pop('uid')
    address = params['address'][0]
    params.pop('address')
    phone = params['phone'][0]
    params.pop('phone')
    payment = params['payment'][0]
    params.pop('payment')

    menu = []
    for i in params.keys():
        menu.append({i:params[i][0]})

    menu = json.dumps(menu)

    timestamp = int(time.time())

    conn = pg.connect(connect_string)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = f"INSERT INTO unprocessed_orders VALUES ('{uid}', '{sid}', '{menu}', '{timestamp}', '{payment}', '{address}', '{phone}')"
    cur.execute(sql)
    conn.commit()

    sql2 = f"INSERT INTO orders VALUES ('{uid}', '{sid}', '{menu}', '{timestamp}', '{payment}', '{address}', '{phone}', 'submitted')"
    cur.execute(sql2)
    conn.commit()
    conn.close()

    return redirect("/mypage/customer/order")

@app.route("/order/detail", methods=['GET'])
def orderdetail():
    if session['role'] == 'customers':
        timestamp, sid, uid = request.args.get('ordertoken').split('-')
        conn = pg.connect(connect_string)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = f"SELECT O.sid, O.uid, O.time, O.menu, O.payment, O.address, O.phone, S.sname FROM orders O, stores S WHERE O.time='{timestamp}' and O.sid='{sid}' and O.uid='{uid}' and O.sid = S.sid"
        cur.execute(sql)
        data = cur.fetchall()[0]

        conn.close()
        return render_template('orderdetail.html', session=session, data=data)

    elif session['role'] == 'sellers':
        timestamp, sid = request.args.get('ordertoken').split('-')
        conn = pg.connect(connect_string)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = f"SELECT O.sid, O.uid, O.time, O.menu, O.payment, O.address, O.phone, S.sname FROM orders O, stores S WHERE O.time='{timestamp}' and O.sid='{sid}' and O.sid = S.sid"
        cur.execute(sql)
        data = cur.fetchall()[0]

        conn.close()
        return render_template('orderdetail.html', session=session, data=data)

@app.route("/order/confirm", methods=['GET'])
def orderconfirmGET():
    timestamp, sid = request.args.get('ordertoken').split('-')
    conn = pg.connect(connect_string)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = f"SELECT uid, sid, menu, time, payment, address, phone FROM unprocessed_orders WHERE time='{timestamp}' and sid='{sid}'"
    cur.execute(sql)
    order = cur.fetchall()[0]

    sql = f"SELECT lat, lng FROM stores WHERE sid='{sid}'"
    cur.execute(sql)
    row = cur.fetchall()[0]
    lat = row[0]
    lng = row[1]

    sql = f"SELECT did, name, phone, lat, lng, stock, ({lat}-lat)^2 + ({lng}-lng)^2 AS length FROM delivery WHERE stock < 5 ORDER BY 7 limit 5"
    print(sql)
    cur.execute(sql)
    delivery = cur.fetchall()
    

    return render_template("orderconfirm.html", session=session, delivery=delivery, order=order)

@app.route("/order/confirm", methods=['POST'])
def orderconfirmPOST():
    timestamp = request.form.get('timestamp')
    sid = request.form.get('sid')
    delivery = request.form.get('delivery')

    conn = pg.connect(connect_string)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = f"SELECT uid, sid, menu, time, payment, address, phone FROM unprocessed_orders WHERE time='{timestamp}' and sid='{sid}'"
    cur.execute(sql)
    row = cur.fetchall()[0]
    uid = row[0]
    sid = row[1]
    menu = json.dumps(row[2])
    timestamp = row[3]
    payment = row[4]
    address = row[5]
    phone = row[6]

    sql = f"DELETE FROM unprocessed_orders WHERE time='{timestamp}' and sid='{sid}'"
    cur.execute(sql)
    conn.commit()
    sql = f"INSERT INTO processing_orders VALUES ('{uid}', '{sid}', '{menu}', '{timestamp}', '{payment}', '{address}', '{phone}', '{delivery}')"
    cur.execute(sql)
    conn.commit()

    sql = f"UPDATE orders SET status='in delivery' WHERE time='{timestamp}' and sid='{sid}'"
    cur.execute(sql)
    conn.commit()

    sql = f"SELECT stock FROM delivery WHERE did='{delivery}'"
    cur.execute(sql)
    stock = int(cur.fetchall()[0][0]) + 1

    sql = f"UPDATE delivery SET stock='{stock}' WHERE did='{delivery}'"
    cur.execute(sql)
    conn.commit()


    conn.close()
    return redirect("/mypage/seller/order?uid=" + session['uid'])
    

@app.route("/mypage/customer/payments", methods=['GET'])
def editcustomerpaymentGET():
    local, domain = session['uid'].split('@')
    passwd = session['password']
    conn = pg.connect(connect_string)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = f"SELECT payments FROM customers WHERE local='{local}'and domain='{domain}' and passwd='{passwd}'" 
    cur.execute(sql)

    payments = cur.fetchall()[0][0]
    if type(payments) == str:
        payments = json.loads(payments)
    
    sql = f"SELECT bid, name FROM bank" 
    cur.execute(sql)
    bank = cur.fetchall()
    banks = {}
    for b in bank:
        banks[b[0]] = b[1]

    conn.close()

    return render_template('paymentedit.html', session=session, payments=payments, banks=banks)

@app.route("/mypage/customer/payments", methods=['POST'])
def editcustomerpaymentPOST():
    local, domain = session['uid'].split('@')
    passwd = session['password']
    conn = pg.connect(connect_string)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = f"SELECT payments FROM customers WHERE local='{local}'and domain='{domain}' and passwd='{passwd}'" 
    cur.execute(sql)

    payments = cur.fetchall()[0][0]
    if type(payments) == str:
        payments = json.loads(payments)

    posttype = request.form.get('type')
    paymenttype =  request.form.get('paymenttype')
    num =  request.form.get('num')

    if posttype == 'add':
        if paymenttype == 'card':
            payments.append({'type': 'card', 'data': {'card_num' : num}})
        else:
            payments.append({'type':'account', 'data':{'bid':int(paymenttype), 'acc_num' : num}})

        sql = f"UPDATE customers SET payments='{json.dumps(payments)}' WHERE local='{local}'and domain='{domain}' and passwd='{passwd}'" 
        cur.execute(sql)
        conn.commit()
        conn.close()

    if posttype == 'delete':
        conn = pg.connect(connect_string)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = f"SELECT payments FROM customers WHERE local='{local}'and domain='{domain}' and passwd='{passwd}'" 
        cur.execute(sql)

        payments = cur.fetchall()[0][0]
        if type(payments) == str:
            payments = json.loads(payments)


        paymenttype , num = request.form.get('value').split("|")
        print(payments)
        print(paymenttype)
        print(num)
        new_payments = []
        for i in payments:
            if i['type'] == paymenttype:
                if paymenttype == 'card':
                    if i['data']['card_num'] == num or i['data']['card_num']  == int(num):
                        pass
                    else:
                        new_payments.append(i)
                else:
                    if i['data']['acc_num'] == num or i['data']['acc_num'] == int(num):
                        pass
                    else:
                        new_payments.append(i)
            else:
                new_payments.append(i)

        sql = f"UPDATE customers SET payments='{json.dumps(new_payments)}' WHERE local='{local}'and domain='{domain}' and passwd='{passwd}'" 
        cur.execute(sql)
        conn.commit()
        conn.close()

    
    
    return redirect("/mypage/customer/payments?uid="+session['uid'])


@app.route("/mypage/customer/address", methods=['GET'])
def editcustomeraddressGET():
    local, domain = session['uid'].split('@')
    passwd = session['password']
    conn = pg.connect(connect_string)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = f"SELECT address FROM customers WHERE local='{local}'and domain='{domain}' and passwd='{passwd}'" 
    cur.execute(sql)

    address = cur.fetchall()[0][0]
    if type(address) == str:
        address = json.loads(address)

    conn.close()

    return render_template('addressedit.html', session=session, address=address)

@app.route("/mypage/customer/address", methods=['POST'])
def editcustomeraddressPOST():
    local, domain = session['uid'].split('@')
    passwd = session['password']
    conn = pg.connect(connect_string)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = f"SELECT address FROM customers WHERE local='{local}'and domain='{domain}' and passwd='{passwd}'" 
    cur.execute(sql)

    address = cur.fetchall()[0][0]
    if type(address) == str:
        address = json.loads(address)

    posttype = request.form.get('type')

    if posttype == 'add':
        new_address =  request.form.get('new_address')
        if address != None:
            address.append(new_address)
        else:
            address = [new_address]

        print(new_address)
        sql = f"UPDATE customers SET address='{json.dumps(address)}' WHERE local='{local}'and domain='{domain}' and passwd='{passwd}'" 
        cur.execute(sql)
        conn.commit()
        conn.close()

    elif posttype == 'delete':
        value = request.form.get('value')

        conn = pg.connect(connect_string)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = f"SELECT address FROM customers WHERE local='{local}'and domain='{domain}' and passwd='{passwd}'" 
        cur.execute(sql)

        address = cur.fetchall()[0][0]
        if type(address) == str:
            address = json.loads(address)

        address.remove(value)
        
        sql = f"UPDATE customers SET address='{json.dumps(address)}' WHERE local='{local}'and domain='{domain}' and passwd='{passwd}'" 
        cur.execute(sql)
        conn.commit()
        conn.close()

    return redirect("/mypage/customer/address?uid="+session['uid'])


@app.route("/mypage/seller/order", methods=['GET'])
def sellerorder():
    local, domain = session['uid'].split('@')
    password = session['password']
    mystores = []
    conn = pg.connect(connect_string)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = f"SELECT S.sid FROM stores S, sellers U WHERE U.local='{local}'and U.domain='{domain}' and U.passwd='{password}' and U.seller_id = S.seller_id" 
    cur.execute(sql)
    stores = cur.fetchall()
    

    return render_template('sellerorderlist.html', session=session, stores=stores)

@app.route("/mypage/seller/store", methods=['GET'])
def mystoresGET():
    if request.args.get('uid') != session['uid']:
        return redirect("/")

    local, domain = request.args.get('uid').split('@')
    password = session['password']
    
    conn = pg.connect(connect_string)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = f"SELECT seller_id FROM sellers WHERE local='{local}'and domain='{domain}' and passwd='{password}'"
    cur.execute(sql)
    seller_id = cur.fetchall()[0][0]

    sql = f"SELECT m.sid,m.address,m.sname,m.lat,m.lng,m.phone_nums,m.schedules, m.description, m.tags FROM stores m, sellers s WHERE s.local='{local}'and s.domain='{domain}' and s.passwd='{password}' and m.seller_id = s.seller_id ORDER BY 1"
    cur.execute(sql)
    rows = cur.fetchall()
    stores = []
    for row in rows:

        temp = {
            'sid' : row[0],
            'address' : str(row[1]),
            'sname' : row[2],
            'lat' : row[3],
            'lng' : row[4],
            'phone' : json.loads(row[5]),
            'schedules' : json.loads(row[6]),
        }
        if row[8] == None:
            temp['tags'] = ''
        else:
            temp['tags'] = row[8]
        
        if row[7] == None:
            temp['description'] = ''
        else:
            temp['description'] = row[7]
        stores.append(temp)
            
    return render_template("mystores.html", session=session, stores=stores, seller_id=seller_id)

@app.route("/mypage/seller/store", methods=['POST'])
def mystoresPOST():
    sid = request.form.get('sid')
    print(sid)
    description = request.form.get('description')
    print(description)
    tag1 = request.form.get('tag1')
    tag2 = request.form.get('tag2')
    tags = tag1 + "|" + tag2

    conn = pg.connect(connect_string)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = f"UPDATE stores SET description='{description}', tags='{tags}' WHERE sid='{sid}'"
    print(sql)
    cur.execute(sql)
    conn.commit()

    conn.close()

    return redirect("/mypage/seller/store?uid="+session['uid'])

@app.route("/mypage/delivery/current", methods=['GET'])
def currentdelivery():
    if session['role'] != 'delivery':
        return redirect("")

    local, domain = session['uid'].split("@")
    password = session['password']
    conn = pg.connect(connect_string)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = f"SELECT did, stock FROM delivery WHERE local='{local}' and domain='{domain}' and passwd='{password}'"
    cur.execute(sql)
    temp = cur.fetchall()[0]
    did = temp[0]
    stock = temp[1]
    
    sql = f"SELECT * FROM processing_orders WHERE delivery='{did}'"
    cur.execute(sql)
    mydelivery = cur.fetchall()

    return render_template("delivery.html", session=session, delivery=mydelivery, stock=stock)

@app.route("/mypage/seller/store/menu", methods=['GET'])
def editmenuGET():
    sid = request.args.get('sid')
    conn = pg.connect(connect_string)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = f"SELECT menu FROM menu WHERE sid='{sid}'"
    cur.execute(sql)
    menus = cur.fetchall()
    data = []
    for menu in menus:
        data.append(menu[0])
    print(data)
    return render_template("editmenu.html", session=session, menus=data, sid=sid)

@app.route("/mypage/seller/store/menu", methods=['POST'])
def editmenuPOST():
    sid = request.form.get('sid')
    posttype = request.form.get('type')
    
    if posttype == 'modify':
        value = request.form.get('value')
        changeto = request.form.get('changeto')
        conn = pg.connect(connect_string)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = f"UPDATE menu SET menu='{changeto}' WHERE menu='{value}'"
        cur.execute(sql)
        conn.commit()
        conn.close()
    
    elif posttype == 'delete':
        value = request.form.get('value')
        conn = pg.connect(connect_string)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = f"DELETE FROM menu WHERE menu='{value}' and sid='{sid}'"
        cur.execute(sql)
        conn.commit()
        conn.close()
    
    elif posttype == 'add':
        value = request.form.get('value')
        conn = pg.connect(connect_string)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = f"INSERT INTO menu VALUES ('{value}', '{sid}')"
        cur.execute(sql)
        conn.commit()
        conn.close()


    return redirect("/mypage/seller/store/menu?sid="+sid)

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5005)