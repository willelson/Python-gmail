""" Show gmail activity in last 30 days """
import imaplib
import email
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import getpass

def last30(dict):
    """Fill a dictionary with last 30 dates (datetime.date() objects)"""
    today = datetime.date.today()
    for n in range(30):
        day = today - datetime.timedelta(days = n)
        dict[day] = 0    
    return dict

def str_to_datetime(date):
    """turn date from email into datetime.date() object"""
    if date[6] == ' ':
        date = date[:5] +'0'+ date[5:]
    return datetime.datetime.strptime(date[:25],
                                      '%a, %d %b %Y %H:%M:%S').date()

def msgCount(IMAP4obj, dict):
    """Update dict with msg count"""
    rv, data = IMAP4obj.search(None, "ALL")
    if rv != 'OK':
        print "No messages found!"
        return
    today = datetime.date.today()
    for num in reversed(data[0].split()):
        rv, data = IMAP4obj.fetch(num, '(RFC822)')
        msg = email.message_from_string(data[0][1])
        date = str_to_datetime(msg['Date'])
        if today - date > datetime.timedelta(days = 30):
            break
        else:
            dict[date] += 1
    
    return dict

def checkMail(IMAP4obj, mailbox, dict):
    """Count messages in specific mailbox"""
    rv, data = IMAP4obj.select(mailbox)
    if rv == 'OK':
        msgCount(IMAP4obj, dict)
        M.close()

def plot(ax, x, y, max_y, title = None, color = 'r'):
    ax.set_title(title)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5)) 
    plt.bar(x, y, align='center', color = color) 
    plt.yticks(range(0, max_y + 2))
            
            
if __name__ == "__main__":
    sent = {}
    inbox = {}
    last30(sent)
    last30(inbox)
    M = imaplib.IMAP4_SSL('imap.gmail.com')
    username = raw_input('Username: ')   
    password = getpass.getpass()
    try:
        M.login(username, password)
        print "login succussful"
    except:
        print "Error: login failed"

    checkMail(M, "[Gmail]/Sent Mail", sent)
    checkMail(M, "INBOX", inbox)
    
    # Plot with matplotlib
    fig = plt.figure()
    width = 0.2  
    if sent[max(sent, key = sent.get)] > inbox[max(inbox,
                                                   key = inbox.get)]:
        max_y = sent[max(sent, key = sent.get)]
    else:
        max_y = inbox[max(inbox, key = inbox.get)]
    
    x_sent = [mdates.date2num(date) for (date, value)
              in sorted(sent.items())]
    y_sent = [value for (date, value) in sorted(sent.items())]
    
    ax_sent = plt.subplot(211)
    plot(ax_sent, x_sent, y_sent, max_y, 'Sent mail', 'r')
    
    x_in = [mdates.date2num(date) for (date, value)
            in sorted(inbox.items())]
    y_in = [value for (date, value) in sorted(inbox.items())]
    
    ax_in = plt.subplot(212)
    plot(ax_sent, x_in, y_in, max_y, 'Mail recieved', 'b')

    plt.tight_layout()
    plt.show()   
    M.logout()


    
