# Problem 6

# Step 1: Data Preparation
df_subset = gss_clean[['income', 'sex', 'job_prestige']].copy()

# Create job_prestige categories
labels = ["Very Low", "Low", "Below Average", "Above Average", "High", "Very High"]
df_subset['job_prestige_cat'] = pd.cut(df_subset['job_prestige'], 6, labels=labels)

# Drop missing values
df_subset.dropna(inplace=True)

# Step 2: Facet Grid Creation

# Create the facet grid box plots
fig_facet = px.box(df_subset,
             y="income",
             color="sex",
             facet_row="job_prestige_cat",
             category_orders={"job_prestige_cat": labels},
             color_discrete_map={'male': 'blue', 'female': 'red'},
             labels={"income": "Income Distribution"})


# Update layout
fig_facet.update_layout(
    showlegend=False,
    height=1500  
)

# Display the plot
fig_facet.show()






#Challenge 1

# Create a fresh instance of the JupyterDash app
app = Dash(__name__)


# Additional Styles
card_style = {
    'padding': '20px',
    'border': 'thin lightgrey solid',
    'borderRadius': '5px',
    'backgroundColor': '#f9f9f9',
    'margin': '10px'
}

grid_style = {
    'display': 'grid',
    'gridTemplateColumns': '1fr 1fr',
    'gap': '20px'
}

# App Layout
app.layout = html.Div([
    
    # Top Header
    html.Div(
        html.H1('Gender Pay Gap Analysis and the General Social Survey Overview', 
                style={'padding': '10px', 'backgroundColor': '#333', 'color': 'white'}),
        style={'width': '100%', 'display': 'block'}
    ),

    # Research Markdown
    html.Div(dcc.Markdown(research_text), style=card_style),

    # Grid Layout for Table and Barplot
    html.Div([
        html.Div([
            html.H3('Average Values Grouped by Sex'),
            dcc.Graph(figure=fig_table)
        ], style=card_style),
        
        html.Div([
            html.H3('Agreement Levels on "Male as Breadwinner" Statement Grouped by Sex'),
            dcc.Graph(figure=fig_barplot)
        ], style=card_style)
    ], style=grid_style),

    # Scatter Plot
    html.Div([
        html.H3('Income vs. Job Prestige Grouped by Sex'),
        dcc.Graph(figure=fig_scatter)
    ], style=card_style),

    # Grid Layout for Two Boxplots
    html.Div([
        html.Div([
            html.H3('Income Distribution by Sex'),
            dcc.Graph(figure=fig_income)
        ], style=card_style),

        html.Div([
            html.H3('Job Prestige Distribution by Sex'),
            dcc.Graph(figure=fig_prestige)
        ], style=card_style)
    ], style=grid_style),

    # Faceted Boxplots
    html.Div([
        html.H3('Income Distribution by Job Prestige Categories'),
        dcc.Graph(figure=fig_facet)
    ], style=card_style),

    # Footer
    html.Div('Generated using Dash & Plotly', style={'textAlign': 'center', 'padding': '10px', 'backgroundColor': '#333', 'color': 'white'})
])

# Run the app
app.run_server(debug=True,port=8054)







#Challenge 2

# Sample data
data = {
    'sex': ['Male', 'Female', 'Male', 'Female'],
    'region': ['North', 'South', 'East', 'West'],
    'education': ['High School', 'College', 'Graduate', 'High School'],
    'satjob': [5, 7, 8, 6],
    'relationship': [8, 6, 7, 5],
    'male_breadwinner': [3, 4, 2, 3],
    'men_bettersuited': [4, 5, 3, 4],
    'child_suffer': [4, 5, 4, 3],
    'men_overwork': [6, 5, 7, 4]
}

df = pd.DataFrame(data)

# New Dash app for Challenge 2
challenge_app = dash.Dash(__name__)


challenge_app.layout = html.Div([
    dcc.Dropdown(
        id='feature-dropdown',
        options=[
            {'label': 'Job Satisfaction', 'value': 'satjob'},
            {'label': 'Relationship', 'value': 'relationship'},
            {'label': 'Male as Breadwinner', 'value': 'male_breadwinner'},
            {'label': 'Men Better Suited', 'value': 'men_bettersuited'},
            {'label': 'Child Suffer', 'value': 'child_suffer'},
            {'label': 'Men Overwork', 'value': 'men_overwork'}
        ],
        value='male_breadwinner',
        clearable=False
    ),
    dcc.Dropdown(
        id='grouping-dropdown',
        options=[
            {'label': 'Sex', 'value': 'sex'},
            {'label': 'Region', 'value': 'region'},
            {'label': 'Education', 'value': 'education'}
        ],
        value='sex',
        clearable=False
    ),
    dcc.Graph(id='barplot-output')
])

@challenge_app.callback(
    Output('barplot-output', 'figure'),
    [Input('feature-dropdown', 'value'),
     Input('grouping-dropdown', 'value')]
)
def update_barplot(feature, grouping):
    fig = px.bar(df, x=grouping, y=feature, color=grouping, title=f"{feature} by {grouping}")
    return fig

if __name__ == '__main__':
    challenge_app.run_server(debug=True, port=8055)
