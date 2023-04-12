import pandas as pd
import plotly.express as px
import plotly.io as pio
from dash import Dash, dcc, html, Input, Output

df = pd.read_csv("weight.csv")
df = df.drop(columns=["Comments"]).dropna()
# Make it a datetime for the rolling window
df["date"] = pd.to_datetime(df.Date)
df.set_index("date", inplace=True)
# Sort dates so the rolling window takes what happens before the day instead of after
df.sort_index(ascending=True,inplace=True)

# Computing the percentages
df["fat"] = df["Fat mass (kg)"]/df["Weight (kg)"]
df["bone"] = df["Bone mass (kg)"]/df["Weight (kg)"]
df["muscle"] = df["Muscle mass (kg)"]/df["Weight (kg)"]
df["hydration"] = df["Hydration (kg)"]/df["Weight (kg)"]

# Computing the average over the last 7 days
period = "7.5D" # .5 Because else it will not take in account things like day 1 @ 7h, and day 2 at 7h10 as it's more than one 1 day
df["weightmean"] = df["Weight (kg)"].rolling(period).mean()
df["fatmean"] = df["fat"].rolling(period).mean()
df["bonemean"] = df["bone"].rolling(period).mean()
df["musclemean"] = df["muscle"].rolling(period).mean()
df["hydrationmean"] = df["hydration"].rolling(period).mean()

# Computing the delta in values between now and 1/7 days
period = "1.5D"
df["weight_delta_1D"] = df["weightmean"]-df["weightmean"].rolling(period).agg(lambda rows: rows[0])
df["fat_delta_1D"] = df["fatmean"]-df["fatmean"].rolling(period).agg(lambda rows: rows[0])
df["bone_delta_1D"] = df["bonemean"]-df["bonemean"].rolling(period).agg(lambda rows: rows[0])
df["muscle_delta_1D"] = df["musclemean"]-df["musclemean"].rolling(period).agg(lambda rows: rows[0])
df["hydration_delta_1D"] = df["hydrationmean"]-df["hydrationmean"].rolling(period).agg(lambda rows: rows[0])
period = "7.5D"
df["weight_delta_7D"] = df["weightmean"]-df["weightmean"].rolling(period).agg(lambda rows: rows[0])
df["fat_delta_7D"] = df["fatmean"]-df["fatmean"].rolling(period).agg(lambda rows: rows[0])
df["bone_delta_7D"] = df["bonemean"]-df["bonemean"].rolling(period).agg(lambda rows: rows[0])
df["muscle_delta_7D"] = df["musclemean"]-df["musclemean"].rolling(period).agg(lambda rows: rows[0])
df["hydration_delta_7D"] = df["hydrationmean"]-df["hydrationmean"].rolling(period).agg(lambda rows: rows[0])

df2 = df.tail(60) # Only the last 60 measures

app = Dash(__name__)

fig = px.line(df2, x="Date", y=["weightmean"], labels={"x": "Date"})
fig.update_layout(hovermode="x unified", xaxis_title="Date", yaxis_title="Weight 7d moving average")
fig["data"][0]["name"] = "Weight 7d moving average"

fig2 = px.line(df2, x="Date", y=["fatmean"], labels={"x": "Date"})
fig2.update_layout(hovermode="x unified", xaxis_title="Date", yaxis_title="Fat 7d moving average")
fig2["data"][0]["name"] = "Fat 7d moving average"

fig3 = px.line(df2, x="Date", y=["fat_delta_1D"], labels={"x": "Date"})
fig3.update_layout(hovermode="x unified", xaxis_title="Date", yaxis_title="Fat % avg delta over 1D")
fig3["data"][0]["name"] = "Fat % avg delta with previous day"

fig4 = px.line(df2, x="Date", y=["fat_delta_7D"], labels={"x": "Date"})
fig4.update_layout(hovermode="x unified", xaxis_title="Date", yaxis_title="Fat % avg delta over 7D")
fig4["data"][0]["name"] = "Fat % avg delta with previous week"

app.layout = html.Div(children=[
    html.H1(children='Shred'),

    html.H2(children='Weight 7d moving average'),
    dcc.Graph(
        id='weight-7d-moving-avg',
        figure=fig
    ),
    html.H2(children='Fat % 7d moving average'),
    dcc.Graph(
        id='fat-7d-moving-avg',
        figure=fig2
    ),
    html.H2(children='Fat % loss compare to the previous day'),
    dcc.Graph(
        id='fat-pct-delta-1d',
        figure=fig3
    ),
    html.H2(children='Fat % loss compare to the previous week'),
    dcc.Graph(
        id='fat-pct-delta-7d',
        figure=fig4
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)

