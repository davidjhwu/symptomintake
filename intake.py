import dash
from dash import dcc
from dash import html
import dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import openai
import os

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
# import pdfkit
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
# from email import encoders
external_stylesheets = ['https://maxcdn.bootstrapcdn.com/bootswatch/4.5.2/journal/bootstrap.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
server = app.server

style = {
    'padding': '3.5em',
    'backgroundColor': '#e3d8df',  
    'fontFamily': 'Arial, sans-serif'
}

app.layout = html.Div([
dcc.Markdown('# Prostate Radiotherapy Patient Symptom Intake Form'),
  html.P([html.Br()]),
  dcc.Markdown('#### Please answer the following questions about your current symptoms'),
  dcc.Markdown('Each form must be carefully filled out, results will be sent to your physician'),
  dcc.Markdown('#### General Questions'),
  dcc.Markdown('###### How many radiation treatments have you had? It\'s okay if you don\'t know.'),
  dcc.Input(
      id='number_of_treatments',
      placeholder='Enter a value',
      type='text',
      value='ie 3, or I don\'t know'),
  html.P([html.Br()]),
  dcc.Markdown('### Symptom Questions'),
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
  html.P([html.Br()]),
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
    dcc.Markdown("#### Radiation Skin Reaction"),
    dcc.Markdown(
        "###### In the last 7 days, what was the SEVERITY of your SKIN BURNS FROM RADIATION at their WORST?"
    ),
    dcc.RadioItems(
        id="radiation_skin_reaction_severity",
        options=[
            {"label": "None", "value": "None"},
            {"label": "Mild", "value": "Mild"},
            {"label": "Moderate", "value": "Moderate"},
            {"label": "Severe", "value": "Severe"},
            {"label": "Very severe", "value": "Very severe"},
            {"label": "Not applicable", "value": "Not applicable"},
        ],
        value=None,
        labelStyle={"display": "inline-block", "margin-right": "10px"},
    ),
    html.P([html.Br()]),
    dcc.Markdown("#### Fatigue"),
    dcc.Markdown(
        "###### In the last 7 days, what was the SEVERITY of your FATIGUE, TIREDNESS, OR LACK OF ENERGY at its WORST?"
    ),
    dcc.RadioItems(
        id="fatigue_severity",
        options=[
            {"label": "None", "value": "None"},
            {"label": "Mild", "value": "Mild"},
            {"label": "Moderate", "value": "Moderate"},
            {"label": "Severe", "value": "Severe"},
            {"label": "Very severe", "value": "Very severe"},
        ],
        value=None,
        labelStyle={"display": "inline-block", "margin-right": "10px"},
    ),

    dcc.Markdown(
        "###### In the last 7 days, how much did FATIGUE, TIREDNESS, OR LACK OF ENERGY INTERFERE with your usual or daily activities?"
    ),
    dcc.RadioItems(
        id="fatigue_interference",
        options=[
            {"label": "Not at all", "value": "Not at all"},
            {"label": "A little bit", "value": "A little bit"},
            {"label": "Somewhat", "value": "Somewhat"},
            {"label": "Quite a bit", "value": "Quite a bit"},
        ],
        value=None,
        labelStyle={"display": "inline-block", "margin-right": "10px"},
    ),
    html.P([html.Br()]),
    dcc.Markdown('#### Last Question!'),
    dcc.Markdown('###### Finally, do you have any other symptoms that you wish to report?'),
    dcc.Input(
        id='additional_symptoms',
        placeholder='Type here...',
        type='text',
        value=''),
    html.P([html.Br()]),  
    html.Div(className="d-grid gap-2 d-flex justify-content-center", children=[
        dcc.Loading(id="loading", type="circle", children=[
            html.Button("Submit", id="submit_button", n_clicks=0, className="btn btn-lg btn-primary", style={"width": "200px"})
        ]),
    ]),
    html.Br(),
    html.Div([
        html.Div([
            html.Div('GPT-3.5-turbo Summary', className='card-header'),
            html.Div([
                html.H4('Radiation Oncology Patient Symptom Summary', className='card-title'),
                html.P(id='summary', className='card-text')
            ], className='card-body')
        ], className='card border-primary mb-3', style={'max-width': '60rem', 'margin': '3 auto'})
    ], className='summary-container mx-auto', style={'width': '60%'}),
    html.Br(),
    html.Div([
        dcc.Markdown('### Survey Results')
    ], style={'textAlign': 'center'}),
    dash_table.DataTable(
        id='results_table',
        columns=[        {'name': 'Question', 'id': 'question'},        {'name': 'Answer', 'id': 'answer'}    ],
        data=[],
        style_cell={
            'whiteSpace': 'normal',
            'height': 'auto',
            'textAlign': 'center',
        },
        style_data_conditional=[        {            'if': {'row_index': 'odd'},            'backgroundColor': 'rgb(248, 248, 248)'        }    ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_table={
            'margin': '0 auto',
            'width': '50%'
        }
    ),
    html.P([html.Br()])
    ], style=style)


@app.callback(
    Output('summary', 'children'),
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
    State('urinary_incontinence_interference', 'value'),
    State('radiation_skin_reaction_severity', 'value'),
    State('fatigue_severity', 'value'),
    State('fatigue_interference', 'value'),
    State('additional_symptoms', 'value'),
)
def update_results_table(n_clicks, *responses):
    if n_clicks == 0:
        return None, []

    questions = [
        'Number of Radiation treatments',
        'Increased passing of gas',
        'Diarrhea frequency',
        'Abdominal pain frequency',
        'Abdominal pain severity',
        'Abdominal pain with ADL',
        'Painful urination severity',
        'Urinary urgency frequency',
        'Urinary urgency with ADL',
        'Urinary frequency',
        'Urinary frequency with ADL',
        'Urine color change',
        'Urinary incontinence frequency',
        'Urinary incontinence with ADL',
        'Radiation skin reaction severity',
        'Fatigue severity',
        'Fatigue with ADL',
        'Additional symptoms',
    ]

    data = [{'question': question, 'answer': response} for question, response in zip(questions, responses)]

    summary = summarize_table(data)
    return summary, data

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
def summarize_table(data):
    messages = [{
        'role': 'system',
        'content': "You are an experienced radiation oncologist physician. You are provided this table of patient symptoms during their weekly follow-up visit during radiotherapy. Please summarize the following data into one sentence of natural language for your physician colleagues. Please put most important symptoms first. Example - This patient's most severe symptom is their very severe abdominal pain. Aside from this, the patient is also experiencing occasional diarrhea. :"
    }]
    
    for row in data:
        messages.append({
            'role': 'user',
            'content': f"{row['question']}: {row['answer']}"
        })
    
    messages.append({
        'role': 'assistant',
        'content': "Summary:"
    })

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        n=1,
        stop=None,
        temperature=0.2,
    )

    summary = response.choices[0].message.content.strip()
    return summary

# def send_email(to_email, pdf_file):
#     from_email = "you@example.com"  # Your email address. 
#     password = "your_password"  # Your email password. Can consider using SendGrid for better security.

#     # Create a multipart email message
#     msg = MIMEMultipart()
#     msg["From"] = from_email
#     msg["To"] = to_email
#     msg["Subject"] = "Patient Symptom Table PDF"

#     # Attach the PDF file
#     with open(pdf_file, "rb") as file:
#         attachment = MIMEBase("application", "octet-stream")
#         attachment.set_payload(file.read())
#         encoders.encode_base64(attachment)
#         attachment.add_header("Content-Disposition", f"attachment; filename={pdf_file}")
#         msg.attach(attachment)

#     # Send the email
#     server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
#     server.login(from_email, password)
#     server.sendmail(from_email, to_email, msg.as_string())
#     server.quit()


if __name__ == '__main__':
    app.run_server(debug=True)