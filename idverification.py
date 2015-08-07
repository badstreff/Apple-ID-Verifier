import imaplib
import email
import datetime
import http.cookiejar
import urllib.request
import urllib.parse
import urllib.error
import time
import sys

criteria = '(FROM "appleid@id.apple.com") (SUBJECT "Verify")'


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def parseVerificationURL(email_content):
    '''
    Parses the email sent by apple and returns the URL to verify
    the apple id.
    '''
    c = email_content.as_string()
    raw_key = c[c.find('key=3D'):c.find('=3D=3D')]
    raw_key = raw_key.replace('=\n', '')
    raw_key = raw_key.replace('=3D', '=')
    final_key = raw_key.replace('key=', '')

    final_url = ('https://id.apple.com/cgi-bin/verify.cgi?language=3DUS-EN&' +
                 'key=' + final_key + '&type=DFT&_C=USA&_L=en_US')
    return final_url


def resendVerificationEmail(user, password):
    '''
    Resends the verification email from apple. This should only be called
    if the previous email has expired.

    TODO: Add checking to ensure email account has not already been verified.
    '''
    # new post data to id.apple.com :(
    print(bcolors.FAIL + 'WARNING:\tUser ' + user + ' will not be processed.' + bcolors.ENDC)
    print('WARNING:\tVerification email will be resent, run the script at a later time to verify the address.')

    # Statis URL to redirect to the actual sign in page
    signin_redirect_url = 'https://appleid.apple.com/signin'

    # Collect cookies
    cj = http.cookiejar.CookieJar()

    # Initial Request to get appIdKey
    req = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    r = req.open(signin_redirect_url)
    signin_url = r.geturl()
    appIdKey = signin_url[signin_url.find('Key=')+4:signin_url.find('&')]
    r.close()

    # Login to apple id
    req = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 \
                Safari/537.36",
               "Connection": "keep-alive",
               "Referer": signin_url}
    data = urllib.parse.urlencode({'appleId': user,
                                   'accountPassword': password,
                                   'appIdKey': appIdKey,
                                   'accNameLocked': 'false',
                                   'openiForgotInNewWindow': 'false'})
    data = data.encode('utf-8')
    req.addheaders = list(headers.items())
    r = req.open('https://idmsa.apple.com/IDMSWebAuth/authenticate', data)

    # Some sort of checksum(?) that needs posted along with the resend button
    scnt = r.info()['scnt']

    r.close()

    # Submit request to resend verification email
    req = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    data = urllib.parse.urlencode({'accountName': user,
                                   'scnt': scnt,
                                   '_method': 'POST'})
    data = data.encode('utf-8')
    try:
        r = req.open('https://appleid.apple.com/account/verify/email', data)
        r.close()
    except urllib.error.URLError as e:
        print('CRITICAL:\t' + e.reason)
        print(bcolors.FAIL + 'CRITICAL:\tFatal error occured while resending verification email' + bcolors.ENDC)
        r.close()
        return

    if r.status == 200:
        print('INFO:\tNew email request was sent successfully')
    r.close()


def getURLFromEmail(user, password):
    '''
    If no valid email is found returns ''
    '''
    print('INFO:\tLocating email for: ' + user)
    url = ''
    M = imaplib.IMAP4_SSL('imap.gmail.com')

    try:
        M.login(user, password)
    except:
        print(bcolors.FAIL + "Login failed, please verify " + user + "'s email credentials" + bcolors.ENDC)
        return url

    rv, data = M.select('INBOX')
    if rv == 'OK':
        # select the first email found if one exist
        typ, data = M.search(None, criteria)
        try:
            verification_email = data[0].split()[0]
            rv, data = M.fetch(verification_email, '(RFC822)')
            content = email.message_from_bytes(data[0][1])
            latest_sent_date = getEmailDate(content)
            url = parseVerificationURL(content)
        except:
            print("Error:\tNo email found")
            resendVerificationEmail(user, password)
            return url

        # select the latest email for parsing
        typ, data = M.search(None, criteria)
        for item in data[0].split():
            rv, data = M.fetch(item, '(RFC822)')
            content = email.message_from_bytes(data[0][1])
            if getEmailDate(content) > latest_sent_date:
                # print('INFO:\tFound a newer email the the first')
                latest_sent_date = getEmailDate(content)
                url = parseVerificationURL(content)

        if (latest_sent_date <
                datetime.datetime.now()-datetime.timedelta(days=3)):
            print(bcolors.WARNING + 'ERROR:\t\tThis email is older than 3 ' +
                  'days and is no longer valid' + bcolors.ENDC)
            resendVerificationEmail(user, password)
            return ''
    else:
        print('INBOX not found')
    M.logout()
    if url != '':
        print('INFO:\tValid email found for ' + user)
    return url


def getEmailDate(content):
    # Format date so it can be used for checking
    time_tuple = email.utils.parsedate_tz(content['Date'])
    date_sent = datetime.datetime.fromtimestamp(
        email.utils.mktime_tz(time_tuple))
    return date_sent


def submitVerification(referer_url, user, password):
    '''
    Verifies an apple id for the given url.
    '''
    print('INFO:\tAttempting to submit verification to apple for ' + user)

    if(checkIfPreviouslyVerified(referer_url)):
        print('INFO:\t' + user + ' previously verified. Skipping.')
        return

    post_url = 'https://id.apple.com/IDMSEmailVetting/authenticate.html;'
    # Collecting Cookies
    cj = http.cookiejar.CookieJar()

    # Get JSESSION Cookie string
    req = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    r = req.open(url)
    jsession = r.info().get_all('Set-Cookie')[1].split(';')[0]
    r.close()

    # Constructing URL & POST DATA
    post_url += jsession
    headers = {"Referer": url,
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 \
                Safari/537.36"}
    data = urllib.parse.urlencode({'appleId': user,
                                   'accountPassword': password})
    data = data.encode('utf-8')
    req = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    req.addheaders = list(headers.items())

    # POST the data
    try:
        r = req.open(post_url, data)
        response = str(r.read())
        if ('Email address previously verified.' in response or
                'Email address verified.' in response):
            print(bcolors.OKGREEN + 'SUCCESS:\t' + user + ' is ready for use' + bcolors.ENDC)
        r.close()
    except:
        print(bcolors.FAIL + "CRITICAL:\tFatal error occured while verifying email" + bcolors.ENDC)
        r.close()


def checkIfPreviouslyVerified(url):
    r = urllib.request.urlopen(url)
    if 'Email address previously verified.' in str(r.read()):
        r.close()
        return True
    r.close()
    return False


if __name__ == "__main__":
    count = 0
    start_time = int(time.time())

    with open(str(sys.argv[1])) as f:
        for line in f:
            count += 1
            token = line.split(',')
            user = token[0].strip()
            email_password = token[1].strip()
            id_password = token[2].strip()

            url = getURLFromEmail(user, email_password)
            if(url == ''):
                print('ERROR:\tUnable to process ' + user + ' at this time. No url found.')
            else:
                print('DEBUG: ' + url)
                submitVerification(url, user, id_password)

    elapsed_time = int(time.time()) - start_time

    print('completed ' + str(count) + " id's")
    print('total time elapsed: ' + str(elapsed_time) + 's')
