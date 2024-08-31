from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    pattern = ""
    pattern_option = ""
    highlighted_text = ""
    error_message = None
    
    # Teks default yang akan diuji jika tidak ada input dari pengguna
    default_text = """
    Berikut adalah beberapa contoh teks yang akan diuji: 
    Email: example@unair.ac.id, user@example.com, john.doe@example.org 
    Nomor KTP: 1234561999123456, 6543211989123456 
    Password: StrongPass123, weakpass 
    Nama File: document.pdf, file.txt, photo.jpg 
    NIM: 1641234567, 1621234567 
    Kata dengan kapital: Jakarta, Surabaya, Bandung, jakarta, surabaya, bandung
    """
    
    if request.method == "POST":
        pattern_option = request.form.get("pattern_option", "")
        pattern = request.form.get("pattern", "")
        text = request.form.get("text", default_text)
        
        # Menentukan pola regex berdasarkan pilihan
        if pattern_option == "Seluruh alamat email valid":
            pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        elif pattern_option == "Seluruh alamat email valid dengan domain akhir .unair.ac.id":
            pattern = r"[a-zA-Z0-9._%+-]+@unair\.ac\.id"
        elif pattern_option == "Seluruh nomor KTP dengan tahun lahir 1999":
            pattern = r"^\d{10}99\d{4}$"
        elif pattern_option == "Seluruh kata dengan awalan huruf kapital":
            pattern = r"\b[A-Z][a-z]*\b"
        elif pattern_option == "Validasi string yang hanya memuat alphanumeric dan underscore":
            pattern = r"^\w+$"
        elif pattern_option == "Mencari file dengan ekstensi dokumen (pdf, docx, doc, txt)":
            pattern = r"\b\w+\.(pdf|docx|doc|txt)\b"
        elif pattern_option == "Strong password filter":
            pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        elif pattern_option == "Mencari NIM mahasiswa sesuai jurusan":
            pattern = r"\b(166|165|164|162|163)\d{6}\b"

        try:
            # Menggunakan regex untuk menandai kecocokan dan membuat teks dengan highlight
            highlighted_text = re.sub(pattern, r'<span class="highlight">\g<0></span>', text)
        except re.error as e:
            error_message = f"Error in regex: {e}"
            highlighted_text = text
    
    return render_template("index.html", pattern=pattern, pattern_option=pattern_option, highlighted_text=highlighted_text, error_message=error_message, text=text)

if __name__ == "__main__":
    app.run(debug=True)
