from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class PesertaForm(FlaskForm):
    id = HiddenField("ID")
    nama = StringField('Nama', validators=[DataRequired()])
    nik = StringField('NIK', validators=[DataRequired()])
    alamat = StringField('Alamat KTP')
    no_hp = StringField('No Telepon')
    batch = SelectField("Batch", choices=[("BATCH 1", "BATCH 1"), ("BATCH 2", "BATCH 2"), ("BATCH 3", "BATCH 3"), ("BATCH 4", "BATCH 4")])
    jenis_kelamin = SelectField("Jenis Kelamin", choices=[("Laki-Laki", "Laki-Laki"), ("Perempuan", "Perempuan")])
    tanggal_lahir = StringField('Tanggal Lahir')
    umur = StringField('Umur')
    instansi_pekerjaan = StringField('Instansi Pekerjaan')
    jenis_pekerjaan = StringField('Jenis Pekerjaan')
    kode_kabupaten = StringField('Kode Kabupaten/Kota')
    nama_kota = StringField('Nama Kabupaten/Kota')
    waktu_vaksin = StringField('Hari / Tanggal Vaksin')
    penyelenggara = SelectField('Instansi Penyelenggara', choices=[("BNI", "BNI"), ("BRI", "BRI"), ("Mandiri", "Mandiri"), ("BCA", "BCA"), ("CIMB Niaga", "CIMB Niaga"), ("OJK", "OJK"), ("UGM", "UGM") , ("Lainnya", "Lainnya")])
    hadir = BooleanField("Kehadiran")
    sudah_vaksin = BooleanField("Sudah Vaksin")
