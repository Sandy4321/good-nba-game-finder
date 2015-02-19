import smtplib
import core
import private_info
import sys
import input_handler
import getopt

#sends an email through Gmail with the given message
def send_email(from_addr, to_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()

# controls what is in the body of the email, and to whom it is sent
# based on command line args
def execution_ctrl_message(message):
    arg = str(sys.argv[1])

    if arg == "custom":
        return input_handler.take_str_input("Enter custom message: ")

    return message

def execution_ctrl_to_send():
    arg = str(sys.argv[2])
    info_list = core.load_private_info()

    if arg == "me":
        return info_list["Email"]

    elif arg == "recipients":
        return info_list["Recipients"]

    else:
        return
    
    
def main():
    
    # controls who the information will be sent to based on command line args
    message = core.main()
    message = execution_ctrl_message(message)
    to_send = execution_ctrl_to_send()

    # sends an email to specified recipients containing a list
    # of good NBA matchups
    send_info = core.load_private_info()
    send_email(send_info["Email"],
               to_send, "NBA Daily",
               message, to_send, send_info["Password"])
main()
