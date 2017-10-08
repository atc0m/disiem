import json

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
