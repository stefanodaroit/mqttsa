import fpdf
from fpdf import FPDF, HTMLMixin

# Create pdf report to show the results in a readable way
# The content of the pdf has to be written following the 
# HTML standard. It will be converted in pdf at the end, 
# using output_pdf()

class MyFPDF(FPDF, HTMLMixin):
    pass

# parameters for the pdf
pdf = MyFPDF()
font_size = 11
html = ''
check = False


# initialize the structure of the pdf and append the title of the report in an HTML format
def init():
    global html
    global check
    pdf.add_page()
    html += '<H1 align="center">MQTTSA Report</H1>'
    check = True

# append a paragraph to the HTML 
def add_paragraph(title, msg=None):
    global html
    global check
    if check == False:
        init()
    if msg != None:
        html += '<h2 align="left">'+title+"</h2><font size="+str(font_size)+">"+msg+'</p><br>'
    else:
        html += '<h2 align="left">'+title+'</h2>'
       
# Create summary table
def add_summary_table(title, IP, Port, Listening, Msg, Interface, MD, DoS, Brute, outdated, implements_TLS, disclosure, weak_ac, no_pass, cred_sniffed_or_bruteforced, client_key):
    global html
    
    Rating = 0
    
    # If it managed to connect (excluding when provided with X.509 certificates)
    if (weak_ac):
        Rating += 8
        if(client_key):
            Rating -= 8
        # But no password
        if(no_pass):
            Rating += 2
        # Or using hijacked credentials
        if(cred_sniffed_or_bruteforced):
            Rating += 4

    # E.g., when providing only CA certificate
    if(implements_TLS):
        Rating -= 4
    # Implies no ACL
    if(disclosure):
        Rating += 2
        
    if (Rating <=0):
        Rating = "Null or not evaluable"
    elif (Rating <3):
        Rating = "LOW"
    elif (Rating <7):
        Rating = "MEDIUM"
    else:
        Rating = "HIGH"
    
    html += '<h4 align="left">'+title+'</h4>'\
        '<table width="100%">'\
        '    <tr width="100%">'\
        '      <th width="50%"><center>Test configuration</center></th>'\
        '      <th width="50%"><center>Vulnerabilities</center></th>'\
        '    </tr>'\
        '    <tr width="100%">'\
        '      <td width="25%">Broker IP and port</td>'\
        '      <td width="25%">'+ IP +':'+ Port +'</td>'\
        '      <td width="25%">&nbsp;&nbsp;&nbsp;Outdated Broker</td>'\
        '      <td width="25%"><center>' + outdated + '</center></td>'\
        '    </tr>'\
        '    <tr width="100%">'\
        '        <td width="25%">Listening time</td>'\
        '        <td width="25%">' + Listening + ' seconds </td>'\
        '        <td width="25%">&nbsp;&nbsp;&nbsp;Use of TLS</td>'\
        '        <td width="25%"><center>'+ str(implements_TLS) +'*</center></td></tr>'\
        '    <tr width="100%">'\
        '        <td width="25%">Message to send</td>'\
        '        <td width="25%">' + Msg + '</td>'\
        '        <td width="25%">&nbsp;&nbsp;&nbsp;Information Disclosure</td>'\
        '        <td width="25%"><center>'+ disclosure +'</center></td></tr>'\
        '    <tr width="100%">'\
        '        <td width="25%">Sniffing interface</td>'\
        '        <td width="25%">' + Interface + '</td>'\
        '        <td width="25%">&nbsp;&nbsp;&nbsp;Accessible service</td>'\
        '        <td width="25%"><center>'+ str(weak_ac) +'</center></td></tr>'\
        '    <tr width="100%">'\
        '        <td width="25%">Data/Msg tampering</td>'\
        '        <td width="25%">' + MD + '</td>'\
        '        <td width="50%">&nbsp;&nbsp;&nbsp;or weak Access Control</td></tr>'\
        '    <tr width="100%">'\
        '        <td width="25%">DoS connections</td>'\
        '        <td width="25%">' + DoS + '</td>'\
        '        <td width="25%">&nbsp;&nbsp;&nbsp;Overall risk</td>'\
        '        <td width="25%"><center>'+ Rating +'</center></td></tr>'\
        '    <tr width="100%">'\
        '        <td width="25%">Brute-forcing</td>'\
        '        <td width="25%">' + Brute + '</td>'\
        '</table>' +"<font size="+str(font_size)+"><br>*: False if not providing X.509 certificates or according to the broker implementation (e.g., Mosquitto). Verify with TLS Assistant (<a href=\"https://github.com/stfbk/tlsassistant\">https://github.com/stfbk/tlsassistant</a>).</font><br></p><br>"

# append a sub-paragraph to the HTML
def add_sub_paragraph(title, msg=None):
    global html
    if msg != None:
        html += '<h4 align="left">'+title+"</h4><font size="+str(font_size)+">"+msg+'</p><br>'
    else:
        html += '<h4 align="left">'+title+'</h4>'

# append to an existing paragraph of the HTML
def add_to_existing_paragraph(msg):
    global html
    html += "<font size="+str(font_size)+">"+msg+'</font><br>'

# generate the pdf using the HTML
def output_pdf(fingerprint):
    global html
    
    html = html.replace("Replace_up_to_date", fingerprint)
    
    pdf.write_html(html.encode('utf-8').decode('latin-1'))
    pdf.output("report.pdf")
