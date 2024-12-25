import sqlite3

class OrderDatabase:
    def __init__(self, db_name='orders.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY,
                    order_type TEXT,
                    scrip_code TEXT,
                    qty INTEGER,
                    price REAL,
                    ah_placed TEXT,
                    exchange TEXT,
                    exchange_type TEXT,
                    is_intraday BOOLEAN,
                    remote_order_id INTEGER,
                    stop_loss_price REAL,
                    status TEXT,
                    buying_price REAL,
                    exchange_order_id TEXT
                )
            ''')

    def save_order(self, order, status, buying_price, exchange_order_id):
        with self.conn:
            self.conn.execute('''
                INSERT INTO orders (
                    order_type, scrip_code, qty, price, ah_placed, exchange, exchange_type, 
                    is_intraday, remote_order_id, stop_loss_price, status, buying_price, exchange_order_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                order.order_type, order.scrip_code, order.qty, order.price, 
                order.ah_placed, order.exchange, order.exchange_type, order.is_intraday, 
                order.remote_order_id, order.stop_loss_price, status, buying_price, exchange_order_id
            ))

    def update_order_exchange_id(self, remote_order_id, exchange_order_id):
        with self.conn:
            self.conn.execute('''
                UPDATE orders
                SET exchange_order_id = ?
                WHERE remote_order_id = ?
            ''', (exchange_order_id, remote_order_id))