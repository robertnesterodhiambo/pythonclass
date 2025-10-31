#!/usr/bin/env python3
from flask import Flask, render_template_string, request, Response
import subprocess
import threading
import queue
import time

app = Flask(__name__)
log_queue = queue.Queue()
process_thread = None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Job Scraper UI</title>
    <style>
        body { font-family: monospace; background: #111; color: #eee; padding: 20px; }
        .terminal { background: #000; border: 1px solid #555; padding: 10px; height: 500px; overflow-y: scroll; }
        button { background: #28a745; color: white; padding: 10px 20px; border: none; cursor: pointer; margin-top: 10px; }
        button:disabled { background: #555; }
    </style>
</head>
<body>
    <h2>Job Scraper UI</h2>
    <form id="scrapeForm">
        <label>Select "Dostępne od" days:</label><br>
        {% for i in range(1, 32) %}
            <label><input type="checkbox" name="days" value="{{ i }}"> {{ i }}</label>
        {% endfor %}
        <br><br>
        <button type="submit" id="startBtn">Start Scraper</button>
    </form>

    <h3>Logs:</h3>
    <div id="terminal" class="terminal"></div>

    <script>
    const terminal = document.getElementById('terminal');
    const form = document.getElementById('scrapeForm');
    const startBtn = document.getElementById('startBtn');

    form.addEventListener('submit', e => {
        e.preventDefault();
        const selectedDays = Array.from(form.elements['days'])
                                 .filter(c => c.checked)
                                 .map(c => c.value)
                                 .join(',');
        if (!selectedDays) {
            alert("Please select at least one day.");
            return;
        }
        startBtn.disabled = true;
        fetch('/start?days=' + selectedDays);
        const eventSource = new EventSource('/stream');
        eventSource.onmessage = function(event) {
            terminal.innerHTML += event.data + "<br>";
            terminal.scrollTop = terminal.scrollHeight;
        };
        eventSource.onerror = function() {
            eventSource.close();
            startBtn.disabled = false;
        };
    });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/start')
def start_scraper():
    global process_thread
    days = request.args.get('days', '')
    if not days:
        return "No days selected", 400

    if process_thread and process_thread.is_alive():
        return "Scraper already running.", 400

    def run_scraper():
        process = subprocess.Popen(
            ['python3', 'scrape.py'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        # Provide user input for days automatically
        process.stdin.write(days + "\n")
        process.stdin.flush()

        for line in process.stdout:
            log_queue.put(line.strip())

        process.stdout.close()
        process.wait()
        log_queue.put("✅ Scraper finished.")

    process_thread = threading.Thread(target=run_scraper, daemon=True)
    process_thread.start()
    return "Started"

@app.route('/stream')
def stream_logs():
    def generate():
        while True:
            try:
                line = log_queue.get(timeout=1)
                yield f"data: {line}\n\n"
            except queue.Empty:
                if not (process_thread and process_thread.is_alive()):
                    break
                continue
    return Response(generate(), mimetype='text/event-stream')

if __name__ == "__main__":
    print("🌐 Open http://127.0.0.1:5000 in your browser")
    app.run(debug=True, use_reloader=False)
