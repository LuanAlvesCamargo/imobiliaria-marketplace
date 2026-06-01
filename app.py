from flask import Flask, render_template
# Make sure to import your get_connection function here!
# (Adjust this import depending on which file 'get_connection' is defined in)
# Example: from database import get_connection 

app = Flask(__name__)

@app.route("/")
def home():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT *
        FROM imoveis
        WHERE status='Disponivel'
    """)
    
    imoveis = cursor.fetchall()
    
    return render_template(
        "index.html",
        imoveis=imoveis
    )

# This block ensures the server runs when you execute this specific file
if __name__ == "__main__":
    app.run(debug=True)