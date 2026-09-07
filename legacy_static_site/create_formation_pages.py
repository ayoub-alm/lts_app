import os

template = """<!doctype html>
<html lang="fr">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title} - LTS ACADEMY</title>
    <link rel="shortcut icon" href="../ltsAcademy.png" type="image/x-icon">
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Bootstrap Icons -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet" />
    <!-- Custom CSS -->
    <link rel="stylesheet" href="../css/style.css">
  </head>
  <body>

  <!-- Navbar -->
  <nav class="navbar navbar-expand-lg fixed-top" style="background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
    <div class="container">
      <a class="navbar-brand d-flex align-items-center" href="../index.html">
        <img src="../ltsAcademy.png" alt="LTS Academy" width="40" height="40" class="me-2">
        <span style="font-weight: 500; color: #1a73e8;">LTS ACADEMY</span>
      </a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="navbarNavDropdown">
        <ul class="navbar-nav gap-2">
          <li class="nav-item"><a class="nav-link" href="../index.html">Accueil</a></li>
          <li class="nav-item"><a class="nav-link" href="../impact.html">Étude d’Impact</a></li>
          <li class="nav-item"><a class="nav-link" href="../impact-environnement.html">Impact Environnement</a></li>
          <li class="nav-item"><a class="nav-link active" href="../poles.html">Nos Pôles</a></li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">Formations</a>
            <ul class="dropdown-menu border-0 shadow-lg" style="border-radius: 12px;">
              <li><a class="dropdown-item" href="marketing.html">Marketing Digital</a></li>
              <li><a class="dropdown-item" href="rh.html">Ressources Humaines</a></li>
              <li><a class="dropdown-item" href="logistique.html">Logistique</a></li>
              <li><a class="dropdown-item" href="web-development.html">Développement Web</a></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item text-primary" href="../poles.html">Voir toutes</a></li>
            </ul>
          </li>
          <li class="nav-item"><a class="nav-link btn btn-primary-custom text-white ms-lg-3 px-4" href="../index.html#contact" style="background-color: #1a73e8; border-radius: 50px;">Contact</a></li>
        </ul>
      </div>
    </div>
  </nav>

  <!-- Hero Section -->
  <header class="hero-section" style="background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{image_url}') center/cover no-repeat;">
    <div class="container text-center text-white py-5">
      <h1 class="display-3 fw-bold hero-title text-white mt-5">{title}</h1>
      <p class="lead mb-4">{subtitle}</p>
      <a href="#details" class="btn btn-primary-custom btn-lg">Découvrir le programme</a>
    </div>
  </header>

  <!-- Content Section -->
  <section id="details" class="py-5">
    <div class="container">
      <div class="row g-5">
        <div class="col-lg-8">
          <div class="glass-panel p-4 mb-4">
            <h2 class="section-title mb-4">Description</h2>
            <p>{description}</p>
          </div>

          <div class="glass-panel p-4 mb-4">
            <h2 class="section-title mb-4">Programme de la formation</h2>
            <ul class="list-group list-group-flush bg-transparent">
              {modules_html}
            </ul>
          </div>

          <div class="glass-panel p-4">
            <h2 class="section-title mb-4">Débouchés Professionnels</h2>
            <ul class="list-unstyled">
              {opportunities_html}
            </ul>
          </div>
        </div>

        <div class="col-lg-4">
          <div class="card border-0 shadow-lg sticky-top" style="top: 100px; border-radius: 20px;">
            <div class="card-body p-4">
              <h4 class="fw-bold mb-3">Détails pratiques</h4>
              <ul class="list-unstyled mb-4">
                <li class="mb-2"><i class="bi bi-clock me-2 text-primary"></i> <strong>Durée:</strong> {duration}</li>
                <li class="mb-2"><i class="bi bi-calendar-check me-2 text-primary"></i> <strong>Mode:</strong> {mode}</li>
                <li class="mb-2"><i class="bi bi-award me-2 text-primary"></i> <strong>Certification:</strong> {certification}</li>
              </ul>
              <div class="d-grid">
                <a href="../index.html#contact" class="btn btn-primary-custom">S'inscrire maintenant</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer class="text-center text-lg-start bg-dark text-white pt-4">
    <div class="container p-4">
      <div class="text-center">
        <p>&copy; 2025 LTS Academy. Tous droits réservés.</p>
      </div>
    </div>
  </footer>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>
"""

formations = [
    {
        "filename": "marketing.html",
        "title": "Marketing Digital",
        "subtitle": "Devenez un expert en stratégie digitale et communication web.",
        "image_url": "https://images.unsplash.com/photo-1533750516457-a7f992034fec?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80",
        "description": "Cette formation vous permet de maîtriser les outils du webmarketing, du SEO aux réseaux sociaux, pour booster la visibilité et les ventes d'une entreprise.",
        "modules": ["Stratégie Digitale", "SEO / SEA", "Community Management", "Publicité en ligne (Ads)", "Analyse de données"],
        "opportunities": ["Chef de projet digital", "Community Manager", "Consultant SEO", "Traffic Manager"],
        "duration": "6 mois",
        "mode": "Hybride (Présentiel/Distanciel)",
        "certification": "Certificat Professionnel"
    },
    {
        "filename": "rh.html",
        "title": "Ressources Humaines",
        "subtitle": "Gérez le capital humain et développez les talents.",
        "image_url": "https://images.unsplash.com/photo-1521791136064-7986c2920216?ixlib=rb-4.0.3&auto=format&fit=crop&w=1469&q=80",
        "description": "Apprenez à gérer le recrutement, la paie, la formation et les relations sociales au sein de l'entreprise.",
        "modules": ["Droit du travail", "Gestion de la paie", "Recrutement", "Communication interne", "GPEC"],
        "opportunities": ["Assistant RH", "Chargé de recrutement", "Gestionnaire de paie", "Responsable formation"],
        "duration": "8 mois",
        "mode": "Présentiel",
        "certification": "Diplôme Agréé"
    },
    {
        "filename": "finance.html",
        "title": "Comptabilité et Finance",
        "subtitle": "Maîtrisez les chiffres clés de l'entreprise.",
        "image_url": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80",
        "description": "Une formation complète pour devenir autonome en comptabilité générale, analytique et en gestion financière.",
        "modules": ["Comptabilité générale", "Fiscalité", "Contrôle de gestion", "Logiciels comptables (Sage)", "Analyse financière"],
        "opportunities": ["Comptable", "Assistant comptable", "Contrôleur de gestion", "Auditeur junior"],
        "duration": "10 mois",
        "mode": "Présentiel",
        "certification": "Diplôme Technicien Spécialisé"
    },
    {
        "filename": "logistique.html",
        "title": "Logistique et Transport",
        "subtitle": "Optimisez la chaîne d'approvisionnement et les flux.",
        "image_url": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80",
        "description": "Devenez un acteur clé de la Supply Chain en maîtrisant les processus de transport, stockage et distribution.",
        "modules": ["Gestion des stocks", "Transport international", "Achats et approvisionnements", "Réglementation douanière", "Supply Chain Management"],
        "opportunities": ["Responsable logistique", "Agent de transit", "Gestionnaire de stock", "Responsable d'entrepôt"],
        "duration": "8 mois",
        "mode": "Hybride",
        "certification": "Certificat de Qualification"
    },
    {
        "filename": "design.html",
        "title": "Infographie et Design",
        "subtitle": "Exprimez votre créativité à travers le design graphique.",
        "image_url": "https://images.unsplash.com/photo-1626785774573-4b799312c95d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80",
        "description": "Maîtrisez la suite Adobe (Photoshop, Illustrator, InDesign) et les principes du design pour créer des visuels percutants.",
        "modules": ["Adobe Photoshop", "Adobe Illustrator", "Adobe InDesign", "Théorie des couleurs", "Identité visuelle"],
        "opportunities": ["Graphiste", "Infographiste", "Directeur artistique junior", "Maquettiste"],
        "duration": "6 mois",
        "mode": "Présentiel",
        "certification": "Certificat de Compétence"
    },
    {
        "filename": "systemes-reseaux.html",
        "title": "Systèmes et Réseaux",
        "subtitle": "Assurez la connectivité et la sécurité des infrastructures.",
        "image_url": "https://images.unsplash.com/photo-1558494949-ef526b0042a0?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80",
        "description": "Formation technique pour installer, configurer et maintenir les réseaux informatiques et les serveurs d'entreprise.",
        "modules": ["Architecture réseaux (CCNA)", "Administration Windows Server", "Linux", "Virtualisation", "Sécurité de base"],
        "opportunities": ["Administrateur réseaux", "Technicien support", "Administrateur système", "Technicien déploiement"],
        "duration": "9 mois",
        "mode": "Présentiel",
        "certification": "Diplôme Agréé"
    },
    {
        "filename": "big-data.html",
        "title": "Big Data et IA",
        "subtitle": "Entrez dans l'ère de la donnée et de l'intelligence artificielle.",
        "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80",
        "description": "Apprenez à collecter, traiter et analyser des volumes massifs de données pour en extraire de la valeur.",
        "modules": ["Python pour la Data", "Machine Learning", "Bases de données NoSQL", "Data Visualization", "Deep Learning"],
        "opportunities": ["Data Analyst", "Data Scientist Junior", "Ingénieur Big Data", "Consultant BI"],
        "duration": "12 mois",
        "mode": "Hybride",
        "certification": "Master / Expert"
    }
]

def create_page(formation):
    modules_html = "".join([f'<li class="list-group-item bg-transparent"><i class="bi bi-check2-circle text-success me-2"></i> {m}</li>' for m in formation["modules"]])
    opportunities_html = "".join([f'<li class="mb-2"><i class="bi bi-briefcase me-2 text-secondary"></i> {o}</li>' for o in formation["opportunities"]])

    content = template.format(
        title=formation["title"],
        subtitle=formation["subtitle"],
        image_url=formation["image_url"],
        description=formation["description"],
        modules_html=modules_html,
        opportunities_html=opportunities_html,
        duration=formation["duration"],
        mode=formation["mode"],
        certification=formation["certification"]
    )

    filepath = os.path.join("formations", formation["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {filepath}")

def main():
    if not os.path.exists("formations"):
        os.makedirs("formations")

    for formation in formations:
        create_page(formation)

if __name__ == "__main__":
    main()
