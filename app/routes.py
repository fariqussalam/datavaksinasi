from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, PesertaForm
from app.models import User, PesertaVaksinasi, requires_roles, Batch


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

    batch = peserta.batch
    batch_upper = batch.upper()
    db_batch = Batch.query.filter_by(nama=batch_upper).first()
    response = {'success': True, 'peserta': {
        "nik": peserta.nik,
        "nama_lengkap": peserta.nama_lengkap,
        "alamat_ktp": peserta.alamat_ktp,
        "no_hp": peserta.no_hp,
        "hari_vaksin": peserta.waktu_vaksin
    }}

    if db_batch is not None:
        response["peserta"]["batch"] = db_batch.nama
        response["peserta"]["waktu"] = db_batch.waktu

    return jsonify(response)


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
    total_peserta_sudah_vaksin = PesertaVaksinasi.query.filter(PesertaVaksinasi.sudah_vaksin == True).count()

    return render_template('backend/registrasi.html',
                           total_peserta=total_peserta,
                           total_peserta_belum_hadir=total_peserta_belum_hadir,
                           total_peserta_hadir=total_peserta_hadir,
                           total_peserta_sudah_vaksin=total_peserta_sudah_vaksin)


@app.route('/backend/registrasi/tambah')
@login_required
@requires_roles('registration')
def tambah_peserta():
    form = PesertaForm()
    return render_template('backend/tambah_peserta.html', form=form)


@app.route('/backend/registrasi/simpan', methods=["POST"])
@login_required
@requires_roles('registration')
def simpan_peserta():
    form = PesertaForm()
    if form.validate_on_submit():
        if form.id.data:
            peserta = PesertaVaksinasi.query.get(form.id.data)
        else:
            peserta = PesertaVaksinasi()
        peserta.nama_lengkap = form.nama.data
        peserta.nik = form.nik.data
        peserta.alamat_ktp = form.alamat.data
        peserta.no_hp = form.no_hp.data
        peserta.batch = form.batch.data
        peserta.jenis_kelamin = form.jenis_kelamin.data
        peserta.tanggal_lahir = form.tanggal_lahir.data
        peserta.umur = form.umur.data
        peserta.instansi_pekerjaan = form.instansi_pekerjaan.data
        peserta.jenis_pekerjaan = form.jenis_pekerjaan.data
        peserta.kode_kabupaten = form.kode_kabupaten.data
        peserta.nama_kota = form.nama_kota.data
        peserta.penyelenggara = form.penyelenggara.data
        peserta.hadir = form.hadir.data
        peserta.waktu_vaksin = form.waktu_vaksin.data
        peserta.sudah_vaksin = form.sudah_vaksin.data
        db.session.add(peserta)
        db.session.commit()
        return redirect(url_for('registrasi'))

    return render_template('backend/tambah_peserta.html', form=form)


@app.route('/backend/registrasi/edit/<id>')
@login_required
@requires_roles('registration')
def edit_peserta(id):
    peserta = PesertaVaksinasi.query.get(id)
    if peserta is None:
        return redirect(url_for('registrasi'))

    form = PesertaForm(obj=peserta)
    form.nama.data = peserta.nama_lengkap
    form.alamat.data = peserta.alamat_ktp
    form.jenis_pekerjaan.data = peserta.jenis_pekerjaan
    return render_template('backend/tambah_peserta.html', form=form, mode="edit")


@app.route('/backend/registrasi/hapus/<id>')
@login_required
@requires_roles('registration')
def hapus_peserta(id):
    peserta = PesertaVaksinasi.query.get(id)
    if peserta is None:
        return redirect(url_for('registrasi'))

    db.session.delete(peserta)
    db.session.commit()
    return redirect(url_for('registrasi'))


@app.route('/backend/daftar-peserta')
@login_required
@requires_roles('watcher')
def daftar_peserta():
    unit_kerja = "%{}%".format(current_user.unit_kerja)
    total_peserta = PesertaVaksinasi.query.filter(PesertaVaksinasi.penyelenggara.like(unit_kerja)).count()
    total_peserta_hadir = PesertaVaksinasi.query.filter(PesertaVaksinasi.hadir == True,
                                                        PesertaVaksinasi.penyelenggara.like(unit_kerja)).count()
    total_peserta_belum_hadir = total_peserta - total_peserta_hadir
    total_peserta_sudah_vaksin = PesertaVaksinasi.query.filter(PesertaVaksinasi.sudah_vaksin == True,
                                                        PesertaVaksinasi.penyelenggara.like(unit_kerja)).count()

    return render_template('backend/daftar_peserta.html',
                           total_peserta=total_peserta,
                           total_peserta_belum_hadir=total_peserta_belum_hadir,
                           total_peserta_hadir=total_peserta_hadir,
                           total_peserta_sudah_vaksin=total_peserta_sudah_vaksin)


@app.route('/backend/registrasi-kehadiran/<id>')
@login_required
@requires_roles('registration')
def registrasi_kehadiran(id):
    peserta = PesertaVaksinasi.query.get(id)
    if peserta is None:
        return redirect(url_for('registrasi'))

    peserta.hadir = True
    db.session.commit()
    return redirect(url_for('registrasi'))


@app.route('/backend/registrasi-sudah-vaksin/<id>')
@login_required
@requires_roles('registration')
def registrasi_sudah_vaksin(id):
    peserta = PesertaVaksinasi.query.get(id)
    if peserta is None:
        return redirect(url_for('registrasi'))

    peserta.sudah_vaksin = True
    db.session.commit()
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

        if peserta.sudah_vaksin:
            sudah_vaksin = "Sudah Vaksin"
        else:
            sudah_vaksin = "Belum Vaksin"
        responseList.append({
            "id": peserta.id,
            "nik": peserta.nik,
            "nama_lengkap": peserta.nama_lengkap,
            "alamat_ktp": peserta.alamat_ktp,
            "no_hp": peserta.no_hp,
            "batch": peserta.batch,
            "hari_vaksin": peserta.waktu_vaksin,
            "hadir": peserta.hadir,
            "peserta_hadir": peserta_hadir,
            "is_sudah_vaksin": peserta.sudah_vaksin,
            "sudah_vaksin": sudah_vaksin,
            "penyelenggara": peserta.penyelenggara
        })
    return jsonify({"data": responseList})
