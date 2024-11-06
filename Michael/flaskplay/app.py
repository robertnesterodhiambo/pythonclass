from flask import Flask, render_template

app = Flask(__name__)

# Route for Level 1 - Render 3 blue boxes
@app.route('/play')
def play():
    return render_template('play.html', boxes=3, color="blue")

# Route for Level 2 - Render x blue boxes
@app.route('/play/<int:x>')
def play_with_x(x):
    return render_template('play.html', boxes=x, color="blue")

# Route for Level 3 - Render x boxes in specified color
@app.route('/play/<int:x>/<color>')
def play_with_x_and_color(x, color):
    return render_template('play.html', boxes=x, color=color)

if __name__ == '__main__':
    app.run(debug=True)
