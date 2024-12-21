import json

def create_grid_visualization(task_id, attempts_data=None):
    # HTML template with embedded CSS
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .container { padding: 20px; font-family: monospace; }
            .row { display: flex; margin-bottom: 15px; }
            .grid { margin: 0 8px; }
            .title { margin-bottom: 3px; font-size: 10px; }
            .grid-row { display: flex; }
            .cell {
                width: 15px;
                height: 15px;
                border: 1px solid #999;
                box-sizing: border-box;
            }
        </style>
    </head>
    <body>
    <div class="container">
    '''
    
    # Color mapping
    colors = {
        0: '#000',
        1: '#0074D9',
        2: '#FF4136',
        3: '#2ECC40',
        4: '#FFDC00',
        5: '#AAAAAA',
        6: '#F012BE',
        7: '#FF851B',
        8: '#7FDBFF',
        9: '#870C25'
    }
    
    # Read task data
    with open(f"{task_id}.json", 'r') as f:
        data = json.load(f)
    
    html += f'<h2>Task: {task_id}</h2>'
    
    # Add each training example
    for i, example in enumerate(data['train']):
        html += '<div class="row">'
        
        # Input grid
        html += f'''
            <div class="grid">
                <div class="title">Train {i+1} Input</div>
        '''
        
        for row in example['input']:
            html += '<div class="grid-row">'
            for cell in row:
                color = colors.get(cell, '#FFFFFF')
                html += f'<div class="cell" style="background-color: {color};"></div>'
            html += '</div>'
        html += '</div>'
         
        # Output grid
        html += f'''
            <div class="grid">
                <div class="title">Train {i+1} Output</div>
        '''
        
        for row in example['output']:
            html += '<div class="grid-row">'
            for cell in row:
                color = colors.get(cell, '#FFFFFF')
                html += f'<div class="cell" style="background-color: {color};"></div>'
            html += '</div>'
        html += '</div>'
        
        html += '</div>'  # end row
    
    # Add test input and output
    html += '<h3>Test Case</h3>'
    html += '<div class="row">'
    
    # Test input grid
    html += '''
        <div class="grid">
            <div class="title">Test Input</div>
    '''
    
    for row in data['test'][0]['input']:
        html += '<div class="grid-row">'
        for cell in row:
            color = colors.get(cell, '#FFFFFF')
            html += f'<div class="cell" style="background-color: {color};"></div>'
        html += '</div>'
    html += '</div>'
    
    # Test output grid
    html += '''
        <div class="grid">
            <div class="title">Test Output</div>
    '''
    
    for row in data['test'][0]['output']:
        html += '<div class="grid-row">'
        for cell in row:
            color = colors.get(cell, '#FFFFFF')
            html += f'<div class="cell" style="background-color: {color};"></div>'
        html += '</div>'
    html += '</div>'
    
    html += '</div>'  # end test row
    
    # Add attempts if provided
    if attempts_data and task_id in attempts_data:
        html += '<div class="row">'
        for attempt_num in [1, 2]:
            attempt = attempts_data[task_id][0][f"attempt_{attempt_num}"]
            html += f'''
                <div class="grid">
                    <div class="title">Attempt {attempt_num}</div>
            '''
            
            for row in attempt:
                html += '<div class="grid-row">'
                for cell in row:
                    color = colors.get(cell, '#FFFFFF')
                    html += f'<div class="cell" style="background-color: {color};"></div>'
                html += '</div>'
            html += '</div>'
        html += '</div>'
    
    html += '</div></body></html>'
    
    # Write to file
    output_file = f'task_{task_id}_viz.html'
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"Created visualization at: {output_file}")

def create_index_page(task_ids):
    # HTML template for index page
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .container { 
                padding: 20px; 
                font-family: monospace;
                max-width: 800px;
                margin: 0 auto;
            }
            .task-link {
                display: inline-block;
                padding: 10px;
                margin: 5px;
                background-color: #f0f0f0;
                border-radius: 4px;
                text-decoration: none;
                color: #333;
            }
            .task-link:hover {
                background-color: #e0e0e0;
            }
        </style>
    </head>
    <body>
    <div class="container">
        <h1>Task Visualizations</h1>
    '''
    
    # Add links to each task visualization
    for task_id in sorted(task_ids):
        html += f'<a class="task-link" href="task_{task_id}_viz.html">Task {task_id}</a>\n'
    
    html += '</div></body></html>'
    
    # Write to file
    with open('task_index.html', 'w') as f:
        f.write(html)
    
    print("Created index page at: task_index.html")

# Modify the main execution
if __name__ == "__main__":
    with open('results.json', 'r') as f:
        results = json.load(f)
    
    with open('attempts.json', 'r') as f:
        attempts_data = json.load(f)
    
    # Visualize failed tasks
    failed_tasks = [task_id for task_id, score in results['task_results'].items() if score < 1.0]
    
    for task_id in failed_tasks:
        create_grid_visualization(task_id, attempts_data)
    
    # Create index page
    create_index_page(failed_tasks)
