# Pages légales du portfolio — une entrée par langue, même ordre que les pages.
# Les textes sont en HTML ; {mail} = lien e-mail, {legal} {privacy} {cookies} {terms} = liens entre pages,
# {gh_pages} {gh_privacy} = pages de GitHub sur les données.
# Ce que le site fait réellement (à garder vrai si le site change) :
#   - aucun formulaire, compte, statistique, publicité, traceur ni cookie ;
#   - polices hébergées sur le site (pas de Google Fonts) ;
#   - une seule entrée de stockage local, « cl-theme », créée au clic sur le bouton de thème ;
#   - hébergement GitHub Pages, qui journalise l'adresse IP des visiteurs pour la sécurité.

SLUGS = ["legal", "privacy", "cookies", "terms"]

GITHUB_PRIVACY = "https://docs.github.com/site-policy/privacy-policies/github-general-privacy-statement"
GITHUB_PAGES_DATA = "https://docs.github.com/pages/getting-started-with-github-pages/about-github-pages#data-collection"
HOST = "GitHub, Inc. (GitHub Pages), 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA"

LEGAL = {
"fr": {
    "updated": "Dernière mise à jour : 13 novembre 2026",
    "nav": "Informations légales", "back": "Retour au portfolio",
    "titles": {"legal": "Mentions légales", "privacy": "Politique de confidentialité", "cookies": "Politique des cookies", "terms": "Conditions d'utilisation"},
    "legal": """
<h2>Éditeur du site</h2>
<p>Ce site est le portfolio personnel de <strong>Clément Lemaine</strong>, particulier et étudiant, résidant à Madrid (Espagne). Il n'a aucune activité commerciale : rien n'y est vendu, il n'y a ni publicité ni paiement.</p>
<p>Contact : {mail}</p>
<h2>Directeur de la publication</h2>
<p>Clément Lemaine.</p>
<h2>Hébergeur</h2>
<p>""" + HOST + """ — <a href="https://github.com">github.com</a>.</p>
<h2>Propriété intellectuelle</h2>
<p>Les textes, la photo, les visuels et le CV appartiennent à Clément Lemaine. Les règles de réutilisation et les marques citées sont détaillées dans les <a href="{terms}">conditions d'utilisation</a>.</p>
<h2>Données personnelles et cookies</h2>
<p>Le site ne collecte aucune donnée par lui-même et ne dépose aucun cookie. Les détails sont dans la <a href="{privacy}">politique de confidentialité</a> et la <a href="{cookies}">politique des cookies</a>.</p>
<h2>Ventes et remboursements</h2>
<p>Le site ne vend aucun produit ni service. Il n'y a donc ni conditions générales de vente, ni politique de remboursement.</p>
""",
    "privacy": """
<p><strong>En bref :</strong> ce site ne vous demande aucune donnée. Il n'a ni formulaire, ni compte, ni outil de statistiques, ni publicité, ni traceur.</p>
<h2>Responsable du traitement</h2>
<p>Clément Lemaine, Madrid (Espagne). Contact : {mail}</p>
<h2>Ce que le site ne fait pas</h2>
<ul>
<li>Aucun formulaire ni création de compte.</li>
<li>Aucune mesure d'audience (pas de Google Analytics ni équivalent), aucune publicité, aucun pixel de réseau social.</li>
<li>Aucun cookie (voir la <a href="{cookies}">politique des cookies</a>).</li>
<li>Aucune ressource chargée depuis un autre site : les polices de caractères sont hébergées sur le site lui-même.</li>
</ul>
<h2>Hébergement : les journaux de GitHub</h2>
<p>Le site est hébergé par GitHub Pages. Comme tout serveur web, GitHub reçoit l'adresse IP de votre appareil et des informations techniques (navigateur, page demandée) pour vous envoyer les pages. <a href="{gh_pages}">GitHub indique</a> enregistrer l'adresse IP des visiteurs à des fins de sécurité. Ce traitement relève de GitHub et de sa <a href="{gh_privacy}">déclaration de confidentialité</a> ; il peut impliquer un transfert vers les États-Unis. Je n'ai pas accès à ces journaux et je ne les utilise pas.</p>
<h2>Si vous m'écrivez</h2>
<p>Si vous m'envoyez un e-mail, je reçois votre adresse, votre nom s'il apparaît, votre message et ses éventuelles pièces jointes.</p>
<ul>
<li><strong>Pourquoi :</strong> uniquement pour vous répondre, par exemple au sujet d'un stage ou d'une offre.</li>
<li><strong>Base légale :</strong> mon intérêt légitime à répondre aux messages reçus et, quand vous me contactez pour une opportunité, les échanges préalables à un éventuel contrat (art. 6.1.f et 6.1.b du RGPD).</li>
<li><strong>Durée :</strong> le temps de l'échange, puis au plus 3 ans après notre dernier contact. Vous pouvez demander la suppression avant.</li>
<li><strong>Destinataires :</strong> personne d'autre que moi. La boîte de réception est fournie par mon école (Vatel), qui l'héberge.</li>
</ul>
<h2>Choix du thème clair ou sombre</h2>
<p>Si vous changez de thème, ce choix est enregistré dans votre navigateur et n'est jamais transmis. Voir la <a href="{cookies}">politique des cookies</a>.</p>
<h2>Liens vers d'autres sites</h2>
<p>Les liens vers LinkedIn ou vers d'autres sites ouvrent des services qui ont leurs propres règles de confidentialité. Rien n'est chargé depuis ces sites tant que vous ne cliquez pas.</p>
<h2>Vos droits</h2>
<p>Vous pouvez demander l'accès à vos données, leur rectification, leur effacement, la limitation de leur traitement, leur portabilité ou vous y opposer, en écrivant à {mail}. Je réponds dans un délai d'un mois.</p>
<p>Vous pouvez aussi déposer une réclamation auprès d'une autorité de protection des données : l'<a href="https://www.aepd.es">AEPD</a> en Espagne, où je réside, ou celle de votre pays (en France, la <a href="https://www.cnil.fr">CNIL</a>).</p>
<h2>Modifications</h2>
<p>Si le site change sa façon de traiter des données, cette page sera mise à jour avant le changement, et sa date avec.</p>
""",
    "cookies": """
<p><strong>Ce site ne dépose aucun cookie</strong>, ni les siens ni ceux d'un autre site. Il n'y a donc pas de bandeau de consentement : il n'aurait rien à vous demander.</p>
<h2>Le seul élément enregistré sur votre appareil</h2>
<table>
<thead><tr><th>Nom</th><th>Détail</th></tr></thead>
<tbody>
<tr><td>Nom</td><td><code>cl-theme</code> (stockage local du navigateur, pas un cookie)</td></tr>
<tr><td>Rôle</td><td>Retenir le thème clair ou sombre que vous avez choisi</td></tr>
<tr><td>Créé quand</td><td>Seulement si vous cliquez sur le bouton de thème</td></tr>
<tr><td>Durée</td><td>Jusqu'à ce que vous effaciez les données du site dans votre navigateur</td></tr>
<tr><td>Transmis</td><td>Jamais : il reste sur votre appareil</td></tr>
</tbody>
</table>
<h2>Pourquoi aucun consentement n'est demandé</h2>
<p>Les règles sur les traceurs (article 5.3 de la directive ePrivacy, article 82 de la loi Informatique et Libertés en France, article 22.2 de la LSSI en Espagne) exemptent de consentement ce qui est strictement nécessaire à un service que vous demandez expressément. La CNIL et l'AEPD citent la mémorisation d'un choix de présentation fait par l'utilisateur parmi ces cas.</p>
<h2>Contenus d'autres sites</h2>
<p>Le site ne charge rien depuis un autre site : pas de polices Google, pas de vidéo intégrée, pas de bouton de partage. L'aperçu mobile affiche ce même site. Les liens vers LinkedIn ou d'autres sites n'ouvrent ces services que si vous cliquez, et leurs propres règles sur les cookies s'appliquent alors.</p>
<h2>Supprimer le choix de thème</h2>
<p>Effacez les données de ce site dans les réglages de votre navigateur. Le site reprendra le thème clair par défaut.</p>
<h2>Si cela change</h2>
<p>Si un jour j'ajoute un outil qui en a besoin (statistiques, vidéo intégrée…), votre accord sera demandé avant tout dépôt, et cette page sera mise à jour.</p>
""",
    "terms": """
<h2>Objet</h2>
<p>Ce site présente mon parcours, mes projets et mon CV. Il est accessible gratuitement, sans inscription. En l'utilisant, vous acceptez les présentes conditions.</p>
<h2>Propriété intellectuelle</h2>
<p>Les textes, la photo, la mise en page, les visuels et le CV sont la propriété de Clément Lemaine. Vous pouvez les consulter, télécharger et imprimer pour un usage personnel ou dans le cadre d'un recrutement. Toute autre reproduction ou réutilisation, en particulier de la photo, nécessite mon accord écrit.</p>
<h2>Marques et projets cités</h2>
<p>Les noms et marques cités (Jumeirah, Loewe, LVMH, Vatel, DRM Fishing, PrestaShop, Nasdaq, LinkedIn…) appartiennent à leurs titulaires. Ils servent uniquement à décrire mes expériences et mes projets, et n'impliquent aucun partenariat ni aucune approbation de leur part.</p>
<p>Les polices Instrument Sans et Instrument Serif sont utilisées sous licence SIL Open Font License 1.1.</p>
<h2>Liens vers d'autres sites</h2>
<p>Les liens vers d'autres sites sont donnés pour information. Je ne contrôle pas leur contenu et n'en suis pas responsable.</p>
<h2>Responsabilité</h2>
<p>Les informations sont données de bonne foi et tenues à jour au mieux, sans garantie d'exhaustivité. Le site peut être interrompu ou modifié à tout moment.</p>
<h2>Droit applicable</h2>
<p>Ces conditions sont soumises au droit espagnol. Si vous êtes consommateur, vous conservez la protection des règles impératives de votre pays de résidence.</p>
<h2>Contact</h2>
<p>{mail}</p>
""",
},
"en": {
    "updated": "Last updated: 13 November 2026",
    "nav": "Legal information", "back": "Back to the portfolio",
    "titles": {"legal": "Legal notice", "privacy": "Privacy policy", "cookies": "Cookie policy", "terms": "Terms of use"},
    "legal": """
<h2>Publisher</h2>
<p>This site is the personal portfolio of <strong>Clément Lemaine</strong>, a private individual and student living in Madrid (Spain). It has no commercial activity: nothing is sold, and there are no ads or payments.</p>
<p>Contact: {mail}</p>
<h2>Publication director</h2>
<p>Clément Lemaine.</p>
<h2>Hosting</h2>
<p>""" + HOST + """ — <a href="https://github.com">github.com</a>.</p>
<h2>Intellectual property</h2>
<p>The texts, photo, visuals and CV belong to Clément Lemaine. Reuse rules and the brands mentioned are covered in the <a href="{terms}">terms of use</a>.</p>
<h2>Personal data and cookies</h2>
<p>The site collects no data itself and sets no cookies. See the <a href="{privacy}">privacy policy</a> and the <a href="{cookies}">cookie policy</a>.</p>
<h2>Sales and refunds</h2>
<p>The site sells no products or services, so there are no terms of sale and no refund policy.</p>
""",
    "privacy": """
<p><strong>In short:</strong> this site asks you for no data. It has no forms, no accounts, no analytics, no ads and no trackers.</p>
<h2>Data controller</h2>
<p>Clément Lemaine, Madrid (Spain). Contact: {mail}</p>
<h2>What the site does not do</h2>
<ul>
<li>No forms and no account creation.</li>
<li>No audience measurement (no Google Analytics or similar), no ads, no social media pixels.</li>
<li>No cookies (see the <a href="{cookies}">cookie policy</a>).</li>
<li>Nothing loaded from other sites: the fonts are hosted on the site itself.</li>
</ul>
<h2>Hosting: GitHub's logs</h2>
<p>The site is hosted on GitHub Pages. Like any web server, GitHub receives your device's IP address and technical information (browser, page requested) in order to send you the pages. <a href="{gh_pages}">GitHub states</a> that it logs visitors' IP addresses for security purposes. This processing is GitHub's, under its <a href="{gh_privacy}">privacy statement</a>, and may involve a transfer to the United States. I have no access to these logs and do not use them.</p>
<h2>If you email me</h2>
<p>If you send me an email, I receive your address, your name if it appears, your message and any attachments.</p>
<ul>
<li><strong>Why:</strong> only to reply to you, for example about an internship or a job.</li>
<li><strong>Legal basis:</strong> my legitimate interest in replying to messages and, when you contact me about an opportunity, steps taken before a possible contract (Art. 6(1)(f) and 6(1)(b) GDPR).</li>
<li><strong>Retention:</strong> for the time of our exchange, then at most 3 years after our last contact. You can ask me to delete it sooner.</li>
<li><strong>Recipients:</strong> nobody but me. The mailbox is provided and hosted by my school (Vatel).</li>
</ul>
<h2>Light or dark theme</h2>
<p>If you switch themes, your choice is saved in your browser and never sent anywhere. See the <a href="{cookies}">cookie policy</a>.</p>
<h2>Links to other sites</h2>
<p>Links to LinkedIn or other sites open services with their own privacy rules. Nothing is loaded from those sites unless you click.</p>
<h2>Your rights</h2>
<p>You can ask to access, correct or erase your data, restrict or object to its processing, or receive it in a portable format, by writing to {mail}. I reply within one month.</p>
<p>You can also lodge a complaint with a data protection authority: the <a href="https://www.aepd.es">AEPD</a> in Spain, where I live, or the authority in your own country.</p>
<h2>Changes</h2>
<p>If the way the site handles data changes, this page and its date will be updated before the change.</p>
""",
    "cookies": """
<p><strong>This site sets no cookies</strong>, neither its own nor any other site's. That is why there is no consent banner: it would have nothing to ask you.</p>
<h2>The only thing saved on your device</h2>
<table>
<thead><tr><th>Item</th><th>Details</th></tr></thead>
<tbody>
<tr><td>Name</td><td><code>cl-theme</code> (browser local storage, not a cookie)</td></tr>
<tr><td>Purpose</td><td>Remembers the light or dark theme you chose</td></tr>
<tr><td>Created</td><td>Only if you click the theme button</td></tr>
<tr><td>Duration</td><td>Until you clear this site's data in your browser</td></tr>
<tr><td>Shared</td><td>Never: it stays on your device</td></tr>
</tbody>
</table>
<h2>Why no consent is requested</h2>
<p>The rules on trackers (Article 5(3) of the ePrivacy Directive, Article 82 of the French Data Protection Act, Article 22.2 of the Spanish LSSI) exempt what is strictly necessary for a service you explicitly request. The French (CNIL) and Spanish (AEPD) authorities list remembering a display choice made by the user among those cases.</p>
<h2>Content from other sites</h2>
<p>The site loads nothing from other sites: no Google Fonts, no embedded videos, no share buttons. The mobile preview shows this same site. Links to LinkedIn or other sites only open those services if you click, and their own cookie rules then apply.</p>
<h2>Deleting your theme choice</h2>
<p>Clear this site's data in your browser settings. The site will go back to the default light theme.</p>
<h2>If this changes</h2>
<p>If I ever add a tool that needs it (analytics, embedded video…), your consent will be asked before anything is stored, and this page will be updated.</p>
""",
    "terms": """
<h2>Purpose</h2>
<p>This site presents my background, my projects and my CV. It is free to use, with no sign-up. By using it, you accept these terms.</p>
<h2>Intellectual property</h2>
<p>The texts, photo, layout, visuals and CV belong to Clément Lemaine. You may view, download and print them for personal use or for recruitment purposes. Any other reproduction or reuse, especially of the photo, requires my written consent.</p>
<h2>Brands and projects mentioned</h2>
<p>The names and brands mentioned (Jumeirah, Loewe, LVMH, Vatel, DRM Fishing, PrestaShop, Nasdaq, LinkedIn…) belong to their owners. They are used only to describe my experience and projects, and imply no partnership or endorsement.</p>
<p>The Instrument Sans and Instrument Serif fonts are used under the SIL Open Font License 1.1.</p>
<h2>Links to other sites</h2>
<p>Links to other sites are provided for information. I do not control their content and am not responsible for it.</p>
<h2>Liability</h2>
<p>The information is given in good faith and kept as up to date as possible, with no guarantee that it is complete. The site may be interrupted or changed at any time.</p>
<h2>Governing law</h2>
<p>These terms are governed by Spanish law. If you are a consumer, you keep the protection of the mandatory rules of your country of residence.</p>
<h2>Contact</h2>
<p>{mail}</p>
""",
},
"es": {
    "updated": "Última actualización: 13 de noviembre de 2026",
    "nav": "Información legal", "back": "Volver al portfolio",
    "titles": {"legal": "Aviso legal", "privacy": "Política de privacidad", "cookies": "Política de cookies", "terms": "Condiciones de uso"},
    "legal": """
<h2>Titular del sitio</h2>
<p>Esta web es el portfolio personal de <strong>Clément Lemaine</strong>, particular y estudiante, residente en Madrid (España). No tiene actividad comercial: no se vende nada, no hay publicidad ni pagos.</p>
<p>Contacto: {mail}</p>
<h2>Responsable de la publicación</h2>
<p>Clément Lemaine.</p>
<h2>Alojamiento</h2>
<p>""" + HOST + """ — <a href="https://github.com">github.com</a>.</p>
<h2>Propiedad intelectual</h2>
<p>Los textos, la foto, los elementos visuales y el CV pertenecen a Clément Lemaine. Las reglas de reutilización y las marcas citadas se detallan en las <a href="{terms}">condiciones de uso</a>.</p>
<h2>Datos personales y cookies</h2>
<p>La web no recoge datos por sí misma ni instala cookies. Los detalles están en la <a href="{privacy}">política de privacidad</a> y la <a href="{cookies}">política de cookies</a>.</p>
<h2>Ventas y reembolsos</h2>
<p>La web no vende productos ni servicios. Por eso no hay condiciones de venta ni política de reembolso.</p>
""",
    "privacy": """
<p><strong>En resumen:</strong> esta web no te pide ningún dato. No tiene formularios, cuentas, estadísticas, publicidad ni rastreadores.</p>
<h2>Responsable del tratamiento</h2>
<p>Clément Lemaine, Madrid (España). Contacto: {mail}</p>
<h2>Lo que la web no hace</h2>
<ul>
<li>Ningún formulario ni registro de cuenta.</li>
<li>Ninguna medición de audiencia (ni Google Analytics ni similares), publicidad ni píxeles de redes sociales.</li>
<li>Ninguna cookie (ver la <a href="{cookies}">política de cookies</a>).</li>
<li>Nada se carga desde otras webs: las fuentes tipográficas están alojadas en la propia web.</li>
</ul>
<h2>Alojamiento: los registros de GitHub</h2>
<p>La web está alojada en GitHub Pages. Como cualquier servidor web, GitHub recibe la dirección IP de tu dispositivo e información técnica (navegador, página solicitada) para enviarte las páginas. <a href="{gh_pages}">GitHub indica</a> que registra la dirección IP de los visitantes por motivos de seguridad. Este tratamiento corresponde a GitHub, según su <a href="{gh_privacy}">declaración de privacidad</a>, y puede implicar una transferencia a Estados Unidos. No tengo acceso a esos registros ni los utilizo.</p>
<h2>Si me escribes</h2>
<p>Si me envías un correo, recibo tu dirección, tu nombre si aparece, tu mensaje y sus posibles adjuntos.</p>
<ul>
<li><strong>Para qué:</strong> solo para responderte, por ejemplo sobre unas prácticas o una oferta.</li>
<li><strong>Base jurídica:</strong> mi interés legítimo en responder a los mensajes y, cuando me contactas por una oportunidad, la aplicación de medidas precontractuales (art. 6.1.f y 6.1.b del RGPD).</li>
<li><strong>Conservación:</strong> el tiempo del intercambio y, como máximo, 3 años después de nuestro último contacto. Puedes pedir que se borren antes.</li>
<li><strong>Destinatarios:</strong> nadie más que yo. El buzón lo proporciona y aloja mi escuela (Vatel).</li>
</ul>
<h2>Tema claro u oscuro</h2>
<p>Si cambias de tema, tu elección se guarda en tu navegador y nunca se envía. Ver la <a href="{cookies}">política de cookies</a>.</p>
<h2>Enlaces a otras webs</h2>
<p>Los enlaces a LinkedIn u otras webs abren servicios con sus propias normas de privacidad. No se carga nada de esas webs si no haces clic.</p>
<h2>Tus derechos</h2>
<p>Puedes solicitar el acceso a tus datos, su rectificación, supresión, la limitación de su tratamiento, su portabilidad u oponerte a él, escribiendo a {mail}. Respondo en el plazo de un mes.</p>
<p>También puedes presentar una reclamación ante la <a href="https://www.aepd.es">Agencia Española de Protección de Datos (AEPD)</a> o ante la autoridad de tu país.</p>
<h2>Cambios</h2>
<p>Si cambia la forma en que la web trata datos, esta página y su fecha se actualizarán antes del cambio.</p>
""",
    "cookies": """
<p><strong>Esta web no instala ninguna cookie</strong>, ni propia ni de terceros. Por eso no hay banner de consentimiento: no tendría nada que pedirte.</p>
<h2>Lo único que se guarda en tu dispositivo</h2>
<table>
<thead><tr><th>Elemento</th><th>Detalle</th></tr></thead>
<tbody>
<tr><td>Nombre</td><td><code>cl-theme</code> (almacenamiento local del navegador, no es una cookie)</td></tr>
<tr><td>Finalidad</td><td>Recordar el tema claro u oscuro que elegiste</td></tr>
<tr><td>Cuándo se crea</td><td>Solo si haces clic en el botón de tema</td></tr>
<tr><td>Duración</td><td>Hasta que borres los datos de esta web en tu navegador</td></tr>
<tr><td>Se comparte</td><td>Nunca: se queda en tu dispositivo</td></tr>
</tbody>
</table>
<h2>Por qué no se pide consentimiento</h2>
<p>Las normas sobre dispositivos de almacenamiento (artículo 22.2 de la LSSI, artículo 5.3 de la Directiva ePrivacy) eximen de consentimiento lo estrictamente necesario para un servicio que solicitas expresamente. La Guía sobre el uso de las cookies de la AEPD incluye entre esos casos las cookies de personalización de la interfaz elegida por el usuario.</p>
<h2>Contenidos de otras webs</h2>
<p>La web no carga nada desde otras webs: ni fuentes de Google, ni vídeos incrustados, ni botones para compartir. La vista móvil muestra esta misma web. Los enlaces a LinkedIn u otras webs solo abren esos servicios si haces clic, y entonces se aplican sus propias normas sobre cookies.</p>
<h2>Borrar tu elección de tema</h2>
<p>Borra los datos de esta web en los ajustes de tu navegador. La web volverá al tema claro por defecto.</p>
<h2>Si esto cambia</h2>
<p>Si algún día añado una herramienta que lo necesite (estadísticas, vídeo incrustado…), se pedirá tu consentimiento antes de guardar nada, y esta página se actualizará.</p>
""",
    "terms": """
<h2>Objeto</h2>
<p>Esta web presenta mi trayectoria, mis proyectos y mi CV. Es gratuita y no requiere registro. Al usarla, aceptas estas condiciones.</p>
<h2>Propiedad intelectual</h2>
<p>Los textos, la foto, el diseño, los elementos visuales y el CV son propiedad de Clément Lemaine. Puedes consultarlos, descargarlos e imprimirlos para uso personal o en un proceso de selección. Cualquier otra reproducción o reutilización, en particular de la foto, requiere mi autorización por escrito.</p>
<h2>Marcas y proyectos citados</h2>
<p>Los nombres y marcas citados (Jumeirah, Loewe, LVMH, Vatel, DRM Fishing, PrestaShop, Nasdaq, LinkedIn…) pertenecen a sus titulares. Solo sirven para describir mis experiencias y proyectos, y no implican ninguna colaboración ni aprobación por su parte.</p>
<p>Las fuentes Instrument Sans e Instrument Serif se usan bajo la licencia SIL Open Font License 1.1.</p>
<h2>Enlaces a otras webs</h2>
<p>Los enlaces a otras webs se ofrecen a título informativo. No controlo su contenido ni soy responsable de él.</p>
<h2>Responsabilidad</h2>
<p>La información se ofrece de buena fe y se mantiene actualizada en la medida de lo posible, sin garantía de que sea completa. La web puede interrumpirse o modificarse en cualquier momento.</p>
<h2>Ley aplicable</h2>
<p>Estas condiciones se rigen por la ley española. Si eres consumidor, conservas la protección de las normas imperativas de tu país de residencia.</p>
<h2>Contacto</h2>
<p>{mail}</p>
""",
},
}
