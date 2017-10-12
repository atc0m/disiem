import json
import pickle
from plotly.offline import plot
import plotly.graph_objs as go

def sort_log_file(key, file_path, wrapper_manager):
    with open(file_path) as f:
        logs = [wrapper_manager.get_wrapper(key, json.loads(line)) for line in f]

    sorted_logs = sorted(
        logs,
        key=lambda x: x.get_time()
    )
    print len(sorted_logs)
    with open('mcafee.txt', 'wb') as fle:
        item = '\n'.join([json.dumps(log) for log in sorted_logs])
        fle.write(item)

def time_coverage_graph():
    data = bytes()
    with open('reports/time_map_server') as f:
        data = f.read()
        time_map = pickle.loads(data)
    graphs = []
    for software, times in time_map.items():
        graphs.append(go.Scatter(x=times.values(), name=software, y=[software for _ in times.values()], mode='markers+lines'))

    layout = go.Layout(title='Time Coverage')
    fig = go.Figure(data=graphs, layout=layout)
    url = plot(
        fig,
        filename='coverage'
    )
