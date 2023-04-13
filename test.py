import dash
from dash import dcc
from dash import html
import dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import pdfkit
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
external_stylesheets = ['https://maxcdn.bootstrapcdn.com/bootswatch/4.5.2/journal/bootstrap.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

style = {'padding': '1.5em'}

app.layout = html.Div([
  html.P([html.Br()]),
  html.P([html.Br()]),
  dcc.Markdown('#### Please answer the following questions about your current symptoms'),
  dcc.Markdown('#### Questions are for patients undergoing prostate radiotherapy'),
  dcc.Markdown('Each form must be carefully filled out, results will be sent to your physician'),
  html.P([html.Br()]),
  dcc.Markdown('#### General Questions'),
  dcc.Markdown('###### How many radiation treatments have you had? It\'s okay if you don\'t know.'),
  dcc.Input(
      id='number_of_treatments',
      placeholder='Enter a value',
      type='text',
      value='ie 3, or I don\'t know'),

  dcc.Markdown('#### Symptom Questions'),
  dcc.Markdown('For each of the following question I\'m going to ask you to grade your symptoms.'),
  dcc.Markdown('#### Gas'),
    dcc.Markdown('###### In the last 7 days, did you have any INCREASED PASSING OF GAS (FLATULENCE)?'),
    dcc.RadioItems(
        id='gas',
        options=[
            {'label': 'Yes', 'value': 'Yes'},
            {'label': 'No', 'value': 'No'}
        ],
        value=None,
        labelStyle={'display': 'inline-block', 'margin-right': '10px'},
        inline=True
    ),
  dcc.Markdown('#### Diarrhea'),      
  dcc.Markdown('###### In the last 7 days, how OFTEN did you have LOOSE OR WATERY STOOLS (DIARRHEA)?'),
    dcc.RadioItems(
    id='diarrhea_frequency',
    options=[
        {'label': 'Never', 'value': 'Never'},
        {'label': 'Rarely', 'value': 'Rarely'},
        {'label': 'Occasionally', 'value': 'Occasionally'},
        {'label': 'Frequently', 'value': 'Frequently'},
        {'label': 'Almost constantly', 'value': 'Almost constantly'}
    ],
    value=None,
    labelStyle={'display': 'inline-block', 'margin-right': '10px'}
    ),

    dcc.Markdown('#### Abdominal Pain'),
    dcc.Markdown('###### In the last 7 days, how OFTEN did you have PAIN IN THE ABDOMEN (BELLY AREA)?'),
    dcc.RadioItems(
        id='abdominal_pain_frequency',
        options=[
            {'label': 'Never', 'value': 'Never'},
            {'label': 'Rarely', 'value': 'Rarely'},
            {'label': 'Occasionally', 'value': 'Occasionally'},
            {'label': 'Frequently', 'value': 'Frequently'},
            {'label': 'Almost constantly', 'value': 'Almost Constantly'}
        ],
        value=None,
        labelStyle={'display': 'inline-block', 'margin-right': '10px'}
    ),

    dcc.Markdown('###### In the last 7 days, what was the SEVERITY of your PAIN IN THE ABDOMEN (BELLY AREA) at its WORST?'),
    dcc.RadioItems(
        id='abdominal_pain_severity',
        options=[
            {'label': 'None', 'value': 'None'},
            {'label': 'Mild', 'value': 'Mild'},
            {'label': 'Moderate', 'value': 'Moderate'},
            {'label': 'Severe', 'value': 'Severe'},
            {'label': 'Very severe', 'value': 'Very severe'}
        ],
        value=None,
        labelStyle={'display': 'inline-block', 'margin-right': '10px'}
    ),

    dcc.Markdown('###### In the last 7 days, how much did PAIN IN THE ABDOMEN (BELLY AREA) INTERFERE with your usual or daily activities?'),
    dcc.RadioItems(
        id='abdominal_pain_adl',
        options=[
            {'label': 'Not at all', 'value': 'Not at all'},
            {'label': 'A little bit', 'value': 'A little bit'},
            {'label': 'Somewhat', 'value': 'Somewhat'},
            {'label': 'Quite a bit', 'value': 'Quite a bit'},
            {'label': 'Very much', 'value': 'Very much'}
        ],
        value=None,
        labelStyle={'display': 'inline-block', 'margin-right': '10px'}
    ),
  dcc.Markdown('Now let\'s discuss your urinary symptoms.'),
  dcc.Markdown('#### Urinary Symptoms'),
    dcc.Markdown('##### Painful Urination'),
    dcc.Markdown('###### In the last 7 days, what was the SEVERITY of your PAIN OR BURNING WITH URINATION at its WORST?'),
    dcc.RadioItems(
        id='painful_urination_severity',
        options=[
            {'label': 'None', 'value': 'None'},
            {'label': 'Mild', 'value': 'Mild'},
            {'label': 'Moderate', 'value': 'Moderate'},
            {'label': 'Severe', 'value': 'Severe'},
            {'label': 'Very severe', 'value': 'Very severe'}
        ],
        value=None,
        labelStyle={'display': 'inline-block', 'margin-right': '10px'}
    ),

    dcc.Markdown('##### Urinary Urgency'),
    dcc.Markdown('###### In the last 7 days, how OFTEN did you feel an URGE TO URINATE ALL OF A SUDDEN?'),
    dcc.RadioItems(
        id='urinary_urgency_frequency',
        options=[
            {'label': 'Never', 'value': 'Never'},
            {'label': 'Rarely', 'value': 'Rarely'},
            {'label': 'Occasionally', 'value': 'Occasionally'},
            {'label': 'Frequently', 'value': 'Frequently'},
            {'label': 'Almost constantly', 'value': 'Almost constantly'}
        ],
        value=None,
        labelStyle={'display': 'inline-block', 'margin-right': '10px'}
    ),

    dcc.Markdown('###### In the last 7 days, how much did SUDDEN URGES TO URINATE INTERFERE with your usual or daily activities?'),
    dcc.RadioItems(
        id='urinary_urgency_adl',
        options=[
            {'label': 'Not at all', 'value': 'Not at all'},
            {'label': 'A little bit', 'value': 'A little bit'},
            {'label': 'Somewhat', 'value': 'Somewhat'},
            {'label': 'Quite a bit', 'value': 'Quite a bit'},
            {'label': 'Very much', 'value': 'Very much'}
        ],
        value=None,
        labelStyle={'display': 'inline-block', 'margin-right': '10px'}
    ),

    dcc.Markdown('##### Urinary Frequency'),
    dcc.Markdown('###### In the last 7 days, were there times when you had to URINATE FREQUENTLY?'),
    dcc.RadioItems(
        id='urinary_frequency',
        options=[
            {'label': 'Never', 'value': 'Never'},
            {'label': 'Rarely', 'value': 'Rarely'},
            {'label': 'Occasionally', 'value': 'Occasionally'},
            {'label': 'Frequently', 'value': 'Frequently'},
            {'label': 'Almost constantly', 'value': 'Almost constantly'}
        ],
        value=None,
        labelStyle={'display': 'inline-block', 'margin-right': '10px'}
    ),

    dcc.Markdown('###### In the last 7 days, how much did FREQUENT URINATION INTERFERE with your usual or daily activities?'),
    dcc.RadioItems(
        id='urinary_frequency_interference',
        options=[
            {'label': 'Not at all', 'value': 'Not at all'},
            {'label': 'A little bit', 'value': 'A little bit'},
            {'label': 'Somewhat', 'value': 'Somewhat'},
            {'label': 'Quite a bit', 'value': 'Quite a bit'},
            {'label': 'Very much', 'value': 'Very much'}
        ],
        value=None,
        labelStyle={'display': 'inline-block', 'margin-right': '10px'}
    ),

    dcc.Markdown('##### Change in Usual Urine Color'),
    dcc.Markdown('###### In the last 7 days, did you have any URINE COLOR CHANGE?'),
    dcc.RadioItems(
        id='urine_color_change',
        options=[
            {'label': 'Yes', 'value': 'Yes'},
            {'label': 'No', 'value': 'No'}
        ],
        value=None,
        labelStyle={'display': 'inline-block', 'margin-right': '10px'}
    ),

    dcc.Markdown('##### Urinary Incontinence'),
    dcc.Markdown('###### In the last 7 days, how OFTEN did you have LOSS OF CONTROL OF URINE (LEAKAGE)?'),
    dcc.RadioItems(
        id='urinary_incontinence_frequency',
        options=[
            {'label': 'Never', 'value': 'Never'},
            {'label': 'Rarely', 'value': 'Rarely'},
            {'label': 'Occasionally', 'value': 'Occasionally'},
            {'label': 'Frequently', 'value': 'Frequently'},
            {'label': 'Very much', 'value': 'Very much'},
            {'label': 'Almost constantly', 'value': 'Almost constantly'}
        ],
        value=None,
        labelStyle={'display': 'inline-block', 'margin-right': '10px'}
    ),

    dcc.Markdown('###### In the last 7 days, how much did LOSS OF CONTROL OF URINE (LEAKAGE) INTERFERE with your usual or daily activities?'),
    dcc.RadioItems(
        id='urinary_incontinence_interference',
        options=[
            {'label': 'Not at all', 'value': 'Not at all'},
            {'label': 'A little bit', 'value': 'A little bit'},
            {'label': 'Somewhat', 'value': 'Somewhat'},
            {'label': 'Quite a bit', 'value': 'Quite a bit'},
            {'label': 'Very much', 'value': 'Very much'}
        ],
        value=None,
        labelStyle={'display': 'inline-block', 'margin-right': '10px'}
    ),
  html.P([html.Br()]),  

  html.Br(),
    html.Button('Submit', id='submit_button', n_clicks=0),
    html.Br(),
    html.Br(),
    dcc.Markdown('#### Survey Results'),
    dash_table.DataTable(
        id='results_table',
        columns=[
            {'name': 'Question', 'id': 'question'},
            {'name': 'Answer', 'id': 'answer'}
        ],
        data=[],
        style_cell={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        }
),
  html.P([html.Br()])
])

@app.callback(
    Output('results_table', 'data'),
    Input('submit_button', 'n_clicks'),
    State('number_of_treatments', 'value'),
    State('gas', 'value'),
    State('diarrhea_frequency', 'value'),
    State('abdominal_pain_frequency', 'value'),
    State('abdominal_pain_severity', 'value'),
    State('abdominal_pain_adl', 'value'),
    State('painful_urination_severity', 'value'),
    State('urinary_urgency_frequency', 'value'),
    State('urinary_urgency_adl', 'value'),
    State('urinary_frequency', 'value'),
    State('urinary_frequency_interference', 'value'),
    State('urine_color_change', 'value'),
    State('urinary_incontinence_frequency', 'value'),
    State('urinary_incontinence_interference', 'value')
)
def update_results_table(n_clicks, *responses):
    if n_clicks == 0:
        return []

    questions = [
        'Number of Radiation treatments',
        'Increased passing of gas',
        'Diarrhea frequency',
        'Abdominal pain frequency',
        'Abdominal pain severity',
        'Abdominal pain interference',
        'Painful urination severity',
        'Urinary urgency frequency',
        'Urinary urgency interference',
        'Urinary frequency',
        'Urinary frequency interference',
        'Urine color change',
        'Urinary incontinence frequency',
        'Urinary incontinence interference',
    ]

    data = [{'question': question, 'answer': response} for question, response in zip(questions, responses)]

    # Convert data to a Pandas DataFrame
    df = pd.DataFrame(data)
    '''below is for pdf stuff'''
    # # Export DataFrame to an HTML file
    # with open("table.html", "w") as file:
    #     file.write(df.to_html(index=False))

    # # Convert the HTML file to a PDF
    # pdfkit.from_file("table.html", "table.pdf")

    # # Email the PDF file
    # #send_email("recipient@example.com", "table.pdf")

    return data

def send_email(to_email, pdf_file):
    from_email = "you@example.com"  # Your email address. 
    password = "your_password"  # Your email password. Can consider using SendGrid for better security.

    # Create a multipart email message
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = "Patient Symptom Table PDF"

    # Attach the PDF file
    with open(pdf_file, "rb") as file:
        attachment = MIMEBase("application", "octet-stream")
        attachment.set_payload(file.read())
        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", f"attachment; filename={pdf_file}")
        msg.attach(attachment)

    # Send the email
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(from_email, password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()


if __name__ == '__main__':
    app.run_server(debug=True)