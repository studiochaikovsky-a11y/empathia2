"""
Creates /fr/index.html and /ar/index.html from index.html.
Run from C:/Users/Настя/Desktop/клод/
"""
import os, re

BASE = r'C:/Users/Настя/Desktop/клод'

with open(os.path.join(BASE, 'index.html'), 'r', encoding='utf-8') as f:
    SRC = f.read()

# ──────────────────────────────────────────────────────────
# COMMON PATH FIXES  (same for FR and AR)
# ──────────────────────────────────────────────────────────
def fix_paths(html):
    html = html.replace('href="index.css?', 'href="../index.css?')
    html = html.replace("href='index.css?", "href='../index.css?")
    html = html.replace('src="mobile-nav.js?', 'src="../mobile-nav.js?')
    html = html.replace("src='mobile-nav.js?", "src='../mobile-nav.js?")
    html = re.sub(r'src="assets/', 'src="../assets/', html)
    html = re.sub(r"src='assets/", "src='../assets/", html)
    html = re.sub(r'href="assets/', 'href="../assets/', html)
    for page in ['residencies','pricing','gallery','construction','blog','faq','agents','contact','about',
                 'aldabra-giant-tortoises-seychelles','baie-lazare-beach-seychelles',
                 'buying-property-in-seychelles','freehold-property-seychelles',
                 'kensington-construction-seychelles','phase-i-construction-update',
                 'seychelles-island-lifestyle','seychelles-residency-by-investment']:
        html = html.replace(f'href="{page}.html"', f'href="../{page}.html"')
    html = html.replace('href="index.html"', 'href="../"')
    html = html.replace("href='index.html'", "href='../'")
    # goTo('#contact') anchor links stay as-is
    return html

def fix_meta_fr(html):
    html = html.replace('<html lang="en">', '<html lang="fr">')
    html = html.replace(
        'content="https://empathia-seychelles.com/"',
        'content="https://empathia-seychelles.com/fr/"'
    )
    html = html.replace(
        'href="https://empathia-seychelles.com/"',
        'href="https://empathia-seychelles.com/fr/"'
    )
    # hreflang block already in index.html — update canonical only
    html = html.replace(
        '<link rel="canonical" href="https://empathia-seychelles.com/">',
        '<link rel="canonical" href="https://empathia-seychelles.com/fr/">'
    )
    html = html.replace(
        '<title>Luxury Villas for Sale in Seychelles | Empathia Village Baie Lazare</title>',
        '<title>Villas de Luxe à Vendre aux Seychelles | Empathia Village Baie Lazare</title>'
    )
    old_desc = 'content="Luxury freehold villas for sale in Baie Lazare, Seychelles. Private gated community between Four Seasons &amp; Kempinski — 35 private plots from 600 m², villas from $990,000. Staged payments. Agent programme from 3%."'
    new_desc = 'content="Villas en pleine propriété à vendre à Baie Lazare, Seychelles. Communauté privée entre Four Seasons &amp; Kempinski — 35 parcelles dès 600 m², villas à partir de $990 000. Paiements échelonnés. Programme agent dès 3 %."'
    html = html.replace(old_desc, new_desc)
    return html

def fix_meta_ar(html):
    html = html.replace('<html lang="en">', '<html lang="ar" dir="rtl">')
    html = html.replace(
        'content="https://empathia-seychelles.com/"',
        'content="https://empathia-seychelles.com/ar/"'
    )
    html = html.replace(
        'href="https://empathia-seychelles.com/"',
        'href="https://empathia-seychelles.com/ar/"'
    )
    html = html.replace(
        '<link rel="canonical" href="https://empathia-seychelles.com/">',
        '<link rel="canonical" href="https://empathia-seychelles.com/ar/">'
    )
    html = html.replace(
        '<title>Luxury Villas for Sale in Seychelles | Empathia Village Baie Lazare</title>',
        '<title>فلل فاخرة للبيع في جزر سيشيل | Empathia Village</title>'
    )
    old_desc = 'content="Luxury freehold villas for sale in Baie Lazare, Seychelles. Private gated community between Four Seasons &amp; Kempinski — 35 private plots from 600 m², villas from $990,000. Staged payments. Agent programme from 3%."'
    new_desc = 'content="فلل فاخرة بملكية حرة للبيع في Baie Lazare، جزر سيشيل. 35 قطعة خاصة من 600 م²، فلل تبدأ من $990,000. دفعات مرحلية. برنامج الوكلاء من 3٪."'
    html = html.replace(old_desc, new_desc)
    # Insert RTL styles after <head>
    rtl_style = '''<style id="rtl-overrides">
body{direction:rtl;text-align:right}
.nav{flex-direction:row-reverse}
.nav-links{flex-direction:row-reverse}
#topbar{flex-direction:row-reverse}
.hero-content{text-align:right}
.hero-h1,.hero-tagline{text-align:right}
.hero-actions{justify-content:flex-start}
.feat-strip{flex-direction:row-reverse}
.loc-row{flex-direction:row-reverse}
.faq-q{flex-direction:row-reverse}
.acq-grid{direction:rtl}
.vd-cols{flex-direction:row-reverse}
.vd-left{text-align:right}
.inv-row{flex-direction:row-reverse}
.inv-num{margin-right:0;margin-left:24px}
.loc-roman{margin-right:0;margin-left:20px}
</style>
<link rel="preload" href="https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;500;600;700&display=swap" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;500;600;700&display=swap"></noscript>
<style>body,p,div,span,button,input,select,a,.body,.lead{font-family:\'Noto Naskh Arabic\',var(--sans),sans-serif}
h1,h2,h3,.h2,.h3,.hero-h1{font-family:\'Noto Naskh Arabic\',var(--serif),serif}
</style>'''
    html = html.replace('</head>', rtl_style + '\n</head>')
    return html

# ──────────────────────────────────────────────────────────
# FRENCH TRANSLATIONS  (ordered: longest strings first to avoid partial matches)
# ──────────────────────────────────────────────────────────
FR = [
    # Page / nav
    ('Private Living · Naturally Yours', 'Vie Privée · Naturellement Vôtre'),
    ('Home', 'Accueil'),
    ('Residencies', 'Résidences'),
    ('Pricing', 'Tarifs'),
    ('Gallery', 'Galerie'),
    ('Construction', 'Construction'),
    ('Agents', 'Agents'),
    ('Contacts', 'Contact'),
    ('Private Enquiry', 'Demande Privée'),

    # Hero
    ('Private Luxury Villas<br>in Seychelles', 'Villas de Luxe Privées<br>aux Seychelles'),
    ('Freehold Title · Staged Payments · Between Four Seasons &amp; Kempinski',
     'Pleine propriété · Paiements échelonnés · Entre Four Seasons &amp; Kempinski'),
    ('35 Private Plots', '35 Parcelles privées'),
    ('From $990,000', 'À partir de $990 000'),
    ('12 Months Build', 'Construction 12 mois'),
    ('Rental Potential', 'Potentiel locatif'),
    ('Request Full Presentation', 'Demander la présentation complète'),
    ('View Residences', 'Voir les résidences'),
    ('WhatsApp', 'WhatsApp'),
    ('Scroll', 'Défiler'),

    # Stats bar
    ('Private Plots', 'Parcelles privées'),
    ('Starting Price', 'Prix de départ'),
    ('To Beach', 'De la plage'),
    ('Developer Experience', 'Expérience promoteur'),
    ('Homes Delivered', 'Résidences livrées'),

    # About
    ('The Estate', 'Le Domaine'),
    ('A new standard<br>of private luxury living', 'Un nouveau standard<br>de vie privée de luxe'),
    ('Kensington Construction &amp; Development presents a gated community of luxury villas on Mahé island — positioned at Baie Lazare beach, between the legendary Four Seasons Resort Seychelles and Kempinski Seychelles Resort.',
     'Kensington Construction &amp; Development présente une communauté résidentielle fermée de villas de luxe sur l\'île de Mahé — située à Baie Lazare, entre le légendaire Four Seasons Resort Seychelles et le Kempinski Seychelles Resort.'),
    ('The estate occupies elevated terrain at 50–100 metres above sea level. The terraced layout ensures most residences command uninterrupted panoramas of the Indian Ocean and tropical sunsets.',
     'Le domaine occupe un terrain surélevé à 50–100 mètres au-dessus du niveau de la mer. La disposition en terrasses garantit à la plupart des résidences des vues panoramiques ininterrompues sur l\'océan Indien et les couchers de soleil tropicaux.'),
    ('"Empathy is what restores a lost paradise"', '« L\'empathie est ce qui restaure un paradis perdu »'),
    ('Built on Trust · Designed for Life · Class 1 License', 'Fondé sur la confiance · Conçu pour la vie · Licence Classe 1'),

    # Features strip
    ('Freehold Title', 'Pleine propriété'),
    ('Foreign buyers may acquire freehold title to villa and land, subject to applicable approvals and transaction procedures confirmed individually with the legal team',
     'Les acheteurs étrangers peuvent acquérir le titre de pleine propriété de la villa et du terrain, sous réserve des approbations applicables et des procédures de transaction confirmées individuellement avec l\'équipe juridique'),
    ('Staged Payments', 'Paiements échelonnés'),
    ('Flexible payment schedule in USD, EUR or GBP, aligned with construction milestones',
     'Calendrier de paiement flexible en USD, EUR ou GBP, aligné sur les jalons de construction'),
    ('Residency', 'Résidence'),
    ('Residence options may be available to eligible purchasers under Seychelles regulations, confirmed individually during the transaction process',
     'Des options de résidence peuvent être disponibles pour les acheteurs éligibles en vertu des réglementations des Seychelles, confirmées individuellement lors du processus de transaction'),
    ('Indicative short-term rental rates from $2,000/night for comparable luxury villas in Baie Lazare. Professional management available. Subject to market conditions — no guaranteed income.',
     'Tarifs locatifs indicatifs à partir de $2 000/nuit pour des villas de luxe comparables à Baie Lazare. Gestion professionnelle disponible. Soumis aux conditions du marché — aucun revenu garanti.'),

    # Cinematic 1
    ('The Setting', 'Le Cadre'),
    ('Between<br>Four Seasons<br>&amp; Kempinski', 'Entre<br>Four Seasons<br>&amp; Kempinski'),
    ('An address defined by its neighbours. Baie Lazare is consistently ranked among the Indian Ocean\'s most beautiful bays — and Empathia Village occupies its finest elevated position.',
     'Une adresse définie par ses voisins. Baie Lazare est régulièrement classée parmi les plus belles baies de l\'océan Indien — et Empathia Village en occupe la plus belle position surélevée.'),
    ('Arrange a Private Visit', 'Organiser une visite privée'),

    # Location
    ('Location', 'Localisation'),
    ('The Finest Address<br>in Seychelles', 'La Plus Belle Adresse<br>des Seychelles'),
    ('2 Minutes to Baie Lazare', '2 minutes de Baie Lazare'),
    ('White sand, turquoise water and granite boulders. One of the island\'s most celebrated beaches — within walking distance',
     'Sable blanc, eau turquoise et rochers de granit. L\'une des plages les plus célèbres de l\'île — à distance de marche'),
    ('Between Four Seasons &amp; Kempinski', 'Entre Four Seasons et Kempinski'),
    ('The estate shares a boundary with Kempinski Seychelles Resort. Premium location with direct access to resort-level amenities and services',
     'Le domaine partage une limite avec le Kempinski Seychelles Resort. Emplacement premium avec accès direct aux équipements et services de niveau resort'),
    ('30 Minutes from Mahé Airport', '30 minutes de l\'aéroport de Mahé'),
    ('Direct flights from Europe, the Middle East and Asia. Private transfers arranged on request',
     'Vols directs depuis l\'Europe, le Moyen-Orient et l\'Asie. Transferts privés organisés sur demande'),
    ('Elevated Panoramic Position', 'Position panoramique surélevée'),
    ('Situated 50–100 metres above sea level on terraced terrain. Most residences enjoy unobstructed views of the Indian Ocean',
     'Situé à 50–100 mètres au-dessus du niveau de la mer sur un terrain en terrasses. La plupart des résidences jouissent de vues dégagées sur l\'océan Indien'),
    ('International School &amp; Medical', 'École internationale et médical'),
    ('British Catholic mission with hospital and school directly opposite the estate. Children of residents are eligible to attend',
     'Mission catholique britannique avec hôpital et école directement en face du domaine. Les enfants des résidents sont éligibles pour y être inscrits'),
    ('World-class dining and resort amenities within five minutes.', 'Restaurants de classe mondiale et équipements de resort à cinq minutes.'),

    # Map
    ('Find Us', 'Nous trouver'),
    ('Project Location', 'Localisation du projet'),
    ('Open in Google Maps', 'Ouvrir dans Google Maps'),
    ('Four Seasons Resort Seychelles — adjacent', 'Four Seasons Resort Seychelles — adjacent'),
    ('Kempinski Seychelles Resort — shared boundary', 'Kempinski Seychelles Resort — limite commune'),
    ('Baie Lazare Beach — 2 minutes on foot', 'Plage de Baie Lazare — 2 minutes à pied'),
    ('Mahé International Airport — 30 minutes by car', 'Aéroport International de Mahé — 30 minutes en voiture'),
    ('Located between Four Seasons Resort Seychelles and Kempinski Seychelles Resort', 'Situé entre le Four Seasons Resort Seychelles et le Kempinski Seychelles Resort'),

    # Masterplan
    ('Masterplan', 'Plan d\'ensemble'),
    ('35 Private Plots<br>in Natural Terrain', '35 Parcelles Privées<br>en Terrain Naturel'),
    ('The estate is designed as a private gated community of 35 individually numbered plots ranging from 600 to 2,000 m².',
     'Le domaine est conçu comme une communauté résidentielle privée et fermée de 35 parcelles numérotées individuellement allant de 600 à 2 000 m².'),
    ('Architecture integrates seamlessly with the tropical landscape — villas are positioned to maximise privacy, ocean views and natural ventilation.',
     'L\'architecture s\'intègre harmonieusement au paysage tropical — les villas sont positionnées pour maximiser la confidentialité, les vues sur l\'océan et la ventilation naturelle.'),
    ('Each villa is built to a carefully considered design by Kensington Construction &amp; Development, incorporating tropical luxury architecture, panoramic glazing, natural materials and private pools.',
     'Chaque villa est construite selon une conception soigneusement étudiée par Kensington Construction &amp; Development, intégrant une architecture de luxe tropical, des vitrages panoramiques, des matériaux naturels et des piscines privées.'),
    ('<strong style="color:rgba(255,255,255,.8);font-weight:500">Plot numbers &amp; availability:</strong> All 35 plots are individually numbered. A full plot map with numbers, sizes, orientations and current availability is included in our presentation pack — sent to qualified enquiries within 24 hours.',
     '<strong style="color:rgba(255,255,255,.8);font-weight:500">Numéros de parcelles &amp; disponibilité :</strong> Les 35 parcelles sont numérotées individuellement. Un plan complet avec numéros, superficies, orientations et disponibilité actuelle est inclus dans notre dossier de présentation — envoyé aux demandes qualifiées sous 24 heures.'),
    ('Request plot map →', 'Demander le plan des parcelles →'),
    ('Total Plots', 'Parcelles totales'),
    ('m² per Plot', 'm² par parcelle'),
    ('Phase I Reserved', 'Phase I réservée'),
    ('Full Completion', 'Livraison complète'),
    ('Estate Masterplan · 2026', 'Plan d\'ensemble · 2026'),

    # Why Seychelles
    ('Investment Destination', 'Destination d\'investissement'),
    ('Why Seychelles?', 'Pourquoi les Seychelles ?'),
    ('Few destinations in the world offer the rare combination of natural beauty, political stability and genuine scarcity of premium land. Seychelles is one of them.',
     'Peu de destinations dans le monde offrent la combinaison rare de beauté naturelle, de stabilité politique et de véritable rareté des terres premium. Les Seychelles en font partie.'),
    ('Land Supply', 'Offre foncière'),
    ('Seychelles is an archipelago of 115 islands covering just 459 km². Developable oceanfront land is finite and irreplaceable — once acquired, it does not return to the market.',
     'Les Seychelles sont un archipel de 115 îles couvrant seulement 459 km². Les terrains bord de mer constructibles sont finis et irremplaçables — une fois acquis, ils ne reviennent pas sur le marché.'),
    ('Jurisdiction', 'Juridiction'),
    ('A business-friendly and internationally recognised jurisdiction.',
     'Une juridiction favorable aux affaires et reconnue internationalement.'),
    ('Specific tax implications depend on the buyer\'s structure and should be confirmed with qualified advisors. One of the most stable property markets in the Indian Ocean region.',
     'Les implications fiscales spécifiques dépendent de la structure de l\'acheteur et doivent être confirmées par des conseillers qualifiés. L\'un des marchés immobiliers les plus stables de la région de l\'océan Indien.'),
    ('Global', 'Mondial'),
    ('Demand', 'Demande'),
    ('Year-round demand from European, Middle Eastern and Asian high-net-worth buyers.',
     'Demande toute l\'année de la part d\'acheteurs fortunés européens, moyen-orientaux et asiatiques.'),
    ('Seychelles is one of the world\'s foremost luxury travel and lifestyle destinations.',
     'Les Seychelles sont l\'une des principales destinations de voyage de luxe et de style de vie au monde.'),
    ('Freehold', 'Pleine propriété'),
    ('Ownership', 'Propriété'),
    ('Rare freehold title opportunities available to international buyers, subject to applicable approvals and transaction procedures confirmed individually with the legal team.',
     'Opportunités rares de titre en pleine propriété disponibles pour les acheteurs internationaux, sous réserve des approbations applicables et des procédures de transaction confirmées individuellement avec l\'équipe juridique.'),
    ('Premium', 'Premium'),
    ('Rental Potential', 'Potentiel locatif'),
    ('Strong year-round demand for luxury villa rentals. Professional management available, allowing owners to generate income when the property is not in personal use.',
     'Forte demande toute l\'année pour la location de villas de luxe. Gestion professionnelle disponible, permettant aux propriétaires de générer des revenus lorsque la propriété n\'est pas en usage personnel.'),
    ('Island', 'Île'),
    ('Lifestyle', 'Art de vivre'),
    ('Turquoise lagoons, tropical rainforest, world-class resorts and a pace of life that cannot be replicated.',
     'Lagon turquoise, forêt tropicale, resorts de classe mondiale et un rythme de vie unique.'),
    ('Seychelles is not just an investment — it is a complete way of living.',
     'Les Seychelles ne sont pas seulement un investissement — c\'est un mode de vie complet.'),

    # Villas
    ('The Collection', 'La Collection'),
    ('Three Villa Designs', 'Trois Conceptions de Villas'),
    ('Each residence is conceived for maximum privacy, panoramic views and effortless tropical living. Private pools, generous terraces and natural materials throughout.',
     'Chaque résidence est conçue pour une confidentialité maximale, des vues panoramiques et une vie tropicale sans effort. Piscines privées, terrasses généreuses et matériaux naturels partout.'),
    ('All Residences', 'Toutes les résidences'),
    ('Entry-level private villa', 'Villa d\'entrée de gamme'),
    ('Elegant ocean-view villa', 'Villa élégante avec vue mer'),
    ('Flagship residence', 'Résidence phare'),
    ('View Details', 'Voir les détails'),
    ('Request Price List', 'Demander le tarif'),
    ('Plot from', 'Parcelle dès'),
    ('House from', 'Maison dès'),
    ('Bedrooms', 'Chambres'),
    ('Bathrooms', 'Salles de bain'),
    ('Residence', 'Résidence'),
    ('Signature Residence', 'Résidence Signature'),
    ('m² Area', 'm² Surface'),
    ('m² Terrace', 'm² Terrasse'),
    ('m² Pool', 'm² Piscine'),
    ('m² Plot', 'm² Parcelle'),
    ('Private', 'Privée'),
    ('Pool', 'Piscine'),
    ('Get Villa Price List', 'Obtenir le tarif de la villa'),

    # Villa Anna desc
    ('An elegant single-storey residence designed for seamless indoor-outdoor living. Panoramic glazing, master suite with dressing room, open-plan living and dining, private pool and sun terrace. The project can be individually tailored to client requirements.',
     'Une élégante résidence de plain-pied conçue pour une vie intérieure-extérieure fluide. Vitrage panoramique, suite parentale avec dressing, séjour et salle à manger ouverts, piscine privée et terrasse ensoleillée. Le projet peut être adapté individuellement aux exigences du client.'),
    ('Open-plan living &amp; dining room', 'Séjour et salle à manger ouverts'),
    ('Master bedroom with dressing room', 'Suite parentale avec dressing'),
    ('Private pool &amp; sun terrace', 'Piscine privée et terrasse ensoleillée'),
    ('Individual project customisation available', 'Personnalisation individuelle du projet disponible'),
    ('Parking for 2 vehicles', 'Parking pour 2 véhicules'),
    ('Architectural Project', 'Projet Architectural'),
    ('From $1,500,000. Plot from 600 m². Individual adjustments to design, size and layout available on request. Not a public offer.',
     'À partir de $1 500 000. Parcelle dès 600 m². Ajustements individuels du design, de la taille et de la disposition disponibles sur demande. Pas une offre publique.'),

    # Villa Georgette desc
    ('The flagship two-storey residence featuring wide panoramic balconies, terraces of 150 m² and a grand private pool. The finest residence in the collection — commanding unobstructed views of the Indian Ocean. Can be expanded up to 450 m².',
     'La résidence phare à deux étages dotée de larges balcons panoramiques, de terrasses de 150 m² et d\'une grande piscine privée. La plus belle résidence de la collection — offrant des vues dégagées sur l\'océan Indien. Peut être agrandie jusqu\'à 450 m².'),
    ('Two floors with panoramic balconies', 'Deux étages avec balcons panoramiques'),
    ('4 bedrooms · Master suite', '4 chambres · Suite parentale'),
    ('Individual customisation up to 450 m²', 'Personnalisation individuelle jusqu\'à 450 m²'),
    ('From $2,100,000. Plot from 1,500 m². All designs can be individually adapted. Not a public offer.',
     'À partir de $2 100 000. Parcelle dès 1 500 m². Tous les designs peuvent être adaptés individuellement. Pas une offre publique.'),

    # Villa Jane desc
    ('A refined single-storey residence with panoramic glazing framing views of the tropical landscape and the Indian Ocean. The most accessible entry point to the Empathia Village collection. Plot from 600 m². Design can be extended and adapted.',
     'Une résidence de plain-pied raffinée avec vitrage panoramique encadrant des vues sur le paysage tropical et l\'océan Indien. Le point d\'entrée le plus accessible de la collection Empathia Village. Parcelle dès 600 m². Le design peut être étendu et adapté.'),
    ('Panoramic floor-to-ceiling glazing', 'Vitrage panoramique sol-plafond'),
    ('2 bedrooms · Private pool', '2 chambres · Piscine privée'),
    ('Individual customisation available', 'Personnalisation individuelle disponible'),
    ('From $990,000. Plot from 600 m². Design, size and layout can be individually tailored. Not a public offer.',
     'À partir de $990 000. Parcelle dès 600 m². Le design, la taille et la disposition peuvent être adaptés individuellement. Pas une offre publique.'),

    # Pricing
    ('Pricing', 'Tarifs'),
    ('Villa Pricing', 'Tarification des villas'),
    ('Three residences. Each priced to reflect plot size, design and ocean view. All prices include land, construction, finishing and landscaping. All plots are at least 600 m².',
     'Trois résidences. Chacune au prix qui reflète la taille de la parcelle, le design et la vue mer. Tous les prix incluent le terrain, la construction, les finitions et l\'aménagement paysager. Toutes les parcelles font au moins 600 m².'),
    ('from 140 m² · 2 Bedrooms', 'dès 140 m² · 2 Chambres'),
    ('from 240 m² · 3 Bedrooms', 'dès 240 m² · 3 Chambres'),
    ('from 240 m²', 'dès 240 m²'),
    ('from 350 m² · 4 Bedrooms', 'dès 350 m² · 4 Chambres'),
    ('Plot from 600 m² · Not a public offer', 'Parcelle dès 600 m² · Pas une offre publique'),
    ('Plot from 1,500 m² · Not a public offer', 'Parcelle dès 1 500 m² · Pas une offre publique'),
    ('2 bedrooms · private pool', '2 chambres · piscine privée'),
    ('Panoramic glazing · ocean views', 'Vitrage panoramique · vues mer'),
    ('Tropical garden · parking', 'Jardin tropical · parking'),
    ('12 months construction', '12 mois de construction'),
    ('Private pool · sun terrace', 'Piscine privée · terrasse ensoleillée'),
    ('Open-plan living &amp; dining', 'Séjour et salle à manger ouverts'),
    ('Master suite with dressing room', 'Suite parentale avec dressing'),
    ('4 bedrooms · private pool', '4 chambres · piscine privée'),
    ('Terrace 150 m²', 'Terrasse 150 m²'),
    ('Panoramic balconies · master suite', 'Balcons panoramiques · suite parentale'),
    ('Individual Customisation Available', 'Personnalisation Individuelle Disponible'),
    ('Each residence can be individually tailored to client requirements. We offer the possibility to increase the house area, expand the plot, adapt the floor plan, or refine the design in accordance with your personal vision. All plots are a minimum of 600 m². Please contact us to discuss your requirements.',
     'Chaque résidence peut être adaptée individuellement aux exigences du client. Nous offrons la possibilité d\'augmenter la superficie de la maison, d\'agrandir la parcelle, d\'adapter le plan d\'étage ou de peaufiner le design selon votre vision personnelle. Toutes les parcelles font au minimum 600 m². Veuillez nous contacter pour discuter de vos exigences.'),
    ('Price includes:', 'Le prix comprend :'),
    ('Land plot &amp; freehold title', 'Parcelle de terrain et pleine propriété'),
    ('Full villa construction', 'Construction complète de la villa'),
    ('Interior finishing', 'Finitions intérieures'),
    ('Landscaping &amp; garden', 'Aménagement paysager et jardin'),
    ('Estate infrastructure', 'Infrastructure du domaine'),
    ('Residence application support', 'Assistance pour la demande de résidence'),

    # What's included
    ('Transparency', 'Transparence'),
    ("What's Included &amp; What's Optional", 'Ce qui est inclus et ce qui est optionnel'),
    ('Every Empathia Village villa is delivered turnkey — land, construction, finishing, pool and landscaping are all included in the stated price. The following table clarifies exactly what is and is not part of the base price.',
     'Chaque villa Empathia Village est livrée clé en main — le terrain, la construction, les finitions, la piscine et l\'aménagement paysager sont tous inclus dans le prix indiqué. Le tableau suivant précise exactement ce qui fait ou non partie du prix de base.'),
    ('Included in Price', 'Inclus dans le prix'),
    ('Everything to Move In', 'Tout pour emménager'),
    ('Land plot &amp; freehold title transfer support', 'Parcelle de terrain et assistance au transfert de pleine propriété'),
    ('Full villa construction to completion', 'Construction complète de la villa'),
    ('Premium interior finishing (flooring, walls, ceilings)', 'Finitions intérieures premium (sols, murs, plafonds)'),
    ('Fitted kitchens &amp; bathroom suites', 'Cuisines équipées et salles de bain'),
    ('Private pool &amp; pool terrace', 'Piscine privée et terrasse de piscine'),
    ('Landscaping, tropical garden &amp; driveway', 'Aménagement paysager, jardin tropical et allée'),
    ('Estate roads, security gate &amp; shared infrastructure', 'Routes du domaine, portail de sécurité et infrastructure commune'),
    ('All parking', 'Tout le stationnement'),
    ('Available as Add-On', 'Disponible en option'),
    ('Optional Extras', 'Options supplémentaires'),
    ('Full furniture package (partner studios in Dubai, Europe, Asia)', 'Pack mobilier complet (studios partenaires à Dubaï, Europe, Asie)'),
    ('Home automation &amp; smart-home systems', 'Domotique et systèmes maison connectée'),
    ('Custom design expansion (area, layout, materials)', 'Extension de design personnalisé (superficie, agencement, matériaux)'),
    ('Vehicle import to Mahé (car, SUV, convertible)', 'Importation de véhicule à Mahé (voiture, SUV, cabriolet)'),
    ('Yacht / catamaran charter &amp; purchase assistance', 'Assistance location et achat yacht / catamaran'),
    ('Professional short-term rental management', 'Gestion professionnelle de location courte durée'),
    ('Legal &amp; residency application advisory', 'Conseil juridique et pour la demande de résidence'),
    ('Concierge &amp; property management services', 'Services de conciergerie et de gestion immobilière'),
    ('Furniture packages are available through our partner design studios in Dubai, Europe and Asia upon request. All optional extras are priced and agreed separately from the villa purchase price. Contact us for a full itemised quotation.',
     'Des packs mobilier sont disponibles via nos studios de design partenaires à Dubaï, en Europe et en Asie sur demande. Toutes les options supplémentaires sont tarifées et convenues séparément du prix d\'achat de la villa. Contactez-nous pour un devis détaillé complet.'),

    # Interiors
    ('Interiors', 'Intérieurs'),
    ('Crafted for Exceptional Living', 'Conçu pour une vie d\'exception'),
    ('Each villa is delivered turnkey — premium flooring, fitted kitchens, bathroom finishing and all built-in elements included in price. Full furniture packages available through our partner design studios.',
     'Chaque villa est livrée clé en main — revêtements de sol premium, cuisines équipées, finitions de salle de bain et tous les éléments intégrés inclus dans le prix. Des packs mobilier complets sont disponibles via nos studios de design partenaires.'),
    ('Interior concept visualization', 'Visualisation concept intérieur'),
    ('Full Interior Finish', 'Finition intérieure complète'),
    ('Villa delivered move-in ready. All surfaces, floors and built-in elements included in price.',
     'Villa livrée prête à emménager. Toutes les surfaces, les sols et les éléments intégrés sont inclus dans le prix.'),
    ('Material Selection', 'Sélection de matériaux'),
    ('Natural stone, hardwood, premium tiles and bespoke joinery throughout every residence.',
     'Pierre naturelle, bois massif, carrelage premium et menuiseries sur mesure dans chaque résidence.'),
    ('Furniture Packages', 'Packs mobilier'),
    ('Full furniture packages available through partner design studios upon request.',
     'Packs mobilier complets disponibles via les studios de design partenaires sur demande.'),

    # Lifestyle
    ('Island Lifestyle', 'Art de vivre insulaire'),
    ('Life on Mahé — Beyond the Villa', 'La vie sur Mahé — Au-delà de la villa'),
    ('Owning a villa at Empathia Village opens up a complete Seychelles lifestyle. We assist our owners with everything — from yacht charters and car imports to island experiences and concierge services.',
     'Posséder une villa à Empathia Village ouvre sur un art de vivre complet aux Seychelles. Nous assistons nos propriétaires en tout — des locations de yachts et des importations de voitures aux expériences insulaires et aux services de conciergerie.'),
    ('Giant Tortoises', 'Tortues géantes'),
    ('Aldabra tortoises — icon of the Seychelles', 'Tortues d\'Aldabra — icône des Seychelles'),
    ('Yacht &amp; Catamaran Charter', 'Location de yacht et catamaran'),
    ('Explore the archipelago from your doorstep', 'Explorez l\'archipel depuis votre porte'),
    ('Island Drives', 'Balades en île'),
    ('Cabrio hire &amp; island exploration by car', 'Location de cabriolet et exploration de l\'île en voiture'),
    ('Concierge Service', 'Service de conciergerie'),
    ('Full concierge, transfers and estate services', 'Service de conciergerie complet, transferts et services du domaine'),
    ('Yachts, Boats &amp; Automobiles', 'Yachts, Bateaux et Automobiles'),
    ('We assist our owners with the complete logistics of island living.',
     'Nous assistons nos propriétaires avec la logistique complète de la vie insulaire.'),
    ('From sourcing and importing your vehicle to arranging yacht charters, powerboat purchases and custom car deliveries — our team handles it all.',
     'Du sourcing et de l\'importation de votre véhicule à l\'organisation de locations de yachts, d\'achats de vedettes et de livraisons de voitures sur mesure — notre équipe s\'occupe de tout.'),
    ('Yacht &amp; catamaran charter and purchase assistance', 'Assistance location et achat yacht et catamaran'),
    ('Powerboat, speedboat &amp; motorboat sourcing', 'Sourcing vedette, bateau rapide et hors-bord'),
    ('Vehicle import &amp; customs clearance on Mahé', 'Importation de véhicule et dédouanement à Mahé'),
    ('Luxury convertibles &amp; premium cars delivered to villa', 'Cabriolets de luxe et voitures premium livrés à la villa'),
    ('Enquire About Services', 'Renseignez-vous sur les services'),

    # Investment
    ('Investment', 'Investissement'),
    ('A Rare Opportunity', 'Une Opportunité Rare'),
    ('Restricted Supply', 'Offre limitée'),
    ('Seychelles is one of the world\'s most constrained luxury real estate markets. Oceanfront land is finite — once gone, it cannot be replaced',
     'Les Seychelles sont l\'un des marchés immobiliers de luxe les plus restreints au monde. Les terrains en bord de mer sont finis — une fois partis, ils ne peuvent pas être remplacés'),
    ('Consistent Value Growth', 'Croissance de valeur constante'),
    ('Land values in Seychelles have risen consistently, driven by limited supply and sustained international demand from HNWIs',
     'Les valeurs foncières aux Seychelles ont augmenté de manière constante, portées par une offre limitée et une demande internationale soutenue des HNWI'),
    ('Premium Rental Yield', 'Rendement locatif premium'),
    ('Strong year-round demand for premium villa rental with professional management options',
     'Forte demande toute l\'année pour la location de villa premium avec des options de gestion professionnelle'),
    ('Seychelles Residency', 'Résidence aux Seychelles'),
    ('Residence options may be available to eligible purchasers under Seychelles regulations. Stable, tax-efficient jurisdiction. Details confirmed individually during the transaction process',
     'Des options de résidence peuvent être disponibles pour les acheteurs éligibles en vertu des réglementations des Seychelles. Juridiction stable et fiscalement efficiente. Détails confirmés individuellement lors du processus de transaction'),
    ('Freehold for Foreign Nationals', 'Pleine propriété pour les ressortissants étrangers'),
    ('Foreign buyers may acquire freehold title to both villa and land, subject to applicable approvals. Purchase structure confirmed individually with the developer\'s legal team',
     'Les acheteurs étrangers peuvent acquérir le titre de pleine propriété de la villa et du terrain, sous réserve des approbations applicables. Structure d\'achat confirmée individuellement avec l\'équipe juridique du promoteur'),
    ('Only 35 Plots Available', 'Seulement 35 parcelles disponibles'),
    ('The estate is intentionally limited to 35 residences to preserve privacy, exclusivity and long-term value appreciation for all owners',
     'Le domaine est intentionnellement limité à 35 résidences pour préserver la vie privée, l\'exclusivité et l\'appréciation de la valeur à long terme pour tous les propriétaires'),
    ('The Proposition', 'La Proposition'),
    ('"Your home by the ocean. Your private resort. Your sanctuary in the Indian Ocean."',
     '« Votre maison au bord de l\'océan. Votre resort privé. Votre sanctuaire dans l\'océan Indien. »'),
    ('Project Completion', 'Achèvement du projet'),
    ('Phase I Reserved', 'Phase I réservée'),
    ('Exclusive Plots', 'Parcelles exclusives'),
    ('Entry Price', 'Prix d\'entrée'),

    # Rental potential
    ('Short-Term Rental Income Potential', 'Potentiel de Revenus Locatifs à Court Terme'),
    ('Baie Lazare, adjacent to Four Seasons and Kempinski, is among the most desirable villa rental locations in the Indian Ocean.',
     'Baie Lazare, adjacent au Four Seasons et au Kempinski, est l\'un des endroits les plus prisés pour la location de villas dans l\'océan Indien.'),
    ('Luxury villa rentals in this area command premium nightly rates from international travellers, honeymooners and high-net-worth guests.',
     'Les locations de villas de luxe dans cette zone affichent des tarifs nocturnes premium de la part de voyageurs internationaux, de couples en lune de miel et de clients fortunés.'),
    ('Villa Jane · Indicative', 'Villa Jane · Indicatif'),
    ('Villa Anna · Indicative', 'Villa Anna · Indicatif'),
    ('Villa Georgette · Indicative', 'Villa Georgette · Indicatif'),
    ('per night', 'par nuit'),
    ('2-bedroom private villa · pool · ocean views. Indicative rate based on comparable luxury properties in Baie Lazare.',
     'Villa privée 2 chambres · piscine · vues mer. Tarif indicatif basé sur des propriétés de luxe comparables à Baie Lazare.'),
    ('3-bedroom villa · private pool · panoramic ocean view. Indicative rate based on comparable luxury properties in the region.',
     'Villa 3 chambres · piscine privée · vue panoramique sur l\'océan. Tarif indicatif basé sur des propriétés de luxe comparables dans la région.'),
    ('4-bedroom flagship villa · 150 m² terrace · pool. Flagship residence with highest indicative rental potential.',
     'Villa phare 4 chambres · terrasse 150 m² · piscine. Résidence phare avec le plus haut potentiel locatif indicatif.'),
    ('Year-Round Demand', 'Demande Toute l\'Année'),
    ('Seychelles enjoys consistent demand across all seasons, with peak periods in December–January and July–August.',
     'Les Seychelles bénéficient d\'une demande constante toutes saisons, avec des périodes de pointe en décembre–janvier et juillet–août.'),
    ('Professional Management', 'Gestion Professionnelle'),
    ('Rental management services available through specialist partners — from guest relations to housekeeping and booking platforms.',
     'Services de gestion locative disponibles via des partenaires spécialisés — des relations clients à l\'entretien et aux plateformes de réservation.'),
    ("Owner's Choice", 'Choix du Propriétaire'),
    ('Rental is entirely at the owner\'s discretion. Block out personal stays at any time. No compulsory rental programme.',
     'La location est entièrement à la discrétion du propriétaire. Bloquez des séjours personnels à tout moment. Aucun programme de location obligatoire.'),
    ('<strong style="color:rgba(10,11,10,.65);font-weight:600">Important notice:</strong>',
     '<strong style="color:rgba(10,11,10,.65);font-weight:600">Avis important :</strong>'),
    ('All rental rate figures shown above are indicative only and based on comparable luxury villa properties in the Baie Lazare / Mahé region as of 2026. Actual rental income depends on occupancy rates, management quality, market conditions, seasonality and the owner\'s individual preferences. No guaranteed return on investment is implied, stated or offered. Prospective purchasers should conduct their own due diligence.',
     'Tous les tarifs de location indiqués ci-dessus sont indicatifs uniquement et basés sur des propriétés de villas de luxe comparables dans la région Baie Lazare / Mahé en 2026. Le revenu locatif réel dépend des taux d\'occupation, de la qualité de la gestion, des conditions du marché, de la saisonnalité et des préférences individuelles du propriétaire. Aucun retour sur investissement garanti n\'est implicite, déclaré ou offert. Les acheteurs potentiels doivent effectuer leur propre diligence raisonnable.'),

    # Booking process
    ('How to Buy', 'Comment Acheter'),
    ('The Reservation &amp; Booking Process', 'Le Processus de Réservation'),
    ('Acquiring a villa at Empathia Village is a straightforward, fully supported process. Our team guides you from initial enquiry through to construction handover — in six clear steps.',
     'L\'acquisition d\'une villa à Empathia Village est un processus simple et entièrement accompagné. Notre équipe vous guide de la première demande jusqu\'à la livraison — en six étapes claires.'),
    ('Express Interest', 'Manifester son intérêt'),
    ('Complete the enquiry form or contact us directly via WhatsApp, email or phone. No obligation at this stage.',
     'Remplissez le formulaire de demande ou contactez-nous directement via WhatsApp, e-mail ou téléphone. Aucune obligation à ce stade.'),
    ('Receive Full Presentation', 'Recevoir la présentation complète'),
    ('We send you the complete villa pack within 24 hours — plans, pricing, plot availability, investment overview and agent terms.',
     'Nous vous envoyons le dossier complet dans les 24 heures — plans, tarifs, disponibilité des parcelles, aperçu de l\'investissement et conditions pour les agents.'),
    ('Select Your Plot', 'Choisir votre parcelle'),
    ('Choose your preferred plot number and villa design. Individual customisation options, plot size and orientation discussed at this stage. Plot numbers and availability confirmed on request.',
     'Choisissez votre numéro de parcelle préféré et le design de villa. Les options de personnalisation individuelles, la taille de la parcelle et l\'orientation sont discutées à ce stade. Les numéros de parcelles et la disponibilité sont confirmés sur demande.'),
    ('Letter of Intent (LOI)', 'Lettre d\'Intention (LOI)'),
    ('Sign a Letter of Intent to reserve your chosen plot. A reservation deposit is required to secure the plot. The LOI sets out the key terms of the transaction.',
     'Signez une lettre d\'intention pour réserver votre parcelle choisie. Un dépôt de réservation est requis pour sécuriser la parcelle. La LOI définit les conditions essentielles de la transaction.'),
    ('Staged Payment Plan', 'Plan de Paiement Échelonné'),
    ('A payment schedule aligned with construction milestones is confirmed and agreed. Payments accepted in USD, EUR or GBP. Specific payment stages and percentages are confirmed individually upon request.',
     'Un calendrier de paiement aligné sur les jalons de construction est confirmé et convenu. Paiements acceptés en USD, EUR ou GBP. Les étapes et pourcentages de paiement spécifiques sont confirmés individuellement sur demande.'),
    ('Construction &amp; Handover', 'Construction et Livraison'),
    ('Kensington Construction &amp; Development begins your villa. Estimated build time is approximately 12 months per residence. Regular progress updates provided throughout.',
     'Kensington Construction &amp; Development commence votre villa. Le délai de construction estimé est d\'environ 12 mois par résidence. Des mises à jour régulières sur l\'avancement sont fournies tout au long.'),
    ('Begin Your Enquiry', 'Commencer votre demande'),
    ('WhatsApp Us Now', 'Contactez-nous sur WhatsApp'),

    # Construction
    ('Construction Progress', 'Avancement des travaux'),
    ('Built on Seychelles Soil', 'Construit sur le sol seychellois'),
    ('Every villa at Empathia Village is built directly on Mahé\'s natural terrain — no reclaimed land, no artificial foundations. Granite bedrock, tropical hillside and Indian Ocean views from every construction milestone.',
     'Chaque villa à Empathia Village est construite directement sur le terrain naturel de Mahé — pas de remblai, pas de fondations artificielles. Socle granitique, flanc de colline tropical et vues sur l\'océan Indien depuis chaque étape de la construction.'),
    ('Phase I Active', 'Phase I active'),
    ('Site Preparation', 'Préparation du site'),
    ('Full Completion', 'Livraison complète'),
    ('Site preparation · Mahé hillside', 'Préparation du site · flanc de colline de Mahé'),
    ('Granite terrain · Empathia Village', 'Terrain granitique · Empathia Village'),
    ('Phase I construction · Empathia Village', 'Construction Phase I · Empathia Village'),
    ('Construction progress · June 2026', 'Avancement des travaux · juin 2026'),
    ('months per villa', 'mois par villa'),
    ('natural terrain', 'terrain naturel'),
    ('design &amp; build', 'conception et construction'),
    ('license holder', 'titulaire de licence'),

    # News
    ('Latest', 'Actualités'),
    ('Project Updates', 'Mises à jour du projet'),
    ('Phase I: 25% of residences reserved — construction underway',
     'Phase I : 25 % des résidences réservées — construction en cours'),
    ('Phase I is now 25% reserved. Construction of the first residences at Empathia Village is actively underway on the Mahé hillside.',
     'La Phase I est maintenant réservée à 25 %. La construction des premières résidences à Empathia Village est activement en cours sur le flanc de colline de Mahé.'),
    ('Phase II plots now available', 'Parcelles de Phase II maintenant disponibles'),
    ('Second phase plots are open for reservation. Villa Anna, Jane and Georgette designs available on plots from 600 to 2,000 m².',
     'Les parcelles de la deuxième phase sont ouvertes à la réservation. Designs Villa Anna, Jane et Georgette disponibles sur des parcelles de 600 à 2 000 m².'),

    # Gallery
    ('Photography &amp; Film', 'Photographie et Film'),

    # Agents
    ('Partner Programme', 'Programme Partenaire'),
    ('For Agents<br>&amp; Partners', 'Pour les Agents<br>et Partenaires'),
    ('Empathia Village offers a premium product for international real estate agents, brokers and investment advisors. We welcome both direct agent registrations and co-brokerage arrangements with established firms worldwide.',
     'Empathia Village offre un produit premium pour les agents immobiliers internationaux, courtiers et conseillers en investissement. Nous accueillons les inscriptions directes d\'agents et les arrangements de co-courtage avec des entreprises établies dans le monde entier.'),
    ('Commission from 3% of transaction value (minimum $24,000 per villa)',
     'Commission dès 3 % de la valeur de la transaction (minimum $24 000 par villa)'),
    ('Full branded sales kit — presentations, villa sheets, floor plans',
     'Kit de vente complet avec marque — présentations, fiches villa, plans'),
    ('Current price lists and plot availability maps', 'Listes de prix actuelles et cartes de disponibilité des parcelles'),
    ('Co-brokerage and referral arrangements welcome', 'Co-courtage et arrangements de référence bienvenus'),
    ('Dedicated support throughout the client\'s purchase journey',
     'Soutien dédié tout au long du parcours d\'achat du client'),
    ('Private site visits and client consultation assistance', 'Visites privées du site et assistance à la consultation clients'),
    ('No exclusivity required — open to global agents', 'Aucune exclusivité requise — ouvert aux agents mondiaux'),
    ('How to Register', 'Comment s\'inscrire'),
    ('Contact us by email or WhatsApp, introduce yourself and your agency, and we will send you the full Agent Pack within 24 hours. No formal registration or exclusivity required to begin.',
     'Contactez-nous par e-mail ou WhatsApp, présentez-vous et votre agence, et nous vous enverrons le dossier Agent complet dans les 24 heures. Aucune inscription formelle ou exclusivité requise pour commencer.'),
    ('Agent Commission', 'Commission Agent'),
    ('of transaction value', 'de la valeur de la transaction'),
    ('Minimum fee per transaction', 'Frais minimum par transaction'),
    ('Starting villa price from $990,000', 'Prix de départ villa dès $990 000'),
    ('What You Receive', 'Ce que vous recevez'),
    ('Full villa presentation deck (PDF &amp; print-ready)', 'Dossier de présentation villa complet (PDF et prêt à imprimer)'),
    ('Floor plans &amp; architectural renders per villa', 'Plans et rendus architecturaux par villa'),
    ('Current pricing &amp; plot availability (confidential)', 'Tarification actuelle et disponibilité des parcelles (confidentiel)'),
    ('Investment overview &amp; location factsheet', 'Aperçu de l\'investissement et fiche localisation'),
    ('Direct developer contact for client Q&amp;A', 'Contact direct avec le promoteur pour les Q&amp;R clients'),
    ('Request Agent Pack', 'Demander le dossier Agent'),
    ('View Full Agent Programme', 'Voir le programme Agent complet'),

    # VS Eden Island
    ('Choosing Your Seychelles Address', 'Choisir votre adresse aux Seychelles'),
    ('Two premium addresses in Seychelles — each suited to a different lifestyle and vision. Understanding the difference helps buyers make the right choice.',
     'Deux adresses premium aux Seychelles — chacune adaptée à un mode de vie et une vision différents. Comprendre la différence aide les acheteurs à faire le bon choix.'),
    ('Natural hillside living.<br>Privacy. Ocean views.', 'Vie sur la colline naturelle.<br>Intimité. Vues mer.'),
    ('Natural hillside terrain — no reclaimed land', 'Terrain naturel de colline — pas de remblai'),
    ('Private villa plots from 600 m²', 'Parcelles de villa privées dès 600 m²'),
    ('Unobstructed Indian Ocean views', 'Vues dégagées sur l\'océan Indien'),
    ('Immersive tropical landscape', 'Paysage tropical immersif'),
    ('Gated residential community · 35 plots', 'Communauté résidentielle fermée · 35 parcelles'),
    ('Individual design customisation available', 'Personnalisation individuelle du design disponible'),
    ('Quiet, private south Mahé setting', 'Cadre calme et privé au sud de Mahé'),
    ('Enquire About Empathia Village', 'Renseignez-vous sur Empathia Village'),
    ('Marina lifestyle.<br>Urban resort atmosphere.', 'Art de vivre marina.<br>Atmosphère de resort urbain.'),
    ('Marina and waterfront setting', 'Cadre marina et bord de mer'),
    ('Apartment and townhouse format', 'Format appartement et maison de ville'),
    ('Reclaimed island setting', 'Cadre insulaire sur remblai'),
    ('Closer to Victoria and city infrastructure', 'Plus proche de Victoria et de l\'infrastructure urbaine'),
    ('More urban and resort-style atmosphere', 'Atmosphère plus urbaine et de type resort'),
    ('Eden Island is a well-established destination for buyers seeking a marina-facing apartment or townhouse lifestyle closer to Victoria.',
     'Eden Island est une destination bien établie pour les acheteurs recherchant un appartement ou une maison de ville face à la marina, plus proche de Victoria.'),
    ('Empathia Village is designed for buyers seeking privacy, nature, larger private plots and a quieter villa lifestyle — in one of Mahé\'s most prestigious coastal addresses, between Four Seasons and Kempinski.',
     'Empathia Village est conçu pour les acheteurs recherchant la vie privée, la nature, de plus grandes parcelles privées et un style de vie villa plus calme — dans l\'une des adresses côtières les plus prestigieuses de Mahé, entre Four Seasons et Kempinski.'),

    # FAQ
    ('Frequently Asked Questions', 'Questions Fréquemment Posées'),
    ('Can foreign nationals purchase property at Empathia Village?',
     'Les ressortissants étrangers peuvent-ils acheter un bien à Empathia Village ?'),
    ('Yes. Foreign buyers may acquire freehold title to both the villa and the land on which it stands, subject to applicable approvals and transaction procedures. The purchase process is fully supported by our legal team.',
     'Oui. Les acheteurs étrangers peuvent acquérir le titre de pleine propriété de la villa et du terrain sur lequel elle se trouve, sous réserve des approbations applicables et des procédures de transaction. Le processus d\'achat est entièrement soutenu par notre équipe juridique.'),
    ('What currencies are payments accepted in?',
     'Dans quelles devises les paiements sont-ils acceptés ?'),
    ('Payments are accepted in USD, EUR or GBP. Payments may be made in the Seychelles jurisdiction or internationally. A staged payment plan aligned to construction milestones is available on request.',
     'Les paiements sont acceptés en USD, EUR ou GBP. Les paiements peuvent être effectués dans la juridiction des Seychelles ou à l\'international. Un plan de paiement échelonné aligné sur les jalons de construction est disponible sur demande.'),
    ('How long does construction take?',
     'Combien de temps dure la construction ?'),
    ('Each villa takes approximately 12 months to construct from groundbreaking. The full estate is planned for completion within 3 years. Phase I represents 25% of total plots and is currently under active construction.',
     'Chaque villa prend environ 12 mois à construire depuis le début des travaux. La totalité du domaine est prévue pour être achevée dans un délai de 3 ans. La Phase I représente 25 % du total des parcelles et est actuellement en construction active.'),
    ('Do I qualify for Seychelles residency?',
     'Est-ce que je suis éligible à la résidence aux Seychelles ?'),
    ('Residence options may be available to eligible purchasers under Seychelles regulations. Eligibility and applicable requirements are confirmed individually with the legal team during the transaction process. We recommend consulting with a qualified Seychelles legal advisor for precise details.',
     'Des options de résidence peuvent être disponibles pour les acheteurs éligibles en vertu des réglementations des Seychelles. L\'éligibilité et les conditions applicables sont confirmées individuellement avec l\'équipe juridique lors du processus de transaction. Nous recommandons de consulter un conseiller juridique qualifié aux Seychelles pour des détails précis.'),
    ('Can I rent my villa when I\'m not using it?',
     'Puis-je louer ma villa lorsque je ne l\'utilise pas ?'),
    ('Yes. Owners may rent their villa on short or long-term terms. Professional villa management services are available, allowing owners to benefit from hotel-quality rental management.',
     'Oui. Les propriétaires peuvent louer leur villa à court ou long terme. Des services professionnels de gestion de villa sont disponibles, permettant aux propriétaires de bénéficier d\'une gestion locative de qualité hôtelière.'),
    ('Is an inspection visit possible before purchase?',
     'Une visite d\'inspection est-elle possible avant l\'achat ?'),
    ('Absolutely. We offer a private one-week discovery tour to the Seychelles with accommodation on Eden Island. Our team arranges all logistics, site visits and meetings. Contact us to plan your visit.',
     'Absolument. Nous proposons une visite de découverte privée d\'une semaine aux Seychelles avec hébergement sur Eden Island. Notre équipe organise toute la logistique, les visites de site et les réunions. Contactez-nous pour planifier votre visite.'),
    ('What exactly is included in the villa price?',
     'Qu\'est-ce qui est exactement inclus dans le prix de la villa ?'),
    ('The stated price includes: the land plot and freehold title transfer support, full villa construction, premium interior finishing (floors, walls, ceilings), fitted kitchen and bathroom suites, private pool and pool terrace, landscaping and tropical garden, driveway and parking, and connection to estate infrastructure (roads, gate, utilities). Furniture and moveable items are not included but are available as an optional package.',
     'Le prix indiqué comprend : la parcelle et l\'assistance au transfert de pleine propriété, la construction complète de la villa, les finitions intérieures premium (sols, murs, plafonds), la cuisine équipée et les salles de bain, la piscine privée et la terrasse de piscine, l\'aménagement paysager et le jardin tropical, l\'allée et le parking, et le raccordement à l\'infrastructure du domaine (routes, portail, services). Le mobilier et les articles mobiles ne sont pas inclus mais sont disponibles en option.'),
    ('Are furniture packages available?',
     'Des packs mobilier sont-ils disponibles ?'),
    ('Yes. Full furniture packages are available as an optional add-on through our partner design studios, sourcing from Dubai, Europe and Asia. Packages are priced separately and tailored to your villa size and design preferences. Contact us to discuss options after plot selection.',
     'Oui. Des packs mobilier complets sont disponibles en option via nos studios de design partenaires, en s\'approvisionnant à Dubaï, en Europe et en Asie. Les packs sont tarifés séparément et adaptés à la taille de votre villa et à vos préférences de design. Contactez-nous pour discuter des options après la sélection de la parcelle.'),
    ('What is the short-term rental potential?',
     'Quel est le potentiel de location courte durée ?'),
    ('Baie Lazare, adjacent to Four Seasons and Kempinski, is among the most desirable villa rental locations in the Indian Ocean. Indicative nightly rates for comparable luxury villas in this area range from approximately $2,000 to $5,000+ per night depending on villa size and season. These figures are indicative only — based on comparable properties in the region — and do not constitute a guaranteed return. Actual rental income depends on occupancy, management quality, market conditions and the owner\'s own decisions. No guaranteed rental income is offered.',
     'Baie Lazare, adjacent au Four Seasons et au Kempinski, est l\'un des endroits les plus prisés pour la location de villas dans l\'océan Indien. Les tarifs nocturnes indicatifs pour des villas de luxe comparables dans cette zone varient d\'environ $2 000 à $5 000+ par nuit selon la taille de la villa et la saison. Ces chiffres sont indicatifs uniquement — basés sur des propriétés comparables dans la région — et ne constituent pas un retour garanti. Le revenu locatif réel dépend de l\'occupation, de la qualité de la gestion, des conditions du marché et des propres décisions du propriétaire. Aucun revenu locatif garanti n\'est offert.'),
    ('What is the payment plan?',
     'Quel est le plan de paiement ?'),
    ('Payments are staged in line with construction milestones — typically reservation, foundation, structure, finishing and handover. The exact payment percentages and schedule are confirmed individually upon request. Payments are accepted in USD, EUR or GBP. No specific payment percentages are published publicly — contact us to receive the current payment plan for your chosen villa.',
     'Les paiements sont échelonnés selon les jalons de construction — généralement réservation, fondation, structure, finitions et livraison. Les pourcentages et le calendrier de paiement exacts sont confirmés individuellement sur demande. Les paiements sont acceptés en USD, EUR ou GBP. Aucun pourcentage de paiement spécifique n\'est publié publiquement — contactez-nous pour recevoir le plan de paiement actuel pour votre villa choisie.'),
    ('Can I see available plot numbers and a plot map?',
     'Puis-je voir les numéros de parcelles disponibles et un plan des parcelles ?'),
    ('Yes. The estate has 35 numbered plots. A detailed plot map with plot numbers, areas, orientations and current availability status is included in our full presentation pack, sent to qualified buyers upon request. Plot availability changes as reservations are made, so we recommend requesting current status directly.',
     'Oui. Le domaine dispose de 35 parcelles numérotées. Un plan de parcelles détaillé avec les numéros de parcelles, les superficies, les orientations et le statut de disponibilité actuel est inclus dans notre dossier de présentation complet, envoyé aux acheteurs qualifiés sur demande. La disponibilité des parcelles évolue au fur et à mesure que les réservations sont effectuées, nous recommandons donc de demander le statut actuel directement.'),
    ('Can I customise the villa design?',
     'Puis-je personnaliser le design de la villa ?'),
    ('Yes. Each villa design can be adapted to individual requirements — including floor plan changes, area expansion, material selections, additional rooms or bespoke architectural features. Villa Georgette, for example, can be extended up to 450 m². Customisation options and associated costs are discussed individually during the sales process. Contact us to discuss your vision.',
     'Oui. Chaque design de villa peut être adapté aux exigences individuelles — y compris les modifications de plan, l\'agrandissement de superficie, la sélection de matériaux, les pièces supplémentaires ou les caractéristiques architecturales sur mesure. La Villa Georgette, par exemple, peut être agrandie jusqu\'à 450 m². Les options de personnalisation et les coûts associés sont discutés individuellement lors du processus de vente. Contactez-nous pour discuter de votre vision.'),
    ('Do you offer citizenship by investment or a passport programme?',
     'Proposez-vous la citoyenneté par investissement ou un programme de passeport ?'),
    ('No. Empathia Village does not offer, imply or guarantee citizenship, a passport or any immigration status. Residence options (not citizenship) may be available to eligible purchasers under Seychelles regulations, subject to individual eligibility review and applicable procedures. We strongly recommend consulting with a qualified Seychelles immigration lawyer for precise and current advice on residency requirements.',
     'Non. Empathia Village n\'offre pas, n\'implique pas et ne garantit pas la citoyenneté, un passeport ou tout statut d\'immigration. Des options de résidence (pas la citoyenneté) peuvent être disponibles pour les acheteurs éligibles en vertu des réglementations des Seychelles, sous réserve d\'un examen d\'éligibilité individuel et des procédures applicables. Nous recommandons vivement de consulter un avocat qualifié en droit de l\'immigration aux Seychelles pour des conseils précis et actuels sur les exigences de résidence.'),
    ('I am a real estate agent — how do I register?',
     'Je suis agent immobilier — comment m\'inscrire ?'),
    ('Simply contact us by email at info@empathia-seychelles.com or via WhatsApp +248 271 51 02 to introduce yourself and your agency. We will send you the full Agent Pack — including villa presentations, floor plans, pricing and commission terms — within 24 hours. No formal registration or exclusivity agreement is required to begin. Commission starts from 3% of transaction value, with a minimum of $24,000 per villa transaction.',
     'Contactez-nous simplement par e-mail à info@empathia-seychelles.com ou via WhatsApp +248 271 51 02 pour vous présenter ainsi que votre agence. Nous vous enverrons le dossier Agent complet — incluant les présentations de villas, plans, tarifs et conditions de commission — dans les 24 heures. Aucune inscription formelle ou accord d\'exclusivité n\'est requis pour commencer. La commission commence à 3 % de la valeur de la transaction, avec un minimum de $24 000 par transaction de villa.'),

    # Presentation form
    ('Detailed Documentation', 'Documentation Détaillée'),
    ('Download Full<br>Presentation', 'Télécharger la Présentation<br>Complète'),
    ('Receive villa plans, pricing, location details and partnership terms. Our full presentation pack is sent directly to qualified buyers, investors and agents.',
     'Recevez les plans de villas, les tarifs, les détails de localisation et les conditions de partenariat. Notre dossier de présentation complet est envoyé directement aux acheteurs, investisseurs et agents qualifiés.'),
    ('Villa floor plans &amp; architectural drawings', 'Plans de villas et dessins architecturaux'),
    ('Pricing &amp; plot availability', 'Tarification et disponibilité des parcelles'),
    ('Location &amp; masterplan documentation', 'Documentation de localisation et plan d\'ensemble'),
    ('Investment overview', 'Aperçu de l\'investissement'),
    ('Agent partnership terms', 'Conditions de partenariat agent'),
    ('Request Presentation', 'Demander la présentation'),
    ('Name', 'Nom'),
    ('Email', 'E-mail'),
    ('>I am a… Buyer / Investor / Agent / Partner<', '>Je suis… Acheteur / Investisseur / Agent / Partenaire<'),
    ('>Buyer<', '>Acheteur<'),
    ('>Investor<', '>Investisseur<'),
    ('>Agent<', '>Agent<'),
    ('>Partner<', '>Partenaire<'),

    # Contact / form
    ('Private Consultation', 'Consultation Privée'),
    ('Request a Private Consultation', 'Demander une Consultation Privée'),
    ('Get the full presentation, villa price list and availability. Our team responds within 24 hours.',
     'Obtenez la présentation complète, la liste de prix des villas et la disponibilité. Notre équipe répond dans les 24 heures.'),
    ('Your name', 'Votre nom'),
    ('Email address', 'Adresse e-mail'),
    ('WhatsApp / Phone', 'WhatsApp / Téléphone'),
    ('>I am a…<', '>Je suis…<'),
    ('Send Request', 'Envoyer la demande'),
    ('Contact via WhatsApp', 'Contacter par WhatsApp'),

    # Cinematic 2
    ('Where the Indian Ocean<br>Becomes Your Garden', 'Là où l\'Océan Indien<br>devient votre jardin'),
    ('Baie Lazare. White sand. Granite boulders. Turquoise water. Two of the world\'s finest resort hotels as your neighbours.',
     'Baie Lazare. Sable blanc. Rochers de granit. Eau turquoise. Deux des plus beaux hôtels-resorts du monde comme voisins.'),
    ('Reserve Your Residence', 'Réserver votre résidence'),

    # Footer
    ('Kensington Construction &amp; Development · Class 1 License · Seychelles',
     'Kensington Construction &amp; Development · Licence Classe 1 · Seychelles'),
    ('© 2026 All rights reserved · Private Living · Naturally Yours',
     '© 2026 Tous droits réservés · Vie Privée · Naturellement Vôtre'),
    ('Prices, floor plans, areas, images, purchase terms and any other information presented on this website are provided for general information purposes only and do not constitute a public offer. Current pricing, availability, specifications, payment terms and transaction procedure are confirmed individually upon request.',
     'Les prix, plans, superficies, images, conditions d\'achat et toute autre information présentés sur ce site sont fournis à titre d\'information générale uniquement et ne constituent pas une offre publique. Les tarifs actuels, la disponibilité, les spécifications, les conditions de paiement et la procédure de transaction sont confirmés individuellement sur demande.'),

    # JS alerts
    ("'Please enter your name or contact details.'",
     "'Veuillez entrer votre nom ou vos coordonnées.'"),
    ("'Sending…'", "'Envoi en cours…'"),
    ("btn.textContent = 'Send Request'", "btn.textContent = 'Envoyer la demande'"),
    ("btn.textContent = 'Request Presentation'", "btn.textContent = 'Demander la présentation'"),
    ("'Thank you' + (n ? ', '+n : '') + '.\\n\\nA member of our team will be in touch within 24 hours.\\n\\nEmpathia Village · Kensington Construction & Development'",
     "'Merci' + (n ? ', '+n : '') + '.\\n\\nUn membre de notre équipe vous contactera dans les 24 heures.\\n\\nEmpathia Village · Kensington Construction & Development'"),
    ("'Sorry, the form could not be sent right now.\\n\\nPlease contact us directly:\\nWhatsApp +248 271 51 02\\ninfo@empathia-seychelles.com'",
     "'Désolé, le formulaire n\\'a pas pu être envoyé.\\n\\nContactez-nous directement :\\nWhatsApp +248 271 51 02\\ninfo@empathia-seychelles.com'"),
    ("'Thank you' + (n ? ', ' + n : '') + '.\\n\\nWe will send you the full presentation shortly.\\n\\nEmpathia Village · Kensington Construction & Development'",
     "'Merci' + (n ? ', ' + n : '') + '.\\n\\nNous vous enverrons la présentation complète sous peu.\\n\\nEmpathia Village · Kensington Construction & Development'"),
    ("'Please enter your name or contact details.'",
     "'Veuillez entrer votre nom ou vos coordonnées.'"),
]

# ──────────────────────────────────────────────────────────
# ARABIC TRANSLATIONS
# ──────────────────────────────────────────────────────────
AR = [
    ('Private Living · Naturally Yours', 'معيشة خاصة · طبيعية بامتياز'),
    ('Home', 'الرئيسية'),
    ('Residencies', 'المساكن'),
    ('Pricing', 'الأسعار'),
    ('Gallery', 'المعرض'),
    ('Construction', 'البناء'),
    ('Agents', 'الوكلاء'),
    ('Contacts', 'اتصل بنا'),
    ('Private Enquiry', 'استفسار خاص'),

    # Hero
    ('Private Luxury Villas<br>in Seychelles', 'فلل فاخرة خاصة<br>في جزر سيشيل'),
    ('Freehold Title · Staged Payments · Between Four Seasons &amp; Kempinski',
     'ملكية حرة · دفعات متدرجة · بين Four Seasons و Kempinski'),
    ('35 Private Plots', '35 قطعة خاصة'),
    ('From $990,000', 'تبدأ من $990,000'),
    ('12 Months Build', 'البناء 12 شهراً'),
    ('Rental Potential', 'إمكانية الإيجار'),
    ('Request Full Presentation', 'طلب العرض الكامل'),
    ('View Residences', 'استعراض المساكن'),
    ('Scroll', 'تمرير'),

    # Stats
    ('Private Plots', 'قطع خاصة'),
    ('Starting Price', 'السعر الابتدائي'),
    ('To Beach', 'إلى الشاطئ'),
    ('Developer Experience', 'خبرة المطور'),
    ('Homes Delivered', 'منازل مُسلَّمة'),

    # About
    ('The Estate', 'المجمع'),
    ('A new standard<br>of private luxury living', 'معيار جديد<br>في المعيشة الفاخرة الخاصة'),
    ('"Empathy is what restores a lost paradise"', '«التعاطف هو ما يُعيد الفردوس المفقود»'),
    ('Built on Trust · Designed for Life · Class 1 License', 'مبني على الثقة · مصمم للحياة · رخصة الفئة الأولى'),

    # Features
    ('Freehold Title', 'ملكية حرة'),
    ('Staged Payments', 'دفعات متدرجة'),
    ('Residency', 'الإقامة'),
    ('Rental Potential', 'إمكانية الإيجار'),
    ('Indicative short-term rental rates from $2,000/night for comparable luxury villas in Baie Lazare. Professional management available. Subject to market conditions — no guaranteed income.',
     'معدلات إيجار قصير الأمد مؤشرية من $2,000/ليلة للفلل الفاخرة المماثلة في Baie Lazare. إدارة احترافية متاحة. يخضع لظروف السوق — لا دخل مضمون.'),

    # Cinematic
    ('The Setting', 'البيئة'),
    ('Between<br>Four Seasons<br>&amp; Kempinski', 'بين<br>Four Seasons<br>و Kempinski'),
    ('Arrange a Private Visit', 'ترتيب زيارة خاصة'),

    # Location
    ('Location', 'الموقع'),
    ('The Finest Address<br>in Seychelles', 'أرقى عنوان<br>في جزر سيشيل'),
    ('Find Us', 'موقعنا'),
    ('Project Location', 'موقع المشروع'),
    ('Open in Google Maps', 'فتح في خرائط Google'),

    # Masterplan
    ('Masterplan', 'المخطط العام'),
    ('35 Private Plots<br>in Natural Terrain', '35 قطعة خاصة<br>في تضاريس طبيعية'),
    ('Total Plots', 'إجمالي القطع'),
    ('m² per Plot', 'م² لكل قطعة'),
    ('Phase I Reserved', 'المرحلة الأولى محجوزة'),
    ('Full Completion', 'الاكتمال الكامل'),
    ('Estate Masterplan · 2026', 'المخطط العام للمجمع · 2026'),
    ('Request plot map →', 'طلب خريطة القطع →'),

    # Why Seychelles
    ('Investment Destination', 'وجهة استثمارية'),
    ('Why Seychelles?', 'لماذا سيشيل؟'),
    ('Land Supply', 'المعروض من الأراضي'),
    ('Jurisdiction', 'الولاية القضائية'),
    ('Global', 'عالمي'),
    ('Demand', 'الطلب'),
    ('Freehold', 'ملكية حرة'),
    ('Ownership', 'التملك'),
    ('Premium', 'متميز'),
    ('Island', 'جزيرة'),
    ('Lifestyle', 'أسلوب الحياة'),

    # Villas
    ('The Collection', 'المجموعة'),
    ('Three Villa Designs', 'ثلاثة تصاميم للفيلا'),
    ('All Residences', 'جميع المساكن'),
    ('Entry-level private villa', 'فيلا خاصة بسعر تنافسي'),
    ('Elegant ocean-view villa', 'فيلا أنيقة بإطلالة بحرية'),
    ('Flagship residence', 'المسكن الرئيسي'),
    ('View Details', 'عرض التفاصيل'),
    ('Request Price List', 'طلب قائمة الأسعار'),
    ('Get Villa Price List', 'الحصول على قائمة أسعار الفيلا'),
    ('Residence', 'مسكن'),
    ('Signature Residence', 'المسكن المميز'),
    ('m² Area', 'م² المساحة'),
    ('m² Terrace', 'م² التراس'),
    ('m² Pool', 'م² المسبح'),
    ('m² Plot', 'م² القطعة'),
    ('Architectural Project', 'المشروع المعماري'),

    # Pricing
    ('Pricing', 'الأسعار'),
    ('Villa Pricing', 'أسعار الفيلا'),
    ('Price includes:', 'السعر يشمل:'),
    ('Land plot &amp; freehold title', 'قطعة الأرض وسند الملكية الحرة'),
    ('Full villa construction', 'بناء الفيلا الكامل'),
    ('Interior finishing', 'التشطيبات الداخلية'),
    ('Landscaping &amp; garden', 'التنسيق الخارجي والحديقة'),
    ('Estate infrastructure', 'البنية التحتية للمجمع'),
    ('Residence application support', 'دعم طلب الإقامة'),
    ('Individual Customisation Available', 'التخصيص الفردي متاح'),
    ('from 140 m² · 2 Bedrooms', 'من 140 م² · غرفتا نوم'),
    ('from 240 m² · 3 Bedrooms', 'من 240 م² · 3 غرف نوم'),
    ('from 350 m² · 4 Bedrooms', 'من 350 م² · 4 غرف نوم'),
    ('Plot from 600 m² · Not a public offer', 'قطعة من 600 م² · ليست عرضاً عاماً'),
    ('Plot from 1,500 m² · Not a public offer', 'قطعة من 1,500 م² · ليست عرضاً عاماً'),
    ('12 months construction', 'بناء 12 شهراً'),

    # What's included
    ('Transparency', 'الشفافية'),
    ("What's Included &amp; What's Optional", 'ما هو مشمول وما هو اختياري'),
    ('Included in Price', 'مشمول في السعر'),
    ('Everything to Move In', 'كل ما تحتاجه للانتقال'),
    ('Available as Add-On', 'متاح كإضافة'),
    ('Optional Extras', 'إضافات اختيارية'),

    # Interiors
    ('Interiors', 'الديكورات الداخلية'),
    ('Crafted for Exceptional Living', 'مُصمَّم لحياة استثنائية'),
    ('Full Interior Finish', 'تشطيب داخلي كامل'),
    ('Material Selection', 'اختيار المواد'),
    ('Furniture Packages', 'حزم الأثاث'),
    ('Interior concept visualization', 'تصور مفهوم الديكور الداخلي'),

    # Lifestyle
    ('Island Lifestyle', 'أسلوب حياة الجزيرة'),
    ('Life on Mahé — Beyond the Villa', 'الحياة في Mahé — خارج الفيلا'),
    ('Giant Tortoises', 'السلاحف العملاقة'),
    ('Aldabra tortoises — icon of the Seychelles', 'سلاحف ألدابرا — رمز سيشيل'),
    ('Yacht &amp; Catamaran Charter', 'استئجار اليخوت والكتاماران'),
    ('Explore the archipelago from your doorstep', 'استكشف الأرخبيل من باب منزلك'),
    ('Island Drives', 'جولات الجزيرة'),
    ('Concierge Service', 'خدمة الكونسيرج'),
    ('Yachts, Boats &amp; Automobiles', 'اليخوت والقوارب والسيارات'),
    ('Enquire About Services', 'الاستفسار عن الخدمات'),

    # Investment
    ('Investment', 'الاستثمار'),
    ('A Rare Opportunity', 'فرصة نادرة'),
    ('Restricted Supply', 'عرض محدود'),
    ('Consistent Value Growth', 'نمو ثابت في القيمة'),
    ('Premium Rental Yield', 'عائد إيجاري متميز'),
    ('Seychelles Residency', 'إقامة سيشيل'),
    ('Freehold for Foreign Nationals', 'ملكية حرة للمواطنين الأجانب'),
    ('Only 35 Plots Available', '35 قطعة فقط متاحة'),
    ('The Proposition', 'العرض'),
    ('Project Completion', 'اكتمال المشروع'),
    ('Exclusive Plots', 'قطع حصرية'),
    ('Entry Price', 'سعر الدخول'),

    # Rental
    ('Short-Term Rental Income Potential', 'إمكانية دخل الإيجار قصير الأمد'),
    ('per night', 'في الليلة'),
    ('Year-Round Demand', 'طلب على مدار العام'),
    ('Professional Management', 'إدارة احترافية'),
    ("Owner's Choice", 'اختيار المالك'),
    ('<strong style="color:rgba(10,11,10,.65);font-weight:600">Important notice:</strong>',
     '<strong style="color:rgba(10,11,10,.65);font-weight:600">ملاحظة مهمة:</strong>'),

    # Booking
    ('How to Buy', 'كيفية الشراء'),
    ('The Reservation &amp; Booking Process', 'عملية الحجز والاستفسار'),
    ('Express Interest', 'التعبير عن الاهتمام'),
    ('Receive Full Presentation', 'استلام العرض الكامل'),
    ('Select Your Plot', 'اختيار قطعتك'),
    ('Letter of Intent (LOI)', 'خطاب النية (LOI)'),
    ('Staged Payment Plan', 'خطة الدفع المتدرجة'),
    ('Construction &amp; Handover', 'البناء والتسليم'),
    ('Begin Your Enquiry', 'ابدأ استفساركم'),
    ('WhatsApp Us Now', 'تواصل معنا عبر واتساب'),

    # Construction
    ('Construction Progress', 'تقدم البناء'),
    ('Built on Seychelles Soil', 'مبني على أرض سيشيل'),
    ('Phase I Active', 'المرحلة الأولى نشطة'),
    ('Site Preparation', 'تجهيز الموقع'),
    ('months per villa', 'أشهر لكل فيلا'),
    ('natural terrain', 'تضاريس طبيعية'),
    ('design &amp; build', 'التصميم والبناء'),
    ('license holder', 'حامل الرخصة'),

    # News
    ('Latest', 'آخر الأخبار'),
    ('Project Updates', 'تحديثات المشروع'),

    # Gallery
    ('Photography &amp; Film', 'الصور والأفلام'),

    # Agents
    ('Partner Programme', 'برنامج الشراكة'),
    ('For Agents<br>&amp; Partners', 'للوكلاء<br>والشركاء'),
    ('How to Register', 'كيفية التسجيل'),
    ('Agent Commission', 'عمولة الوكيل'),
    ('of transaction value', 'من قيمة الصفقة'),
    ('Minimum fee per transaction', 'الحد الأدنى للرسوم لكل صفقة'),
    ('Starting villa price from $990,000', 'سعر الفيلا يبدأ من $990,000'),
    ('What You Receive', 'ما ستحصل عليه'),
    ('Request Agent Pack', 'طلب حقيبة الوكيل'),
    ('View Full Agent Programme', 'عرض برنامج الوكيل الكامل'),

    # VS Eden
    ('Choosing Your Seychelles Address', 'اختيار عنوانك في سيشيل'),
    ('Enquire About Empathia Village', 'الاستفسار عن Empathia Village'),

    # FAQ
    ('Frequently Asked Questions', 'الأسئلة الشائعة'),

    # Presentation
    ('Detailed Documentation', 'توثيق تفصيلي'),
    ('Download Full<br>Presentation', 'تحميل العرض<br>الكامل'),
    ('Request Presentation', 'طلب العرض'),
    ('Name', 'الاسم'),
    ('Email', 'البريد الإلكتروني'),
    ('>I am a… Buyer / Investor / Agent / Partner<', '>أنا... مشترٍ / مستثمر / وكيل / شريك<'),
    ('>Buyer<', '>مشترٍ<'),
    ('>Investor<', '>مستثمر<'),
    ('>Agent<', '>وكيل<'),
    ('>Partner<', '>شريك<'),

    # Contact
    ('Private Consultation', 'استشارة خاصة'),
    ('Request a Private Consultation', 'طلب استشارة خاصة'),
    ('Your name', 'اسمك'),
    ('Email address', 'عنوان البريد الإلكتروني'),
    ('WhatsApp / Phone', 'واتساب / الهاتف'),
    ('>I am a…<', '>أنا...<'),
    ('Send Request', 'إرسال الطلب'),
    ('Contact via WhatsApp', 'التواصل عبر واتساب'),

    # Cinematic 2
    ('Where the Indian Ocean<br>Becomes Your Garden', 'حيث يصبح المحيط الهندي<br>حديقتك الخاصة'),
    ('Reserve Your Residence', 'احجز مسكنك'),

    # Footer
    ('© 2026 All rights reserved · Private Living · Naturally Yours',
     '© 2026 جميع الحقوق محفوظة · معيشة خاصة · طبيعية بامتياز'),
    ('SEYCHELLES · MAHÉ', 'سيشيل · ماهيه'),

    # JS
    ("'Please enter your name or contact details.'",
     "'يرجى إدخال اسمك أو بيانات الاتصال.'"),
    ("'Sending…'", "'جارٍ الإرسال...'"),
    ("btn.textContent = 'Send Request'", "btn.textContent = 'إرسال الطلب'"),
    ("btn.textContent = 'Request Presentation'", "btn.textContent = 'طلب العرض'"),
]

def apply_translations(html, pairs):
    for old, new in pairs:
        html = html.replace(old, new)
    return html

# ──────────────────────────────────────────────────────────
# ADD LANGUAGE SWITCHER  (insert before <div class="nav-actions">)
# ──────────────────────────────────────────────────────────
LANG_SWITCHER_EN = '''<div style="display:flex;gap:8px;align-items:center;font-size:9px;letter-spacing:.12em;margin-right:16px">
      <a href="/" style="color:var(--gold);text-decoration:none;font-weight:600" title="English">EN</a>
      <span style="color:rgba(255,255,255,.2)">|</span>
      <a href="/fr/" style="color:rgba(255,255,255,.4);text-decoration:none" title="Français">FR</a>
      <span style="color:rgba(255,255,255,.2)">|</span>
      <a href="/ar/" style="color:rgba(255,255,255,.4);text-decoration:none" title="العربية">AR</a>
    </div>
    '''
LANG_SWITCHER_FR = '''<div style="display:flex;gap:8px;align-items:center;font-size:9px;letter-spacing:.12em;margin-right:16px">
      <a href="../" style="color:rgba(255,255,255,.4);text-decoration:none" title="English">EN</a>
      <span style="color:rgba(255,255,255,.2)">|</span>
      <a href="../fr/" style="color:var(--gold);text-decoration:none;font-weight:600" title="Français">FR</a>
      <span style="color:rgba(255,255,255,.2)">|</span>
      <a href="../ar/" style="color:rgba(255,255,255,.4);text-decoration:none" title="العربية">AR</a>
    </div>
    '''
LANG_SWITCHER_AR = '''<div style="display:flex;gap:8px;align-items:center;font-size:9px;letter-spacing:.12em;margin-right:16px">
      <a href="../" style="color:rgba(255,255,255,.4);text-decoration:none" title="English">EN</a>
      <span style="color:rgba(255,255,255,.2)">|</span>
      <a href="../fr/" style="color:rgba(255,255,255,.4);text-decoration:none" title="Français">FR</a>
      <span style="color:rgba(255,255,255,.2)">|</span>
      <a href="../ar/" style="color:var(--gold);text-decoration:none;font-weight:600" title="العربية">AR</a>
    </div>
    '''

NAV_ACTIONS = '<div class="nav-actions">'

def add_lang_switcher(html, switcher):
    return html.replace(NAV_ACTIONS, switcher + NAV_ACTIONS, 1)

# ──────────────────────────────────────────────────────────
# BUILD FR
# ──────────────────────────────────────────────────────────
fr = fix_paths(SRC)
fr = fix_meta_fr(fr)
fr = apply_translations(fr, FR)
fr = add_lang_switcher(fr, LANG_SWITCHER_FR)

os.makedirs(os.path.join(BASE, 'fr'), exist_ok=True)
with open(os.path.join(BASE, 'fr', 'index.html'), 'w', encoding='utf-8') as f:
    f.write(fr)
print('FR done:', os.path.join(BASE, 'fr', 'index.html'))

# ──────────────────────────────────────────────────────────
# BUILD AR
# ──────────────────────────────────────────────────────────
ar = fix_paths(SRC)
ar = fix_meta_ar(ar)
ar = apply_translations(ar, AR)
ar = add_lang_switcher(ar, LANG_SWITCHER_AR)

os.makedirs(os.path.join(BASE, 'ar'), exist_ok=True)
with open(os.path.join(BASE, 'ar', 'index.html'), 'w', encoding='utf-8') as f:
    f.write(ar)
print('AR done:', os.path.join(BASE, 'ar', 'index.html'))

# ──────────────────────────────────────────────────────────
# Also add EN switcher to main index.html
# ──────────────────────────────────────────────────────────
en_updated = add_lang_switcher(SRC, LANG_SWITCHER_EN)
with open(os.path.join(BASE, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(en_updated)
print('EN switcher added to index.html')
