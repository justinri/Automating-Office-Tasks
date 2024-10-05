from function_files.send_email import sendEmail
from money import Money

def AR_past_due(cursor, today):
    ### Getting JobBOSS data
    cursor.execute("SELECT * FROM Invoice_Header")
    table_Invoice_Headers = cursor.fetchall()

    ### creating a small data set to look over, i.e., optimizing
    ### If the due date is past and the amount owned is not zero, keep in table
    table_Invoice_Headers = [item for item in table_Invoice_Headers if item[12] > 0 and item[9].date() <= today]
    table_Invoice_Headers.sort(key=lambda x: x[9])

    # ### Creating top 10 owed list
    customersPastDueTotal = {item[1] : 0 for item in table_Invoice_Headers}
    for num, row in enumerate(table_Invoice_Headers):
        customerNum = row[1] 
        openAmount_curr_per = Money(amount=row[12], currency='USD')
        customersPastDueTotal[customerNum] = customersPastDueTotal[customerNum] + openAmount_curr_per
    email_text = ["Top 10 Customers Past Due: <br>"]
    email_text.append("Customer Number, Total Past Due <br>")
    email_text.append("<ol>")
    sort_orders = sorted(customersPastDueTotal.items(), key=lambda x: x[1], reverse=True)
    for num, item in enumerate(sort_orders):
        email_text.append("<li> {}, &#160; {}</li>".format(item[0], item[1].format('en_US')))
        if num >= 9: break
    email_text.append("</ol>")    

    #### Creating total list of past due invoices
    email_text.append("<br> <br>")
    email_text.append('Please double check the invoices below, <b> all <span style="color:red">{}</span> are past due </b>. <br>'.format(len(table_Invoice_Headers)))
    email_text.append("Note: The list below is in descending order. All open amounts equal to/over $1,000 are highlighted in red. <br>")
    email_text.append("Invoice Number, Customer Number, Open Amount, Due Date, Invoice Date, Terms <br>")
    email_text.append("<ol>")
    for num, row in enumerate(table_Invoice_Headers):
        InvoiceNum = row[0]
        customerNum = row[1] 
        terms = row[5]
        documentDate = row[7].date()
        dueDate = row[9].date()
        # origAmount = row[10]
        # openAmount = row[11]
        openAmount_curr_per = Money(amount=row[12], currency='USD')
        if openAmount_curr_per.amount >= 1000:
            email_text.append('<li> {}, &#160;{}, &#160;<span style="color:red"><b>{}</b></span>, &#160;{}, &#160;{}, &#160;{} </li>'.format(InvoiceNum, customerNum, openAmount_curr_per.format('en_US'), dueDate, documentDate, terms))
        else:
            email_text.append("<li> {}, &#160; {}, &#160; {}, &#160; {}, &#160; {}, &#160; {} </li>".format(InvoiceNum, customerNum, openAmount_curr_per.format('en_US'), dueDate, documentDate, terms))
    email_text.append("</ol>")

    ### Sending Email
    emailContent = "\n".join(email_text)
    whyEmail = "Past Due AR"
    sendEmail(whyEmail, emailContent, today, email_to)

    # cursor.execute("SELECT * FROM Invoice_Detail")
    # table_Invoice_Detail = cursor.fetchall()
    # print(table_Invoice_Detail[0])
    
    # cursor.execute("SELECT * FROM Invoice_Receipt")
    # table_Invoice_Receipt = cursor.fetchall()
    # print(table_Invoice_Receipt[0])
    return 0
