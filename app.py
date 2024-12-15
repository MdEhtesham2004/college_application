from pragnya_responsive_app import create_app
import os 
from flask_login import LoginManager
RENDER_API_KEY="rnd_o8bcbIKkQ9kzenLPKwXGY6eQ1X4z"


app = create_app()



if __name__=="__main__":
    app.run(debug=True)



    
