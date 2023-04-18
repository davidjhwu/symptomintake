import dash_table

severity_colors = {
    "None": '#008000',
    "Not at all": '#008000',
    "Never": '#008000',
    "Mild": '#90ee90',
    "A little bit": '#90ee90',
    "Rarely": '#90ee90',
    "Moderate": '#ffff00',
    "Somewhat": '#ffff00',
    "Occasionally": '#ffff00',
    "Severe": '#ffa500',
    "Quite a bit": '#ffa500',
    "Frequently": '#ffa500',
    "Very severe": '#ff0000',
    "Very much": '#ff0000',
    "Almost constantly": '#ff0000',
    "Yes": '#008000',
    "No": '#ff0000',
}

def create_data_table():
    style_data_conditional = []

    for response, color in severity_colors.items():
        text_color = 'white' if color != '#ffff00' else 'black'
        style_data_conditional.append({
            'if': {
                'filter_query': '{{answer}} = "{}"'.format(response),
                'column_id': 'answer'
            },
            'backgroundColor': color,
            'color': text_color
        })

    return dash_table.DataTable(
        id='results_table',
        columns=[
            {'name': 'Question', 'id': 'question'},
            {'name': 'Answer', 'id': 'answer'},
        ],
        data=[],
        style_cell={
            'whiteSpace': 'normal',
            'height': 'auto',
            'textAlign': 'center',
            'border': 'none',
        },
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold',
            'border': 'none',
        },
        style_table={
            'margin': '0 auto',
            'width': '50%'
        },
        style_data_conditional=style_data_conditional
    )
