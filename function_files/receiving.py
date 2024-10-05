from datetime import datetime, timedelta
from function_files.send_email import sendEmail

def PO_receiving_past_due(cursor, today):

    ### Getting JobBOSS data
    cursor.execute("SELECT * FROM PO_Detail")
    table_PO_Detail = cursor.fetchall()
    cursor.execute("SELECT * FROM PO_Header")
    table_PO_Headers = cursor.fetchall()

    ### creating a small data set to look over, i.e., optimizing
    table_PO_Detail = [item for item in table_PO_Detail if item[9].date() < today and item[4] != 'Closed']  
    table_PO_Headers = [item for item in table_PO_Headers if item[11].date() < today and item[14] != 'Closed']           

    ### Getting information about over due POs
    PO_info = []
    for num, row in enumerate(table_PO_Headers):
        PO = row[0]
        for num2, row2 in enumerate(table_PO_Detail):
            if PO == row2[2]:
                vendor = row[1]
                orderDate = row[10]
                dueDate = row[11]
                description = row2[22]
                PO_info.append([PO, vendor, dueDate, orderDate, description])
                break
    PO_info.sort(key=lambda x: x[2])
        
    #### Creating total list of past due POs
    minus30Days = today - timedelta(days=30)
    email_text = ["<br> <br>"]
    email_text.append('Please double check the POs below, <b> all <span style="color:red">{}</span> are past due </b>. <br>'.format(len(PO_info)))
    email_text.append("Note: All open POs equal to/over 30 days past due are highlighted in red. <br>")
    email_text.append("PO Number, Vender, Due Date, Order Date, Description<br>")
    email_text.append("<ol>")
    for row in PO_info:
        PO = row[0]
        vendor = row[1]
        dueDate = row[2].date()
        orderDate = row[3].date()
        description = row[4]
        if minus30Days > dueDate:
            email_text.append('<li> {}, &#160; {}, &#160;<span style="color:red"><b>{}</b></span>, &#160;{}, &#160;{} </li>'.format(PO, vendor, dueDate, orderDate, description))
        else:
            email_text.append("<li> {}, &#160; {}, &#160; {}, &#160; {}, &#160;{} </li>".format(PO, vendor, dueDate, orderDate, description))
    email_text.append("</ol>")

    ### Sending Email
    emailContent = "\n".join(email_text)
    whyEmail = "PO Receiving Past Due"
    sendEmail(whyEmail, emailContent, today, email_to)
    return 0 
