import html
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_host = "smtpgw.bnl.gov"
smtp_port = 25
message_from = "iss@bnl.gov"

def send_email_message(PI_email=None, proposal_number=None, html=None):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"ISS beamline data for Proposal {proposal_number}"
    msg["From"] = "iss@bnl.gov"
    msg["To"] = f"{PI_email}"
    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.send_message(msg)


def create_message(PI=None, working_directory=None, zip_id_file=None):
    PI = PI
    working_directory = working_directory
    zip_id_file = zip_id_file
    html = f"""
    <html>
    <body>
        <p>Dear {PI},</p>

        <p>
        You can download the results of your experiment from JupyterHub by following the steps below:
        </p>

        <ol>
            <li>
                Go to <a href="https://jupyter.nsls2.bnl.gov">JupyterHub</a>
                and log in using your BNL credentials.
            </li>
            <li>
                Click on <b>Start My Server</b> to launch a new server or relaunch an already active server.
            </li>
            <li>
                In the <b>Server Options</b> window, select <b>Pluto Cluster</b> as the job profile,
                then click <b>Start</b>.
            </li>
            <li>
                In the <b>File</b> menu, select <b>Open from Path...</b>.
            </li>
            <li>
                Copy and paste the following path:
                <br>
                <code>{working_directory}</code>
            </li>
            <li>
                Right-click on the zip file named <b>{zip_id_file}</b>
                and download it to your PC.
            </li>
        </ol>

        <p>Sincerely,</p>
        <p>ISS Staff</p>
    </body>
    </html>
    """
    return html






def create_zip(self):
    _, _current_user = self.user_manager.current_user()
    proposal = (_current_user['runs'][-1]['proposal'])

    year = self.RE.md['year']
    cycle = self.RE.md['cycle']
    proposal = self.RE.md['proposal']
    PI = self.RE.md['PI']
    email_address = self.lineEdit_email.text()
    # working_directory = f'/nsls2/xf08id/users/{year}/{cycle}/{proposal}'
    working_directory = f'{ROOT_PATH}/{USER_PATH}/{year}/{cycle}/{proposal}'
    zip_file = f'{working_directory}/{proposal}.zip'
    id = str(uuid.uuid4())[0:5]
    zip_id_file = f'{proposal}-{id}.zip'

    if os.path.exists(zip_file):
        os.remove(zip_file)

    # os.system(f'zip {zip_file} {working_directory}/*.* ')

    print('Creating a zip file')
    os.system(f"cd '{working_directory}'; zip '{zip_id_file}' *.dat")

    message = create_html_message(
        'staff08id@gmail.com',
        email_address,
        f'ISS beamline data for Proposal {proposal}\n',
        f' <p> Dear {PI},</p> <p>You can download the results of your experiment from JupyterHub by following the steps below: </p>'
        f'<p> 1. Go to https://jupyter.nsls2.bnl.gov and log in using your BNL credentials. </p>'
        f'<p> 2. Click on "Start My Server" to launch a new server or relaunch an already active server. </p>'
        f'<p> 3. In the "Server Options" window, select "Pluto Cluster" as the job profile, then click "Start".</p>'
        f'<p> 4. In the File menu, select "Open from Path..." </p>'
        f'<p> 5. Copy and paste the following path (without quotation marks): "{working_directory}" </p>'
        f'<p> 6. Right-click on the zip file named {zip_id_file} and download it to your PC. </p> '
        f'<p> Sincerely, </p> <p> ISS Staff </p>'
    )

    draft = upload_draft(self.parent.gmail_service, message)
    sent = send_draft(self.parent.gmail_service, draft)
    print('Email sent for zip files')