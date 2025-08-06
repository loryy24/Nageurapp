from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from .simulateur import data_buffer, simulate_data
from .models import db, Session, BpmLog, User
import threading


def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret-key'  # À changer en production

    # Config BDD
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/nageur_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Connexion Arduino
    try:
        import serial
        arduino = serial.Serial('COM3', 9600, timeout=1)
    except Exception as e:
        print("Erreur de connexion Arduino :", e)
        arduino = None

    with app.app_context():
        db.create_all()

        thread = threading.Thread(target=simulate_data)
        thread.daemon = True
        thread.start()

    # AUTHENTIFICATION

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            user = User.query.filter_by(email=email).first()
            
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash("Email ou mot de passe invalide", 'danger')
        return render_template('login.html')
        


    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')

            if password != confirm_password:
                flash("Les mots de passe ne correspondent pas", 'danger')
                return redirect(url_for('register'))

            if User.query.filter_by(email=email).first():
                flash("Cet email est déjà utilisé", 'warning')
                return redirect(url_for('register'))

            new_user = User(email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash("Compte créé avec succès. Connectez-vous.", 'success')
            return redirect(url_for('login'))

        return render_template('register.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    # ROUTES UTILISATEUR

    @app.route('/')
    @login_required
    def index():
        donnees = data_buffer[-1] if data_buffer else {}
        return render_template('index.html', donnees=donnees)

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/historique')
    @login_required
    def historique():
        historique = BpmLog.query.order_by(BpmLog.timestamp.desc()).limit(50).all()
        return render_template('historique.html', historique=historique)

    @app.route('/data')
    @login_required
    def data():
        if data_buffer:
            return jsonify(data_buffer[-1])
        return jsonify({})

    @app.route('/set_coach', methods=['POST'])
    @login_required
    def set_coach():
        coach_name = request.form.get('coach')
        print("Coach assigné :", coach_name)
        return '', 204

    @app.route('/arduino/<etat>', methods=['POST'])
    @login_required
    def arduino_toggle(etat):
        if etat not in ['on', 'off']:
            return 'État invalide', 400

        if arduino and arduino.is_open:
            try:
                arduino.write(f"{etat}\n".encode('utf-8'))
                return f"Commande {etat.upper()} envoyée à Arduino", 200
            except Exception as e:
                return f"Erreur lors de l'envoi : {e}", 500
        return "Arduino non connecté", 500

    return app
