from flask import Flask, render_template, request, redirect, url_for
import xmlrpc.client

app = Flask(__name__)

url = "http://localhost:8069"
db = "db"
username = 'your_login'
password = 'your_password'

# Set up common and models URL for XMLRPC
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

@app.route('/')
def index():
    # Fetch all game servers
    ids = models.execute_kw(db, uid, password, 'server_status', 'search', [[]])
    servers = models.execute_kw(db, uid, password, 'server_status', 'read', [ids], {'fields': ['name', 'ip_addr', 'is_online', 'num_player']})
    return render_template('index.html', servers=servers)

@app.route('/delete/<int:server_id>', methods=['POST'])
def delete_server(server_id):
    # Delete a server
    models.execute_kw(db, uid, password, 'server_status', 'unlink', [[server_id]])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
