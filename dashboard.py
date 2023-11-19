import plotly
import plotly.graph_objs as go
import plotly.offline as opy
import sqlite3
import plotly.express as px
import json

def fetch_data(userid):
    conn = sqlite3.connect('Cal.db')
    cursor = conn.cursor()
    query = "SELECT e_name, duration FROM exercise WHERE uid = ?"
    cursor.execute(query, (userid,))
    data = cursor.fetchall()
    time_query = "SELECT date, calories FROM exercise WHERE uid = ?"
    cursor.execute(time_query, (userid,))
    time_data = cursor.fetchall()
    calories_query = "SELECT e_name, calories FROM exercise WHERE uid = ?"
    cursor.execute(calories_query, (userid,))
    calories_data = cursor.fetchall()
    heart_query = "SELECT bpm, calories FROM exercise WHERE uid = ?"
    cursor.execute(heart_query, (userid,))
    heart_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data, time_data, calories_data, heart_data

def create_bar_chart(data):
    exercise, duration = zip(*data)

    trace = go.Bar(x=exercise, y=duration)
    layout = go.Layout(title='Exercise vs duration', xaxis=dict(title='Exercise'), yaxis=dict(title='Duration'))
    fig = go.Figure(data=[trace], layout=layout)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def create_line_chart(time_data):
    date, calories = zip(*time_data)

    trace = go.Scatter(x=date, y=calories, mode='lines+markers', marker=dict(size=10), line=dict(width=2))
    layout = go.Layout(title='Total Calories Over Time', xaxis=dict(title='Date'), yaxis=dict(title='Total Calories'))
    fig = go.Figure(data=[trace], layout=layout)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_pie_chart(data, title):
    exercise_names, calories = zip(*data)

    trace = go.Pie(labels=exercise_names, values=calories)
    layout = go.Layout(title=title)
    fig = go.Figure(data=[trace], layout=layout)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_heart_rate_scatter_plot(data):
    bpm, calories = zip(*data)

    trace = go.Scatter(x=bpm, y=calories, mode='markers', marker=dict(size=12))
    layout = go.Layout(title='Heart Rate vs. Calories Burned', xaxis=dict(title='Heart Rate (BPM)'), yaxis=dict(title='Calories Burned'))
    fig = go.Figure(data=[trace], layout=layout)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
