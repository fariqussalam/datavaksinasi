from functools import wraps
from datetime import datetime
from hashlib import md5
from app import db, login
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    unit_kerja = db.Column(db.String(140))
    role = db.Column(db.String(140))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Batch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(140))
    waktu = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Batch {}>'.format(self.nama)


class PesertaVaksinasi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(140))
    pn = db.Column(db.String(140))
    unit_kerja = db.Column(db.String(140))
    batch = db.Column(db.String(140))
    nik = db.Column(db.String(140))
    nama_lengkap = db.Column(db.String(140))
    jenis_kelamin = db.Column(db.String(140))
    tanggal_lahir = db.Column(db.String(140))
    instansi_pekerjaan = db.Column(db.String(140))
    pekerjaan = db.Column(db.String(140))
    jenis_pekerjaan = db.Column(db.String(140))
    no_hp = db.Column(db.String(140))
    alamat_ktp = db.Column(db.String(140))
    kode_kabupaten = db.Column(db.String(140))
    nama_kota = db.Column(db.String(140))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    waktu_kehadiran = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    hadir = db.Column(db.Boolean, default=False)
    umur = db.Column(db.Integer)
    penyelenggara = db.Column(db.String(140))
    waktu_vaksin = db.Column(db.String(140))

    def __repr__(self):
        return '<PesertaVaksinasi {}>'.format(self.nik)


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                # Redirect the user to an unauthorized notice!
                return "You are not authorized to access this page"
            return f(*args, **kwargs)
        return wrapped
    return wrapper