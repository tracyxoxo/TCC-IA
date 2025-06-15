import os
import zipfile
import shutil as sh 
from typing import List
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def extract_filtered_files(
    files_path: str,
    extract_path: str,
    pattern: str
) -> List[str]:
    
    final_path = extract_path + "_final"
    os.makedirs(extract_path, exist_ok=True)

    if os.path.exists(extract_path) and os.path.isdir(extract_path):
        sh.rmtree(extract_path)

    
    if os.path.exists(final_path) and os.path.isdir(final_path):
        sh.rmtree(final_path)

    for zip_file in os.listdir(files_path):
        if zip_file.endswith(".zip"):
            file = zip_file.removesuffix(".zip")
            extract_to = os.path.join(extract_path, file)
            os.makedirs(extract_to, exist_ok=True)
            with zipfile.ZipFile(os.path.join(files_path, zip_file), 'r') as zip_ref:
                zip_ref.extractall(extract_to)

    for dir in os.listdir(extract_path):
        full_name = os.path.join(extract_path, dir)
        if os.path.isdir(full_name) and os.listdir(full_name).count(dir) == 0:
            os.makedirs(final_path, exist_ok=True)
            sh.move(full_name, os.path.join(final_path, dir))

    for dir in os.listdir(extract_path):
        full_name = os.path.join(extract_path, dir)
        if os.path.isdir(full_name) and os.listdir(full_name).count(dir) > 0:
            os.makedirs(final_path, exist_ok=True)
            sh.move(os.path.join(full_name, dir), final_path)

    filterFiles_paths = []
    for root, dirs, files in os.walk(final_path):
        for file in files:
            if pattern in file:
                filterFiles_path = os.path.join(root, file)
                filterFiles_paths.append(filterFiles_path)

    return filterFiles_paths

def standard_hour(hour):
    hour = str(hour).replace("UTC", "").strip()

    if ':' in hour:
        hour = hour.replace(":", "")
    
    return hour

def create_incorrect_data_matrix(df, variable, lower, upper, title, row, col, fig):
    series = df[variable]
    outlier_col = f'is_outlier_{variable}'
    df[outlier_col] = (series < lower) | (series > upper)

    counts = df[outlier_col].value_counts()
    custom_labels = {
        False: f'False (Normal) [{counts.get(False, 0)}]',
        True: f'True (Anomalia) [{counts.get(True, 0)}]'
    }

    colors = {False: 'dodgerblue', True: 'red'}

    for outlier_value in [False, True]:
        subset = df[df[outlier_col] == outlier_value]

        fig.add_trace(
            go.Scattergl( 
                x=subset['datetime'],
                y=subset[variable],
                mode='markers',
                marker=dict(color=colors[outlier_value], size=2, opacity=0.5),
                name=custom_labels[outlier_value],
                legendgroup=custom_labels[outlier_value],
                showlegend=True
            ),
            row=row,
            col=col
        )
    fig.update_xaxes(title_text="Data e Hora", row=row, col=col)
    fig.update_yaxes(title_text=variable, row=row, col=col)

def plot_two_variables_vs_time(df, var1, var2, var1_label=None, var2_label=None, title=None):
    outlier_col_var1 = f'is_outlier_{var1}'
    outlier_col_var2 = f'is_outlier_{var2}'

    df_filtered = df[~(df[outlier_col_var1] | df[outlier_col_var2])] 

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scattergl(
            x=df_filtered['datetime'],
            y=df_filtered[var1],
            name=var1_label if var1_label else var1,
            mode='markers', 
            marker=dict(color='firebrick', size=5, opacity=0.5)
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scattergl(
            x=df_filtered['datetime'],
            y=df_filtered[var2],
            name=var2_label if var2_label else var2,
            mode='markers',
            marker=dict(color='dodgerblue', size=5, opacity=0.2)
        ),
        secondary_y=True,
    )

    fig.update_layout(
        height=600,
        width=1100,
        title=title if title else f'{var1} e {var2} ao longo do tempo',
        legend_title="Variáveis",
        template="plotly_white"
    )

    fig.update_xaxes(title_text="Data e Hora", showline=True, linewidth=1, linecolor='rgba(0, 0, 0, 0.3)', ticks="outside")
    
    fig.update_yaxes(
        title_text=var1_label if var1_label else var1,
        secondary_y=False,
        showline=True,
        linewidth=1,
        linecolor='rgba(255, 0, 0, 0.3)', 
        tickfont=dict(color='rgba(255, 0, 0, 0.5)'), 
    )

    fig.update_yaxes(
        title_text=var2_label if var2_label else var2,
        secondary_y=True,
        showline=True,
        linewidth=1,
        linecolor='rgba(0, 0, 255, 0.3)', 
        tickfont=dict(color='rgba(0, 0, 255, 0.5)'), 
    )
    fig.show()
