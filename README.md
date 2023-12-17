LocalKVM is a Django project designed to manage virtual machines locally. It provides a web-based interface for users to interact with their virtual machines, perform CRUD (Create, Read, Update, Delete) operations, and visualize the status of the virtual machines.

## Installation:

Clone the Repository:
```bash
git clone https://github.com/mrankitvish/Localkvm.git
cd LocalKVM
```
Create a Virtual Environment:

```bashbash
python -m venv venv
```

Activate the Virtual Environment:

On Windows:
```bash
.\venv\Scripts\activate
```
On Linux/Mac:
```bash
source venv/bin/activate
```
Install Dependencies:

```bash
pip install -r requirements.txt
```
Configure `api/config.py`:

```bash
LIBVIRT_CREDENTIALS = {
    'username': 'cloud',
    'host': '192.168.29.4'
}
```
Replace `username` and `host` with your KVM machine's credentials.

Apply Database Migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

```bash
python manage.py runserver
```
Access the web application at `http://localhost:8000/api/vmlist` in your browser.