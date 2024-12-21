import json

# Constants
COLORS = {
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

# HTML Templates
MAIN_HTML_TEMPLATE = '''
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

PREVIEW_HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <style>
        body { 
            margin: 0; 
            padding: 0; 
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: #f5f5f5;
        }
        .preview-grid { 
            display: inline-block;
            padding: 8px;
            background: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border-radius: 4px;
        }
        .grid-row { 
            display: flex;
            line-height: 0;
        }
        .cell {
            width: 6px;
            height: 6px;
            border: 0.5px solid rgba(0,0,0,0.2);
            box-sizing: border-box;
            flex-shrink: 0;
        }
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
    </style>
    <script>
        window.onload = function() {
            const grid = document.querySelector('.preview-grid');
            const container = document.body;
            const gridWidth = grid.offsetWidth;
            const gridHeight = grid.offsetHeight;
            const containerWidth = container.clientWidth;
            const containerHeight = container.clientHeight;
            const padding = 16;
            const scaleX = (containerWidth - padding) / gridWidth;
            const scaleY = (containerHeight - padding) / gridHeight;
            const scale = Math.min(scaleX, scaleY, 2.5);
            grid.style.transform = `scale(${scale})`;
        };
    </script>
</head>
<body>
    <div class="preview-grid">
'''

def generate_grid_html(grid_data, colors=COLORS):
    """Generate HTML for a grid visualization."""
    html = ''
    for row in grid_data:
        html += '<div class="grid-row">'
        for cell in row:
            color = colors.get(cell, '#FFFFFF')
            html += f'<div class="cell" style="background-color: {color};"></div>'
        html += '</div>'
    return html

def create_grid_visualization(task_id, attempts_data=None):
    """Create main visualization HTML file for a task."""
    html = MAIN_HTML_TEMPLATE
    
    # Read task data
    with open(f"/ARC-AGI/data/evaluation/{task_id}.json", 'r') as f:
        data = json.load(f)
    
    html += f'<h2>Task: {task_id}</h2>'
    
    # Training examples
    for i, example in enumerate(data['train']):
        html += '<div class="row">'
        
        # Input grid
        html += f'<div class="grid"><div class="title">Train {i+1} Input</div>'
        html += generate_grid_html(example['input'])
        html += '</div>'
        
        # Output grid
        html += f'<div class="grid"><div class="title">Train {i+1} Output</div>'
        html += generate_grid_html(example['output'])
        html += '</div></div>'
    
    # Test case
    html += '<h3>Test Case</h3><div class="row">'
    html += '<div class="grid"><div class="title">Test Input</div>'
    html += generate_grid_html(data['test'][0]['input'])
    html += '</div>'
    
    html += '<div class="grid"><div class="title">Test Output</div>'
    html += generate_grid_html(data['test'][0]['output'])
    html += '</div></div>'
    
    # Attempts visualization
    if attempts_data and task_id in attempts_data:
        html += '<div class="row">'
        for attempt_num in [1, 2]:
            attempt = attempts_data[task_id][0][f"attempt_{attempt_num}"]
            html += f'<div class="grid"><div class="title">Attempt {attempt_num}</div>'
            html += generate_grid_html(attempt)
            html += '</div>'
        html += '</div>'
    
    html += '</div></body></html>'
    
    # Write to file
    output_file = f'task_{task_id}_viz.html'
    with open(output_file, 'w') as f:
        f.write(html)
    
    # Create preview
    preview_html = PREVIEW_HTML_TEMPLATE
    preview_html += generate_grid_html(data['test'][0]['input'])
    preview_html += '</div></body></html>'
    
    preview_file = f'task_{task_id}_preview.html'
    with open(preview_file, 'w') as f:
        f.write(preview_html)
    
    print(f"Created visualization at: {output_file}")

def create_index_page(task_ids):
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .container { 
                padding: 20px; 
                font-family: monospace;
                max-width: 1200px;
                margin: 0 auto;
            }
            .task-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
                gap: 15px;
                padding: 20px;
            }
            .task-card {
                position: relative;
                border: 1px solid #ddd;
                border-radius: 8px;
                overflow: hidden;
                transition: transform 0.2s;
                background: white;
                text-decoration: none;
                color: #333;
                cursor: pointer;
            }
            .task-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            .preview-container {
                width: 100%;
                aspect-ratio: 1;
                display: flex;
                align-items: center;
                justify-content: center;
                background: #f5f5f5;
                pointer-events: none;
            }
            .preview-frame {
                border: none;
                width: 100%;
                height: 100%;
                transform-origin: center;
                transform: scale(2);
                pointer-events: none;
            }
            .task-title {
                padding: 10px;
                text-align: center;
                font-weight: bold;
                border-top: 1px solid #eee;
                background: white;
                pointer-events: none;
            }
            .card-link {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 1;
            }
        </style>
    </head>
    <body>
    <div class="container">
        <h1>Task Visualizations</h1>
        <div class="task-grid">
    '''
    
    # Add cards for each task with proper file paths
    for task_id in sorted(task_ids):
        viz_path = f"task_{task_id}_viz.html"
        preview_path = f"task_{task_id}_preview.html"
        
        html += f'''
            <div class="task-card">
                <a href="{viz_path}" class="card-link"></a>
                <div class="preview-container">
                    <iframe class="preview-frame" src="{preview_path}" scrolling="no"></iframe>
                </div>
                <div class="task-title">Task {task_id}</div>
            </div>
        '''
    
    html += '</div></div></body></html>'
    
    # Write to file
    with open('task_index.html', 'w', encoding='utf-8') as f:
        f.write(html)
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