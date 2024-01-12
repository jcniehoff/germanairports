import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv("AirportsGermany")

# Initialize the Dash app
app = dash.Dash(__name__)

# Assume df is your DataFrame after processing the data with columns 'Name', 'City', 'Latitude', 'Longitude'
# df = pd.read_csv('your_data.csv')  # You would load your data here

# Parse the coordinates from the last column and add them as separate columns
df['Latitude'] = df['coordinates_column'].apply(lambda x: float(x.split(',')[0]))
df['Longitude'] = df['coordinates_column'].apply(lambda x: float(x.split(',')[1]))

# Create the Plotly map
fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", hover_name="Name",
                        hover_data=["City", "Country"], zoom=5)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Define the layout of the Dash app
app.layout = html.Div([
    dcc.Graph(
        id='germany-airports-map',
        figure=fig
    ),
    html.Div(id='clicked-data')
])


# Define callback to update the click-data div
@app.callback(
    Output('clicked-data', 'children'),
    [Input('germany-airports-map', 'clickData')]
)
def display_click_data(clickData):
    if clickData is not None:
        return html.P(str(clickData))
    else:
        return 'Click on an airport'


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
