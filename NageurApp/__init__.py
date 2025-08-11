from datetime import datetime
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user
from sqlalchemy import select, func
from .models import db, Session, User, Info, Bassin


def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret-key'  # À changer en production

    # Config BDD
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
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

        # thread = threading.Thread(target=simulate_data)
        # thread.daemon = True
        # thread.start()

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
    def load_data():
        last_session = db.session.execute(
            select(Session).order_by(Session.id.desc()).limit(1)
        ).scalar_one_or_none()
        if not last_session:
            return None

        last_info = db.session.execute(
            select(Info)
            .where(Info.session_id == last_session.id)
            .order_by(Info.id.desc())
            .limit(1)
        ).scalar_one_or_none()
        if not last_info:
            return None

        bassin = db.session.execute(
            select(Bassin)
            .order_by(Bassin.id.desc())
            .limit(1)
        ).scalar_one_or_none()
        
        if not bassin:
            return None

        # avg_vitesse = db.session.execute(
        #     select(func.avg(Info.vitesse))
        #     .where(Info.session_id == last_session.id)
        # ).scalar_one_or_none()

        avg_bpm = db.session.execute(
            select(func.avg(Info.bpm))
            .where(Info.session_id == last_session.id)
        ).scalar_one_or_none()

        all_infos = db.session.execute(
            select(Info)
            .where(Info.session_id == last_session.id)
            .order_by(Info.id.asc())
        ).scalars().all()

        temps_total_list = [ info.temps_total for info in all_infos ]
        vitesse_list = [info.vitesse for info in all_infos]
        bpm_list = [info.bpm for info in all_infos]
        swolf_list = [info.swolf for info in all_infos]

        return {
            "longueur_bassin": round(bassin.longueur, 2),
            "nb_longueurs": last_info.nb_longueurs,
            "mouvements_bras": last_info.mouvements_bras,
            "vitesse": round(last_info.vitesse, 2),
            # "moyenne_vitesse": round(avg_vitesse),
            "bpm_instantanne": round(last_info.bpm, 2),
            "swolf": round(last_info.swolf, 2),
            "bpm_moyen": round(avg_bpm, 2),
            "battery": last_info.battery,
            "temps_list": temps_total_list,
            "vitesse_list": vitesse_list,
            "bpm_list": bpm_list,
            "swolf_list": swolf_list,
        }
        
    def load_history():
        sessions_data = []

        # Récupérer toutes les sessions, de la plus récente à la plus ancienne
        all_sessions = db.session.execute(
            select(Session).order_by(Session.id.desc())
        ).scalars().all()

        for session in all_sessions:
            # Dernière info pour cette session
            last_info = db.session.execute(
                select(Info)
                .where(Info.session_id == session.id)
                .order_by(Info.id.desc())
                .limit(1)
            ).scalar_one_or_none()

            if not last_info:
                continue  # On saute si pas de données pour cette session

            # Dernier bassin connu pour cette session
            bassin = db.session.execute(
                select(Bassin)
                .where(Bassin.id == last_info.bassin_id)
                .limit(1)
            ).scalar_one_or_none()

            # Moyennes
            avg_vitesse = db.session.execute(
                select(func.avg(Info.vitesse))
                .where(Info.session_id == session.id)
            ).scalar_one_or_none()
            
            avg_swolf = db.session.execute(
                select(func.avg(Info.swolf))
                .where(Info.session_id == session.id)
            ).scalar_one_or_none()

            avg_bpm = db.session.execute(
                select(func.avg(Info.bpm))
                .where(Info.session_id == session.id)
            ).scalar_one_or_none()

            sessions_data.append({
                "session_id": session.id,
                "date": session.date.strftime("%d/%m/%Y %H:%M:%S"),
                "longueur_bassin": bassin.longueur if bassin else 0,
                "nb_longueurs": last_info.nb_longueurs,
                "mouvements_bras": last_info.mouvements_bras,
                "vitesse_moyenne": round(avg_vitesse, 2),
                "swolf_moyen": round(avg_swolf, 2),
                "bpm_moyen": round(avg_bpm, 2),
            })
        return sessions_data[::-1]


    @app.route('/')
    @login_required
    def index():
        return redirect(url_for('dashboard'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        datas = load_data()
        if datas is None:
            bassin = db.session.execute(select(Bassin).order_by(Bassin.id.desc()).limit(1)
        ).scalar_one_or_none()
            return render_template(
                'dashboard.html',
                longueur_bassin = bassin.longueur if bassin else 0,
                nb_longueurs = 0,
                mouvements_bras = 0,
                vitesse_instantannee = 0,
                # moyenne_vitesse = 0,
                bpm_instantanne = 0,
                swolf = 0,
                bpm_moyen = 0,
                battery = 0,
                temps_list = [],
                vitesse_list = [],
                bpm_list = [],
                swolf_list = [],
            )
        return render_template(
            'dashboard.html',
            longueur_bassin = datas['longueur_bassin'],
            nb_longueurs = datas['nb_longueurs'],
            mouvements_bras = datas['mouvements_bras'],
            vitesse = datas['vitesse'],
            # moyenne_vitesse = datas['moyenne_vitesse'],
            bpm_instantanne = datas['bpm_instantanne'],
            swolf = datas['swolf'],
            bpm_moyen = datas['bpm_moyen'],
            battery = datas['battery'],
            temps_list = datas['temps_list'],
            vitesse_list = datas['vitesse_list'],
            bpm_list = datas['bpm_list'],
            swolf_list = datas['swolf_list'],
        )

    @app.route('/historique')
    @login_required
    def historique():
        datas = load_history()
        return render_template('historique.html', history= datas)

    @app.route('/get_data')
    def data(): 
        return jsonify(success=True, data=load_data())

    @app.post('/set_data')
    def set_data():
        data = request.json
        
        if Session.query.count() == 0 or Bassin.query.count() == 0:
            return jsonify(success=False, message="Longueur de bassin non définie ou Aucune session débutée."), 400
        
        info = Info(
            session_id = Session.query.order_by(Session.id.desc()).first().id,
            bassin_id = Bassin.query.order_by(Bassin.id.desc()).first().id,
            nb_longueurs = data.get("nb_longueurs"),
            battery = int(data.get("battery")),
            mouvements_bras = data.get("mouvements_bras"),
            vitesse = data.get("vitesse"),
            temps_total = data.get("temps_total"),
            bpm = data.get("bpm"),
            swolf = data.get("swolf"),
        )
        db.session.add(info)
        db.session.commit()
        
        return jsonify(
            success = True,
        )

    @app.post('/arduino/<etat>')
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

    @app.post('/set_pool_length')
    @login_required
    def set_length():
        longueur = request.form.get('longueur', type=float)
        print(f"Longueur du bassin définie : {longueur} mètres")
        bassin = Bassin(longueur=longueur)
        db.session.add(bassin)
        db.session.commit()
        return redirect(url_for('dashboard'))

    @app.post('/begin')
    @login_required
    def degin_session():
        session = Session(
            date = datetime.now()
        )
        db.session.add(session)
        db.session.commit()
        return redirect(url_for('dashboard'))

    return app