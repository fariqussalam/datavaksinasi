from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User, PesertaVaksinasi, requires_roles


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Vaksinasi')


@app.route('/api-cek-jadwal', methods=['POST'])
def cek_jadwal():
    nik = request.form['nik']
    peserta = PesertaVaksinasi.query.filter_by(nik=nik).first()
    if peserta is None:
        return jsonify({'success': False, 'message': 'NIK Tidak Terdaftar'})
    return jsonify({'success': True, 'peserta': {
        "nik": peserta.nik,
        "nama_lengkap": peserta.nama_lengkap,
        "alamat_ktp": peserta.alamat_ktp,
        "no_hp": peserta.no_hp
    }})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('backend')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")


@app.route('/backend')
@login_required
def backend():
    if current_user.role == "registration":
        return redirect(url_for("registrasi"))
    elif current_user.role == "watcher":
        return redirect(url_for("daftar_peserta"))
    else:
        return redirect("/")



@app.route('/backend/registrasi')
@login_required
@requires_roles('registration')
def registrasi():
    total_peserta = PesertaVaksinasi.query.count()
    total_peserta_hadir = PesertaVaksinasi.query.filter(PesertaVaksinasi.hadir == True).count()
    total_peserta_belum_hadir = total_peserta - total_peserta_hadir

    return render_template('backend/registrasi.html',
                           total_peserta=total_peserta,
                           total_peserta_belum_hadir=total_peserta_belum_hadir,
                           total_peserta_hadir=total_peserta_hadir)


@app.route('/backend/daftar-peserta')
@login_required
@requires_roles('watcher')
def daftar_peserta():
    unit_kerja = "%{}%".format(current_user.unit_kerja)
    total_peserta = PesertaVaksinasi.query.filter(PesertaVaksinasi.penyelenggara.like(unit_kerja)).count()
    total_peserta_hadir = PesertaVaksinasi.query.filter(PesertaVaksinasi.hadir == True, PesertaVaksinasi.penyelenggara.like(unit_kerja)).count()
    total_peserta_belum_hadir = total_peserta - total_peserta_hadir
    return render_template('backend/daftar_peserta.html',
                           total_peserta=total_peserta,
                           total_peserta_belum_hadir=total_peserta_belum_hadir,
                           total_peserta_hadir=total_peserta_hadir)



@app.route('/backend/registrasi-kehadiran/<id>')
@login_required
@requires_roles('registration')
def registrasi_kehadiran(id):
    peserta = PesertaVaksinasi.query.get(id)
    if peserta is None:
        # flash("Peserta Tidak Ditemukan")
        return redirect(url_for('registrasi'))

    peserta.hadir = True
    db.session.commit()
    # flash("Registrasi Kehadiran Peserta Berhasil")
    return redirect(url_for('registrasi'))


@app.route('/backend/api/daftar-peserta')
@login_required
def api_daftar_peserta():
    unit_kerja = "%{}%".format(current_user.unit_kerja)
    if current_user.role == "watcher":
        pesertaList = PesertaVaksinasi.query.filter(PesertaVaksinasi.penyelenggara.like(unit_kerja)).all()
    else:
        pesertaList = PesertaVaksinasi.query.all()
    responseList = []
    for peserta in pesertaList:
        if peserta.hadir:
            peserta_hadir = "Sudah Hadir"
        else:
            peserta_hadir = "Belum Hadir"
        responseList.append({
            "id": peserta.id,
            "nik": peserta.nik,
            "nama_lengkap": peserta.nama_lengkap,
            "alamat_ktp": peserta.alamat_ktp,
            "no_hp": peserta.no_hp,
            "batch": peserta.batch,
            "hari_vaksin": peserta.waktu_vaksin,
            "hadir": peserta.hadir,
            "peserta_hadir": peserta_hadir
        })
    return jsonify({"data": responseList})
