#!/usr/bin/env python3
"""
02_graph_cleaning.py
====================
Limpieza del grafo social: eliminación de nodos sin sentido y fusión de duplicados.

Uso:
    python 02_graph_cleaning.py

Entrada:  data/processed/epstein_social_graph.gml
Salida:   data/processed/epstein_social_graph_cleaned.gml
"""

import re
import networkx as nx
from collections import defaultdict

# ──────────────────────────────────────────────
# 1. CARGA DEL GRAFO
# ──────────────────────────────────────────────
INPUT_PATH  = "../data/processed/epstein_social_graph.gml"
OUTPUT_PATH = "../data/processed/epstein_social_graph_cleaned.gml"

G = nx.read_gml(INPUT_PATH)
print(f"Grafo original: {G.number_of_nodes()} nodos, {G.number_of_edges()} aristas")

# Construimos un mapeo label → node_key  (en GML de NetworkX, el key del nodo es el label)
all_labels = set(G.nodes())

# ──────────────────────────────────────────────
# 2. IDENTIFICACIÓN DE NODOS SIN SENTIDO
# ──────────────────────────────────────────────

def is_nonsensical(label: str) -> bool:
    """Devuelve True si la label NO es un nombre plausible de persona/organización."""
    s = label.strip()

    # 2a. Demasiado corto (< 3 caracteres)
    if len(s) < 3:
        return True

    # 2b. Contiene muy pocas letras en proporción
    alpha_chars = sum(1 for c in s if c.isalpha())
    if alpha_chars == 0:
        return True
    if len(s) > 4 and alpha_chars / len(s) < 0.40:
        return True

    # 2c. Es un nombre de archivo
    if re.search(r'\.(pdf|htm|html|gml|csv|gexf|png|jpg)$', s, re.I):
        return True
    if s.endswith('htm') and ' ' not in s:
        return True

    # 2d. Parece una frase larga (más de 10 palabras y contiene palabras comunes en inglés)
    words = s.split()
    sentence_words = {'the', 'is', 'are', 'you', 'my', 'your', 'was', 'were', 'but',
                      'have', 'has', 'that', 'this', 'with', 'for', 'not', 'can',
                      'will', 'would', 'should', 'could', 'about', 'from', 'they',
                      'their', 'been', 'being', 'which', 'when', 'where', 'what',
                      'how', 'who', 'also', 'than', 'then', 'just', 'only', 'very',
                      'some', 'any', 'each', 'every', 'all', 'both', 'few', 'more',
                      'most', 'other', 'into', 'over', 'such', 'because', 'always',
                      'never', 'sometimes', 'often', 'going', 'tried', 'hope',
                      'please', 'welcome', 'good', 'bad', 'well', 'may', 'might',
                      'shall', 'if', 'or', 'and', 'so', 'yet', 'nor', 'an', 'a',
                      'to', 'of', 'in', 'on', 'at', 'by', 'up', 'do', 'no', 'am',
                      'fabulous', 'anytime', 'convenience', 'otherwise', 'drawing',
                      'board', 'cruise', 'january', 'february', 'thanksgiving',
                      'peaceful', 'talking', 'interesting', 'times', 'answers',
                      'ignore', 'ambushed', 'reporters', 'receive', 'calls',
                      'photos', 'look', 'tried', 'slightly', 'hipper', 'youthful'}
    if len(words) > 8:
        common_count = sum(1 for w in words if w.lower() in sentence_words)
        if common_count >= 3:
            return True

    # 2e. Patrones de metadatos de email
    lower = s.lower()
    metadata_patterns = [
        'undisclosed recipients', 'undisclosed-recipients',
        'multiple senders', 'all receiving offices',
        'comms alert', 'scoop notifications', 'google alerts',
        'quora digest', 'philanthropy', 'full text articles',
        'mailer-daemon@', 'courtmail@', 'digest-noreply@',
        'editorialstaff@', 'all-research@',
        'from:', 'privileged - redacted',
        'untitled attachment',
    ]
    for pat in metadata_patterns:
        if pat in lower:
            return True

    # 2f. Patrones de basura OCR frecuentes
    ocr_garbage = [
        'momminnemummin', 'otsttrtoton', 'cscscscsci',
        'isscsss', 'oe—sscscs', 'o—s—cscscs',
    ]
    for pat in ocr_garbage:
        if pat in lower:
            return True

    # 2g. Solo letras sueltas / tokens cortos sin sentido (3 chars, todas consonantes raras)
    if len(s) <= 3 and not re.search(r'[aeiou]', s, re.I):
        return True

    return False


# Lista explícita adicional de nodos a eliminar que pasan los filtros heurísticos
EXPLICIT_REMOVE = {
    # Letras sueltas / fragmentos muy cortos sin sentido
    'a', 'as', 'be', 'bee', 'cc', 'cl', 'cs', 'csc', 'cscc', 'ec', 'ed',
    'ee', 'eee', 'ees', 'eg', 'es', 'es ee', 'es es', 'et', 'et ies',
    'ev rotc', 'f', 'fe', 'g', 'g g', 'gg', 'hs', 'i', 'i ee',
    'i vote', 'i! sis', 'ia', 'iabory', 'ie', 'ii', 'iii', 'iin',
    'in cilings', 'is cote', 'ix', 'iy', 'j', 'j j', 'jp', 'l',
    'las', 'lem', 'lh', 'lhs', 'lhs te', 'ls', 'lsj', 'lv ct',
    'ly', 'm', 'm1j', 'mbr', 'me', 'meg', 'mm', 'ms', 'nn', 'nine',
    'oi', 'oi at', 'or ts', 're', 's', 'ss', 'ts', 'w', 'x',
    'xy', 'y', '1s', '4s', '6 e', '6 mxwe', '<a', '[ae', '[i rote',
    'a', 'a ticsscs', '- mmiimim', 'gmax', 'lvje', 'lvjet',
    'bs stern', 'cilings', 'drsra', 'jee', 'lito',
    'ny max', 'on trump', 'from a', 'from:', 'house',
    'dear friends', 'dear men', 'herald', 'miami', 'miami @',
    'new york', 'possibly', 'story', 'ugh', 'please',
    # OCR garbage
    'le rere otsttrtoton', 'momminnemummin',
    'oe\u2014sscscs', 'o\u2014s\u2014cscscscsci\u00e9iss',
    'es | &2252: 2052:', 'lhs ~~ 0 i sss\u2014\u2018\u201cisscsss',
    # Frases
    'but my answers are always 1 have nothing to say or i try to ignore altogether a few times i have been ambushed on the street with questions but am more careful now hope you are well photos look good fyi i receive many calls a week about both donald and clinton from reporters less so recently with clinton',
    'are you going to stop in st thomas on your cruise?',
    'ill be there wed',
    "fabulous! may i buy you lunch?",
    'hope thanksgiving is peaceful miss talking to you',
    'great great anytime at your convenience or you can come to the house',
    'i can organize anytime with wife your call otherwise new york dec 6-9? interesting times http ://www dailymail co uk/news/article-3914012/troub led-woman-history-drug-use-claime d-ass aulted-d onald- trump -jeffrey-ep stein-sex -p arty-age-13 -fabricated-story html you are always welcome if you would like to visit caribean',
    'i can organize anytime with wife your call otherwise new york dec 6-9? you are always welcome if you would like to visit caribean',
    'no st thomas back to the drawing board hope youre well greetings! just got my hands on the itinerary alas',
    'or ny when youre next there many thanks darn on a cruise in the aforementioned caribbean that week weekly standard post-election cruise bad timing on our part well try for january-february in warm climate',
    'only you please',
    'ken and to you as well well be at the breakers en famine as of tuesday evening any chance to see you in the sunshine state? hugs',
    'and back in the day tried to be seen as slightly hipper, more youthful and considered a bit more clever than its big name rival almost an anti-establishment playboy a slogan stated: your dad bought playboy, you bought cavalier for the american male) was published the year before playboy to whom it has often been compared',
    # Archivos adjuntos
    'company-overview_pdfhtml',
    # Metadata de email
    'multiple senders', 'all receiving offices', 'comms alert',
    'google alerts',
    'digest-noreply@quoracom',
    'mailer-daemon@p3plismtp05-03prodphx3secureservernet',
    'courtmail@nysduscourtsgov',
    'editorialstaff@flipboardcom',
    'all-research@mitedu',
    'nysd ecf pool@nysduscourtsgov',
    # Fragmentos de CC / encabezados
    'cc', 'cc: ainbanklaw info; denyse sabagh;',
    'ce: nick pykc si li: hartley',
    'cn=anne boyles/o=palmbeach',
    'i (sienna ee',
    'es | &#38;2252: 2052:',
    'lhs ~~ 0 i sss&#8212;&#8216;&#8220;isscsss',
    'o&#8212;s&#8212;cscscscsci&#233;iss',
    'oe&#8212;sscscs',
    # Emails puros sin nombre
    'jeevacation@gmailcom',
    'jeeproject@yahoocom',
    'jeffreyepsteinorg@gmailcom',
    'jeffrey@jeffreyepsteinorg',
    'live:linkspirit',
}

nodes_to_remove = set()
for node in list(G.nodes()):
    label = G.nodes[node].get('label', node) if isinstance(node, int) else node
    lab = str(label).lower().strip()
    if lab in EXPLICIT_REMOVE or is_nonsensical(lab):
        nodes_to_remove.add(node)

print(f"\nNodos marcados para eliminar (sin sentido): {len(nodes_to_remove)}")

# ──────────────────────────────────────────────
# 3. DEFINICIÓN DE CLUSTERS DE DUPLICADOS
# ──────────────────────────────────────────────
# Formato: canonical_label → [lista de labels duplicadas]
# Todos en minúsculas, tal como aparecen en el GML.

MERGE_CLUSTERS = {
    "jeffrey e": [   # Este es probablemente el nodo hub; lo renombraremos a "jeffrey epstein"
        "j epstein", "jeff epstein", "epstein jeffrey", "jeffrey",
        "jeffery", "je gmail", "je vacation", "jeffery vacation",
        "jeffrey e vacation", "jeffrey / e / epstein",
        "jeffrey epstein", "jeffrey epstein jeevacation@gmailcom",
        "jeffrey epstein usa", "jeffrey leevacation@gmailcom",
        "e jeffrey", "jeevacation",
        "j jep jeevacation@gmailcom", "j jep",
        "ej 2cvacation@gmailcom",
        "j <jeevacation@gmailcom]",
        "jeffrey e <jeevacation@gmailcom]",
        "jeficy 5 i;",
        "derby je vacation", "jeff",
        "j jep", "jeff epstein",
        "jeffery edwards",  # This might be different - removing from merge
        "donalad trup",  # NO - this is a different reference
    ],
    "darren indyke": [
        "darren", "darren indivig", "darren indykc xy",
        "darren indyke (sah", "darren indyke <_i\u2014 as",
        "darren indyke [mailt", "darren indyke ________________",
        "darren indyke ao", "darren indyke iis",
        "darren indyke jeevacation@gmailcom",
        "darren indyke py", "darren indyke jeffrey epstein",
        "dee jecvecation@emailcom",
        "jecvacation@emailcom", "deeyacation@gmailcom",
        "darren a jack goldberger",
    ],
    "kathy ruemmler": [
        "kathy", "kathy er", "kathy rucmm", "kathy rucmmicr",
        "kathy rue", "kathy rue ler", "kathy ruemm",
        "kathy ruemm ler i", "kathy ruemmeli",
        "kathy ruemmler te darren indykc iy",
        "kathy ruemmler | as |", "kathy ruemm|cr",
        "kathy ruemm|cr sa", "kathy ruemm|er in",
        "kathy ruennler", "kathy ruernn|er lr",
        "a e a kathy ruemmler ee darren indyke",
    ],
    "martin weinberg": [
        "martin", "esq martin weinberg", "im: martin weinberg",
        "martin g weinberg i gerald b lefcourt",
        "martin g weinberg iii", "martin g weinberg p",
        "martin weinbcro", "martin weinberg [ni",
        "martin weinberg ee", "martin weinberg esq ed",
        "martin weinberg ii darren indyke | kathy ruemmler",
        "martin weinberg me \u00ab jeffrey epstein",
        "martin weinberg pf", "mr weinberg",
        "martin weinberg me &#171; jeffrey epstein",
    ],
    "michael wolff": [
        "michacl wola", "michael wo!", "michael wo! [aaa",
        "michael wo! ffi", "michael wo! ft", "michael wo!ft a",
        "michael wol [rr", "michael wola", "michael wolf? iii",
        "michael wolff <a nfw", "michael wolff <q",
        "michael wolff [ee", "michael wolff [is",
        "michael wolff i rote", "michael wolff ii",
        "michael wolff nn", "michael wolff otc",
        "michael wolff po", "michael wolft [s",
        "michael woli", "michael woltt", "michael wott <r",
        "michael wott [ia", "miche! woltt",
    ],
    "steve bannon": [
        "steve ban)", "steve bannon (ies",
        "steve bannon [nas", "steve bannon [nn",
        "steve bannon iii", "steve bannon pf",
        "steve bannon qq", "steve bannor", "steve bano",
        "sean bann cr", "sean bannon",
    ],
    "landon thomas jr": [
        "ladr1 iii iii thomas jr", "land a thomas jr",
        "lando iii ti iii thomas jr",
        "landon <_______________________ thomas jr",
        "landon [iy| thomas jr", "landon iii thomas jr",
        "landon po thomas jr", "landon rr thomas jr",
        "landon thomas", "landon thomas j iii",
        "landon thomas | ee", "landon thorns",
        "landon xy thomas jr", "mace thomas jr",
        "2ndr i thomas j", "jr landon thomas",
    ],
    "larry summers": [
        "larry summers <9", "larry summers <_ rr wr otc",
        "larry summers <ns", "larry summers | a s",
        "larry summers |s |", "larry sunes",
        "larrysunmers", "lary sinners",
        "lawrence summers", "lawrence summers (a",
        "lawrence summers ii", "lawrence henry summers",
    ],
    "reid weingarten": [
        "dd weingarten", "reid weingarten",
    ],
    "lesley groff": [
        "lesley", "lesley grof a", "lesley groff [mmiiii;",
        "lesley groff pd", "lesley groft",
    ],
    "richard kahn": [
        "alan richard kahn (i: diucash",
        "amanda richard kohn ens",
    ],
    "jack goldberger": [
        "jack goldberger es", "goelberg", "golenbrg", "jack nn",
    ],
    "peggy siegal": [
        "peggy",
    ],
    "lisa new": [
        "lisa new <7 e", "lisa new ____l", "lisa new ay",
        "lisa new ee", "lisa new i", "lisa new te",
    ],
    "lawrence krauss": [
        "dr krauss", "lawkrauss", "lawrence kraus [i",
        "lawrence krauss iii", "lawrence krauss jin",
        "lawrence krauss laie at",
    ],
    "nicholas ribis": [
        "nicholas rib <i", "nicholas ribis [a",
        "nicholas ribis ii", "nicholas ribis ts",
        "nicholas rit iii", "nicholasribis in",
    ],
    "noam chomsky": [
        "chomsky", "noam chomsky <q", "noam chomsky [as",
    ],
    "robert trivers": [
        "robert trivers [a", "robert trivers [nn",
        "robert trivers fs",
    ],
    "paul krassner": [
        "paul krassner <q", "paul krassner [ie",
        "paul krassner [sn", "paul krassner ii",
        "paul krassner | a |",
    ],
    "linda stone": [
        "linda stone [s", "linda stone py",
        "linda stone tr", "linde stn he",
    ],
    "david stern": [
        "david stern oy", "david stern tt",
        "david stern {qq", "david sterr i",
    ],
    "boris nikolic": [
        "boris", "boris niki", "boris niko", "boris nikolic <n",
    ],
    "ehud barak": [
        "barrack barak", "barrak", "chbarak", "chbarak x",
        "ehbarak", "nil priell barak", "mongolia gambat ehud",
    ],
    "deepak chopra": [
        "deepak chopra <j", "deepak chopra ay", "deepak chopra se",
    ],
    "ghislaine maxwell": [
        "ghislaine", "g maxwell", "gm ax",
        "gmax gmax1@ellmaxcom", "gmax1@ellmaxcom",
        "fan maxwell",
    ],
    "sultan bin sulayem": [
        "sultan ahmed bin sulayem",
    ],
    "jack lang": [
        "jack lang ep", "jack lang pf", "jacque lang woody", "jacuwe lang",
    ],
    "larry visoski": [
        "larry visoski [ay", "larry visoski me",
        "larry visoski pf", "lawrance visoski",
    ],
    "joi ito": [
        "ito as", "jcichi", "joi", "joichi", "joichi ito",
        "loi ito", "loi to se",
    ],
    "jes staley": [
        "_jes staley <i", "jes staley <a",
        "jes staley [as", "jes: barclays staley",
    ],
    "fred haddad": [
        "fred haddad ps", "haddadfm@aolcom",
    ],
    "peter mandelson": [
        "lord mandelson", "mandelson", "mandelson balir",
        "ben and lord mandelson",
        "iee: peter mandelson",
    ],
    "alan dershowitz": [
        "alan dershowitz sn", "alan m dershowitz",
        "alan m dershowitz fim martin weinberg",
        "alan m dershowitz re jack goldberger pcs",
        "aln deshowit7", "dersh",
    ],
    "jessica cadwell": [
        "jessica cadwell [iy", "jessica cadwell [mailto ae",
        "jessica cadwell po", "paralegal jessica cadwell",
        "cp, frs jessica cadwell",
    ],
    "leon black": [
        "leon", "leon balck", "leon bick", "leon blac is",
        "leon black as weingarten",
    ],
    "barbro c ehnbom": [
        "barbro c ehnborn", "barbro cc ehnbom 1 sr",
        "barbro ehnbom iii", "behnbom", "behnbom@aolcom",
    ],
    "melanie spinella": [
        "mclanic spinclla", "melanie spincla je",
        "melanie spincll", "melanie spine! i",
        "melanie spinella iy", "melanie spinella po",
        "melanie spinella se",
        "melanie spinella x 8 rad wechsler [nn",
    ],
    "eric roth": ["eric roth qq"],
    "etienne binant": ["etienne binant si"],
    "erika kellerhals": ["erika kellerhals ay", "erika kellerhals po"],
    "jacquie johnson": ["jacquie johnson [ nail", "jacquie johnson [mailto"],
    "alan fraade": ["alan fraadc"],
    "gary h baise": [
        "gary h baisallillw", "gary h baisc", "gary h \u2014 i d",
        "gary h &#8212; i d",
    ],
    "joscha bach": ["joscha 82h", "joscha bach [as"],
    "masha drokova": ["masha drokova [a"],
    "brad wechsler": ["brad wcchsicr"],
    "cecilia steen": ["cecilia steer ns"],
    "katherine keating": ["katherine keating qq"],
    "heather mann": ["heather mani", "heather mann po"],
    "jonathan farkas": [
        "jonathan farkas ee", "jonathan farkasiiii",
        "jonathan &#8216;areca",
    ],
    "lilly sanchez": ["lilly", "lilly ann sanchez"],
    "diane ziman": ["diane ziman po"],
    "charlotte abrams": ["charlotte abrams iy"],
    "adrienne ross": ["a dricnne ross", "adricnne ro", "cedricone ross"],
    "daniel siad": ["daniel siac", "daniel sicd", "daniel sick a"],
    "fabrice aidan": ["fabrice aidan [i"],
    "gianni serazzi": ["gianni seraz7i ay"],
    "robert kuhn": [
        "robert kuhn rr", "robert kuhn se",
        "robert l kuhn", "robert l kuhn po",
        "robert lawrence kuhn", "robert lawrence kuhn iii",
    ],
    "el hachem johnny": ["el hachem johnny po", "el hachem johnny qq"],
    "paul barrett": ["paul barred", "paul barrett [is", "paul barrett a >"],
    "ross gow": ["ross gow <i -", "rossacuity gow"],
    "stephen hanson": ["stephen hanson [aa", "stephen hanson [i"],
    "peter thomas roth": ["peter thomas roth iii"],
    "brad edwards": ["brad@pathtojusticecom", "bradley j edwards"],
    "faith kates": ["faith kate sis"],
    "jesse kornbluth": ["jesse kornbluth ps"],
    "cecile de jongh": ["cecile de jongh <a"],
    "david rivkin": ["david <q rivkin"],
    "ann marie c villafana": ["a marie villafa\u00f1a"],
    "gwendolyn beck": ["gwendolyn"],
    "bruce moskowitz": ["bruce moskowitz [is"],
    "barry josephson": ["barry josephson [iii"],
    "glenn dubin": ["glenn dubin <[s"],
    "eva dubin": ["eva dubin <a-"],
    "nancy portland": ["nancy portland [a"],
    "nancy dahl": ["nancy dah!"],
    "osman oz": ["osman", "osman o02"],
    "nima mohebbi": ["nima vmohcbbi"],
    "bill siegel": ["bill siege!"],
    "kevin bright": ["kevin bright ee", "kevin cright"],
    "dan fleuette": ["dan fleuette ii"],
    "david schoen": ["devid schoen"],
    "bill gates": ["bill gates <i;"],
    "anil ambani": [
        "amabani", "ani anbar",
        "anil ambani <anilambani", "anil ambar i",
        "anilambani", "anilambani aa",
    ],
    "juleanna glover": ["juleanna glover fo"],
    "bob &#38; sandy": ["bob &#38; sancall"],
    "danny goldberg": ["danny goldberg caryl ratner", "danny goldberg mb"],
    "anas alrasheed": [
        "anas", "anas alrashecd", "anas raafat",
        "anasalrasheed", "anasalrasheed [ia",
        "anasalrasheed1111", "anasalrasheed@gmailcom",
    ],
    "dkiesq": ["dkiesq po", "dkiesq@aolcom"],
    "criminal investigative": ["criminal tnvdiigative"],
    "andrew m grossman": ["andrew m <a grossman"],
    "ken starr": ["ken po starr", "ken starrk karp", "ken str rr", "ker i starr"],
    "norman d rau": ["norman d rau mmiim"],
    "maria t zuber": ["maria t zuber <p"],
    "nancy cain": ["nancy c2 in"],
    "jabor y": ["jabor", "jabor y as", "jabor y ee", "jabor y inewei"],
    "john brockman": ["john brockman fst"],
    "coy garrett": ["coy e garrett"],
    "lisa randall": ["lisa randa] | aes"],
    "brad s karp": [
        "brad s karp <q melanie spinella <", "brad s korp",
        "brod s kap", "karp brad s <bkarp@paulweisscom]",
    ],
    "liz hartley": ["liz hertey"],
    "caryl ratner": ["cary ratner rs"],
    "amanda ens": ["ananda ens"],
    "lhsoffice": ["ihsofficel", "hscffico"],
    "forrest miller": [
        "forrest miller - adj kearsarge",
        "forrest miller - adj kearsarge house",
    ],
    "authoritarian influence": ["authoritarian influence <mim"],
    "moshe hoffman": ["moshe hoffa [aaa"],
    "matthewschafe": ["matthewschafe i="],
    "louella rabuyo": ["louellarabuycll januiz banasiak"],
    "paul morris": [
        "paul mors", "paul morris/db/",
        "paul morris/db/ vinit sahni/db/",
        "paul morris/db/\u2014 me",
        "paul morris/db/&#8212; me",
    ],
    "harry shearer": [],  # solo si hay variantes
    "jackie perczek": ["jackie perczek cs | derren indyxc"],
}


# ──────────────────────────────────────────────
# 4. FUNCIÓN DE MERGE
# ──────────────────────────────────────────────

def merge_node(G, canonical, duplicate):
    """Fusiona 'duplicate' en 'canonical': redirige aristas y suma pesos."""
    if duplicate not in G or canonical not in G:
        return
    if duplicate == canonical:
        return

    # Redirigir aristas del duplicado al canónico
    for neighbor in list(G.neighbors(duplicate)):
        if neighbor == canonical:
            # Sería un auto-lazo → ignorar
            continue
        if neighbor == duplicate:
            continue
        w_dup = G[duplicate][neighbor].get('weight', 1.0)
        if G.has_edge(canonical, neighbor):
            G[canonical][neighbor]['weight'] = G[canonical][neighbor].get('weight', 0) + w_dup
        else:
            G.add_edge(canonical, neighbor, weight=w_dup)

    G.remove_node(duplicate)


# ─────────────────��────────────────────────────
# 5. EJECUTAR ELIMINACIÓN DE NODOS SIN SENTIDO
# ──────────────────────────────────────────────

# Primero eliminamos nodos sin sentido que NO sean canónicos de ningún merge
canonical_labels = set(MERGE_CLUSTERS.keys())
all_duplicate_labels = set()
for dups in MERGE_CLUSTERS.values():
    all_duplicate_labels.update(dups)

# Eliminar nodos sin sentido (que no sean canónicos ni necesarios)
removed_nonsense = 0
for node in list(nodes_to_remove):
    if node in G and node not in canonical_labels:
        # Si es un duplicado, primero hacer merge antes de eliminar
        if node in all_duplicate_labels:
            continue  # se manejará en el merge
        G.remove_node(node)
        removed_nonsense += 1

print(f"Nodos eliminados (sin sentido): {removed_nonsense}")


# ──────────────────────────────────────────────
# 6. EJECUTAR MERGES DE DUPLICADOS
# ──────────────────────────────────────────────

merged_count = 0
for canonical, duplicates in MERGE_CLUSTERS.items():
    if canonical not in G:
        # El canónico podría no existir; buscar si hay un duplicado que sí exista
        found = False
        for dup in duplicates:
            if dup in G:
                # Renombrar este nodo como canónico
                nx.relabel_nodes(G, {dup: canonical}, copy=False)
                duplicates = [d for d in duplicates if d != dup]
                found = True
                break
        if not found:
            continue

    for dup in duplicates:
        if dup in G and dup != canonical:
            merge_node(G, canonical, dup)
            merged_count += 1

print(f"Nodos duplicados fusionados: {merged_count}")


# ──────────────────────────────────────────────
# 7. SEGUNDA PASADA: ELIMINAR NODOS SIN SENTIDO RESTANTES
# ──────────────────────────────────────────────
removed_pass2 = 0
for node in list(G.nodes()):
    label = str(node).lower().strip()
    if label in EXPLICIT_REMOVE or is_nonsensical(label):
        G.remove_node(node)
        removed_pass2 += 1

print(f"Nodos eliminados (segunda pasada): {removed_pass2}")


# ──────────────────────────────────────────────
# 8. ELIMINAR AUTO-LAZOS RESIDUALES
# ──────────────────────────────────────────────
selfloops = list(nx.selfloop_edges(G))
G.remove_edges_from(selfloops)
print(f"Auto-lazos eliminados: {len(selfloops)}")


# ──────────────────────────────────────────────
# 9. ELIMINAR NODOS AISLADOS (sin aristas)
# ──────────────────────────────────────────────
isolated = list(nx.isolates(G))
G.remove_nodes_from(isolated)
print(f"Nodos aislados eliminados: {len(isolated)}")


# ──────────────────────────────────────────────
# 10. RENUMERAR IDs Y ESTABLECER LABELS
# ──────────────────────────────────────────────
# Creamos un nuevo grafo con IDs numéricos secuenciales
sorted_nodes = sorted(G.nodes())
node_mapping = {old: idx for idx, old in enumerate(sorted_nodes)}

G_clean = nx.Graph()
for idx, old_name in enumerate(sorted_nodes):
    G_clean.add_node(idx, id=idx, label=old_name)

for u, v, data in G.edges(data=True):
    new_u = node_mapping[u]
    new_v = node_mapping[v]
    G_clean.add_edge(new_u, new_v, **data)


# ──────────────────────────────────────────────
# 11. RESUMEN Y EXPORTACIÓN
# ──────────────────────────────────────────────
print(f"\n{'='*50}")
print(f"RESUMEN DE LIMPIEZA")
print(f"{'='*50}")
print(f"Grafo original:  1586 nodos, 2065 aristas")
print(f"Grafo limpio:    {G_clean.number_of_nodes()} nodos, {G_clean.number_of_edges()} aristas")
print(f"Nodos eliminados total: {1586 - G_clean.number_of_nodes()}")
print(f"{'='*50}")

nx.write_gml(G_clean, OUTPUT_PATH)
print(f"\nGrafo limpio exportado a: {OUTPUT_PATH}")

# Mostrar los 20 nodos con mayor grado ponderado
print("\nTop 20 nodos por grado ponderado:")
w_degree = dict(G_clean.degree(weight='weight'))
label_map = nx.get_node_attributes(G_clean, 'label')
top20 = sorted(w_degree.items(), key=lambda x: x[1], reverse=True)[:20]
for rank, (node, wd) in enumerate(top20, 1):
    print(f"  {rank:2d}. {label_map[node]:<35s} weighted_degree={wd:.1f}")