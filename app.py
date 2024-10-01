from pragnya_responsive_app import create_app
import os 
from flask_login import LoginManager



app = create_app()



if __name__=="__main__":
 

    app.run(debug=True)



    
