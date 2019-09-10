import os
from FlaskApp import app


if __name__ == "__main__":
   app.run(host=os.getenv('IP', '127.0.0.1'), 
            port=int(os.getenv('PORT', 8080)),debug=True)

