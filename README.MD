# Panduan Instalasi Program

## Requirements
Pastikan sistem Anda memiliki hal berikut sebelum menginstal dan menjalankan program ini:

- Python (versi 3.x)
- Django (versi yang kompatibel dengan Python 3.x)
- Graphviz

## Langkah-langkah Instalasi

1. **Python**: Jika Anda belum memiliki Python diinstal, Anda bisa mendapatkannya dari [situs web resmi Python](https://www.python.org/downloads/). Ikuti petunjuk instalasi yang disediakan di sana.

2. **Django**: Setelah menginstal Python, Anda bisa menginstal Django menggunakan pip, manajer paket Python. Jalankan perintah berikut di terminal atau command prompt:

    ```
    pip install django
    ```

3. **Graphviz**: Untuk menginstal Graphviz, Anda bisa mengunjungi [situs web resminya](https://graphviz.org/) dan mengikuti petunjuk instalasi yang disediakan.

## Menjalankan Program

Setelah Anda menginstal semua requirements, Anda bisa menjalankan program ini dengan langkah-langkah berikut:

1. **Clone Repositori**: Clone repositori program ini ke dalam sistem Anda.

    ```
    git clone https://github.com/namauser/namarepositori.git
    ```

2. **Navigasi ke Direktori**: Pindah ke direktori tempat Anda telah mengkloning repositori.

    ```
    cd namarepositori
    ```

3. **Migrasi Database**: Lakukan migrasi database dengan menjalankan perintah berikut:

    ```
    python manage.py migrate
    ```

4. **Jalankan Server**: Jalankan server Django dengan perintah:

    ```
    python manage.py runserver
    ```

5. **Akses Program**: Buka browser web Anda dan akses `http://localhost:
