import datetime
import emails

#******************************** Only Edit **************************/
def emailInfo(whyEmail, emailContent, today):
    if whyEmail == "Shipping Error":
        packlist = emailContent[0]
        trackNumShipto = emailContent[1]
        soNumShipto = emailContent[2]

        SUBJECT = 'WARNING: Packlist: #{}'.format(packlist)
        CONTENT   = """
        <p>
        <b>Please double check that packlist #: {} is going to the correct city.<br></b>
        Tracking number, ship-to city: {}, {} <br> 
        Sales order, ship-to city: {}, {} <br> 
        </p>
        """.format(packlist, trackNumShipto[0], trackNumShipto[1], soNumShipto[0], soNumShipto[1])
    elif whyEmail == "API ship city Error":
        packlist = emailContent[0]
        trackNumShipto = emailContent[1]

        SUBJECT = 'WARNING: Packlist: #{}'.format(packlist)
        CONTENT   = """
        <p>
        <b>Please double check that packlist #: {} is going to the correct city.<br></b>
        The ship-to city could not be found using the tracking number: {}
        </p>
        """.format(packlist, trackNumShipto)
        
    elif whyEmail == "Past Due AR":
        SUBJECT = 'WARNING: ARs Past Due'
        CONTENT   = emailContent

    elif whyEmail == "PO Receiving Past Due":
        SUBJECT = 'WARNING: PO Receiving Past Due'
        CONTENT   = emailContent

    else:   ### If we cannot find an if statement to write to, there was an error
        with open("error_log.txt", "a") as myfile:
            myfile.write("{}: Could not find an if/elif statement to send email to. whyEmail: {} \n".format(today, whyEmail))
            
    return SUBJECT, CONTENT

def sendEmail(whyEmail, emailContent, today, email_to = ["removed..."]):
	####********************Sending the email************************************/
	# Here goes the configuration of your email provider.
	# Look online to find it.
	# For instance for Yahoo!Mail:
	SMTP_SERVER   = 'smtp.mail.yahoo.com'
	SMTP_LOGIN    = 'removed...'
	SMTP_PASSWORD = 'removed...'  # Have to use a app password: https://mail.yahoosmallbusiness.com/accountinfo
	SENDER_NAME  = 'No_Reply'
	SENDER_EMAIL = 'removed...'
	RECIPIENT = email_to
	SUBJECT, CONTENT  = emailInfo(whyEmail, emailContent, today)

	message = emails.html(
		subject=SUBJECT, 
		html=CONTENT, 
		mail_from=(SENDER_NAME, SENDER_EMAIL)
	)

	config = {
		'host': SMTP_SERVER,
		'timeout': 5,
		'ssl': True,
		'user': SMTP_LOGIN,
		'password': SMTP_PASSWORD
	}

	r = message.send(to=RECIPIENT, smtp=config)

#		if r.success:
#			print('Email #{} sent!'.format(emailSent))
#			emailSent += 1
#		else:
#			print('Something wrong happened')
#			print('Here is the smtp status code', r.status_code)
	return 0
