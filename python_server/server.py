import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Type
import psycopg2
import os
import time

DB_HOST = os.environ.get('DB_HOST', 'postgres')
DB_PORT = int(os.environ.get('DB_PORT', 5432))
DB_NAME = os.environ.get('DB_NAME', 'mydatabase')
DB_USER = os.environ.get('DB_USER', 'myuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'mypassword')

def connect_to_db():
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            print("Połączono z bazą danych")
            return conn
        except psycopg2.OperationalError:
            print("Błąd połączenia z bazą danych, ponawianie za 5 sekund...")
            time.sleep(5)

conn = connect_to_db()
        


class SimpleRequestHandler(BaseHTTPRequestHandler):


    # user_list = [{
    #     'id': 1,
    #     'firstName': 'Kacper',
    #     'lastName': 'Samolej',
    #     'role': 'student'
    # }]

    # next_id = 2


    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        cursor = conn.cursor()
        cursor.execute("select id, first_name, last_name, role from users;")
        users = cursor.fetchall()
        user_list = [
            {'id': row[0], 'firstName': row[1], 'lastName': row[2], 'role': row[3]}
            for row in users
        ]


        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        self.wfile.write(json.dumps(user_list).encode())
        cursor.close()

   
    def do_POST(self) -> None:
        content_length: int = int(self.headers['Content-Length'])
        post_data: bytes = self.rfile.read(content_length)
        received_data: dict = json.loads(post_data.decode())

        firstName = received_data.get('firstName')
        lastName = received_data.get('lastName')
        role = received_data.get('role')

        cursor = conn.cursor()
        cursor.execute(
            "insert into users (first_name, last_name, role) values (%s, %s, %s) returning id;",
            (firstName, lastName, role)
        )

        user_id = cursor.fetchone()[0]
        conn.commit()   

        
        new_user = {
            'id': user_id,
            'firstName': firstName,
            'lastName': lastName,
            'role': role
        } 

        response: dict = {
            "message": "New user added",
            "user": new_user
        }

        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        self.wfile.write(json.dumps(response).encode())
        cursor.close()

    
    def do_DELETE(self) -> None:
        

    
        user_id = self.path.split('/')[-1]  
        user_id = int(user_id)

        cursor = conn.cursor()
        cursor.execute("delete from users where id = %s returning id;", (user_id,))
        deleted_user = cursor.fetchone()
        conn.commit()

        if deleted_user:
            response = {
                "message": f"User with ID {user_id} deleted"
            }
            self.send_response(200)
        else:
            response = {
                "message": f"User with ID {user_id} not found"
            }
            self.send_response(404)    
    

        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        self.wfile.write(json.dumps(response).encode())
        cursor.close



def run(
        server_class: Type[HTTPServer] = HTTPServer,
        handler_class: Type[BaseHTTPRequestHandler] = SimpleRequestHandler,
        port: int = 8000
) -> None:
    server_address: tuple = ('0.0.0.0', port)
    httpd: HTTPServer = server_class(server_address, handler_class)
    print(f"Starting HTTP server on port {port}...")
    httpd.serve_forever()


if __name__ == '__main__':
    run()