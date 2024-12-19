import smtplib
import random 


class Mail:

    def __init__(self):
        self.credentials={
        "my_email" : "ehteshammohammed612@gmail.com",
        "password" : "kfmtconxcvlnvqck"        
        }

    
    def send_token(self,to_email_address):
        token = random.randint(1000, 9999)
        message = f"Hello,\n\nYour verification token is {token}. Please use this token to verify your account.\n\nBest regards,\nPragnya Admin/Faculty"
        
        connection = smtplib.SMTP("smtp.gmail.com",587)
        connection.starttls()
        connection.login(user=self.credentials['my_email'],password=self.credentials['password'])
        connection.sendmail(
            from_addr=self.credentials['my_email'],
            to_addrs=to_email_address,
            msg=f"Subject: Verification Token\n\n{message} "
            )
        connection.close() 
        return token

mail=Mail()
mail.send_token("ehteshammd089@gmail.com")