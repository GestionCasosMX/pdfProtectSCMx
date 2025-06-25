from flask import Flask, request, send_file
import pypdf
import io

app = Flask(__name__)

@app.route('/protect_pdf', methods=['POST'])
def protect_pdf():
    pdf_file = request.files['file']
    password = request.form['password']

    pdf_reader = pypdf.PdfReader(pdf_file)
    pdf_writer = pypdf.PdfWriter()

    for page in pdf_reader.pages:
        pdf_writer.add_page(page)

    pdf_writer.encrypt(user_password=password, owner_password=None, use_128bit=True)

    encrypted_pdf = io.BytesIO()
    pdf_writer.write(encrypted_pdf)
    encrypted_pdf.seek(0)

    return send_file(encrypted_pdf, download_name='protected.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
