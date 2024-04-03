import falcon
from auth import initialize_auth
 
# Initialize your Falcon application
app = falcon.App()
 
# Initialize your auth module (replace this with your actual initialization logic)
auth_app = initialize_auth()
 
# Add your auth app to the Falcon app
app.add_route('/auth', auth_app)
 
# Add other routes and middleware as needed
 
if __name__ == '__main__':
    # Run the Falcon app
    from wsgiref import simple_server
    httpd = simple_server.make_server('localhost', 8000, app)
    httpd.serve_forever()
