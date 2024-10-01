from pragnya_responsive_app import create_app
import os 
from flask_login import LoginManager



app,socket = create_app()



if __name__=="__main__":
 

    socket.run(app, host='0.0.0.0', port=5000, debug=True)

    # app.run(debug=True)



    
