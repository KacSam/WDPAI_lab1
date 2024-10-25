import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Type


class SimpleRequestHandler(BaseHTTPRequestHandler):


    user_list = [{
        'id': 1,
        'firstName': 'Kacper',
        'lastName': 'Samolej',
        'role': 'student'
    }]

    next_id = 2


    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        self.wfile.write(json.dumps(self.user_list).encode())

   
    def do_POST(self) -> None:
        content_length: int = int(self.headers['Content-Length'])
        post_data: bytes = self.rfile.read(content_length)
        received_data: dict = json.loads(post_data.decode())

        
        new_user = {
            'id': self.next_id,
            'firstName': received_data.get('firstName'),
            'lastName': received_data.get('lastName'),
            'role': received_data.get('role')
        }

    
        self.user_list.append(new_user)
        SimpleRequestHandler.next_id += 1   

       
        response: dict = {
            "message": "New user added",
            "user": new_user
        }

        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        self.wfile.write(json.dumps(response).encode())

    
    def do_DELETE(self) -> None:


    
        user_id = self.path.split('/')[-1]  
        user_id = int(user_id)
    
        user_to_delete = next((user for user in self.user_list if user['id'] == user_id), None)

        if user_to_delete:
            self.user_list.remove(user_to_delete)
            response = {
                "message": f"User with ID {user_id} deleted."
            }
            self.send_response(200)
        else:
            response = {
                "message": f"User with ID {user_id} not found."
            }
            self.send_response(404)

        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        self.wfile.write(json.dumps(response).encode())



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
