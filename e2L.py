#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import json
import os
from re import search
import requests
from lxml import html
import codecs

# Global variable
LANGUAGE = [
    [
        "Croatian",
        "HR",
        "Includes all species and non-species taxa recorded in Croatia. Thanks to Josip Turkalj for these translations.",
    ],
    [
        "Danish",
        "DA",
        "Includes all species and non-species taxa recorded in Denmark. Thanks to Nikolaj Thomsen for these translations.",
    ],
    [
        "German",
        "DE",
        "Includes all species and non-species taxa recorded in Germany. Thanks to Heiko Heerklotz, who provided these names in accord with the listing on Wikipedia. Thanks also to Wes Hochachka for some revisions to this list.",
    ],
    [
        "Finnish",
        "FI",
        "Erkki Pöytäniemi provided this translation for the names prevailing usage in Finland.",
    ],
    [
        "French",
        "FR",
        "All birds in the world. Denis Lepage, who runs the Avibase website",
        "which itself maintains multiple taxonomies and common name translations), provides these for the entire world with each taxonomic update. Many thanks to Denis for help with this and many other things related to our taxonomic updates.",
    ],
    [
        "French (Haiti)",
        "FR_HT",
        "Limited to species recorded in Haiti. Local French names.",
    ],
    [
        "English (Au.)",
        "EN_AU",
        "For species recorded in Australia only and differs from eBird/Clements in only limited cases. Our Eremaea eBird review and partner network provide Australian names, largely in accord with Christidis and Boles"
        " 2008 Systematics and Taxonomy of Australian Birds. Thanks in particular to Mat Gilfedder to providing the names and updates.",
    ],
    [
        "English (In.)",
        "EN_IN",
        "For species recorded in India only and differs from eBird/Clements in only limited cases. This list is maintained by our editor team in India (special thanks to Suhel Quader, Raman Kumar, and Praveen J), and matches the names in most common usage in India.",
    ],
    [
        "English (IOC)",
        "EN_IOC",
        "The International Ornithologists"
        " Committee (IOC) maintains a list of bird names and unique taxonomy, similar to eBird baseline Clements checklist. This name set is current for IOV v5.3 and eBird v2015. We provide a full set of translated names to match IOC, but note that this is a beta version for testing. This is the one case in eBird where an alternative taxonomy is supported. Note that the bird names are adjusted so that species in eBird that are not species for the IOC . All differences between IOC and eBird are documented at Avibase. For example, one can see that IOC splits Green-winged Teal (Anas carolinensis) from Eurasian Teal (Anas crecca), while eBird lumps them as a single species; when the IOC names are selected in eBird, the eBird version of Green-winged Teal (Anas crecca) will appear as Eurasian/Green-winged Teal, to represent the split. Special thanks to Denis Lepage (who manages the Avibase site) for his role in making this taxonomic matchup possible between the two taxonomies.",
    ],
    [
        "English (UE)",
        "EN_AE",
        "For Middle Eastern species only. This list is maintained by our United Arab Emirates reviewer, Tommy Pedersen, and matched names used by the Ornithological Society of the Middle East.  It is intended to be used for other Middle Eastern countries as well.",
    ],
    [
        "English (Mal.)",
        "EN_MY",
        'This listing uses the same name set that we use in eBird with one minor difference that all names using the American spelling "Gray" instead use the spelling "Grey". This includes Greylag and Greytail.',
    ],
    [
        "English (NZ)",
        "EN_NZ",
        "For species recorded in New Zealand only. Our New Zealand review team provides these names which match prevailing usage in New Zealand. Special thanks to Paul Scofield for providing these names and keeping them updated.",
    ],
    [
        "English (Ph)",
        "EN_PH",
        "In 2015, The Wild Bird Club of the Philippines (WBCP) officially endorsed eBird for its membership. This set of names follows the IOC names with a few exceptions that are maintained by the WBCP. Thanks especially to Christian Perez for his help with these names.",
    ],
    [
        "English (UK)",
        "EN_UK",
        "This list is maintained by our United Kingdom review team and mostly matches names used by the British Ornithological Union, as well as the BTO (British Trust for Ornithology). Many thanks to Stuart Fisher for the updates to these names.",
    ],
    [
        "Spanish",
        "ES",
        "This category uses some of the widespread Spanish names. In general, we recommend selecting one of the regionally-specific options below, which are more current. There is no official worldwide list of spanish bird names, so instead, each country has its own set of preferred names.",
    ],
    [
        "Spanish (Arg.)",
        "ES_AR",
        "Limited to species recorded in Argentina. Local Argentine Spanish names. Thanks to our eBird Argentina team, with special thanks to Nacho Areta for help with the names.",
    ],
    [
        "Spanish (Chile)",
        "ES_CL",
        "Limited to species recorded in Chile. Local Chilean Spanish names. Thanks to our Chile eBird team, with special thanks to Fabrice Schmitt for coordinating this list of names.",
    ],
    [
        "Spanish (Cuba)",
        "ES_CU",
        "Limited to species recorded in Cuba. Local Cuban Spanish names.",
    ],
    [
        "Spanish (DR)",
        "ES_DO",
        "Limited to species recorded in the Dominican Republic. Local Dominican Spanish names.",
    ],
    [
        "Spanish (Spain)",
        "ES_ES",
        "Limited to species recorded in Spain. Official names for birds in Spain provided courtesy of Whitehawk Birding, with special thanks to Yeray Seminario and Fernando Enrique.",
    ],
    [
        "Spanish (Mexico)",
        "ES_MX",
        "Limited to species recorded in Mexico. Local Mexican Spanish names. Thanks to our aVerAves team, and especially to Humberto Berlanga and Hector Gomez de Silva for providing these names.",
    ],
    [
        "Spanish (Panama)",
        "ES_PA",
        "Limited to species recorded in Panama. Local names in usage in Panama.",
    ],
    [
        "Spanish (Puerto Rico)",
        "ES_PR",
        "Limited to species recorded in Puerto Rico. Local Puerto Rican Spanish names. Thanks to our Puerto Rico eBird team.",
    ],
    [
        "Spanish (Venezuela)",
        "ES_VE",
        "Limited to species recorded in Venezuela; subspecies will generally appear in English. Thanks to our Venezuela editors, Jhonathan Miranda and Beto Matheus for these translations.",
    ],
    [
        "Haitian (Haiti)",
        "HT_HT",
        "Limited to species recorded in Haiti. Local Haitian names.",
    ],
    [
        "Indonesian",
        "ID",
        "Limited to species recorded in Indonesia. These names were provided by Mat Gilfedder.",
    ],
    [
        "Icelandic",
        "IS_IS",
        "Limited to species recorded in Iceland. This list is maintained by our Iceland review team. Many thanks to Yann Kolbeinsson for the updates to these names.",
    ],
    [
        "Latvian",
        "LV",
        "Limited to species recorded in Latvia. Thanks to Pēteris Daknis for his help compiling these names.",
    ],
    [
        "Norwegian",
        "NO",
        "Limited to species and non-species taxa recorded in Norway. Thanks to Harald Steensland for compiling these names.",
    ],
    [
        "Portuguese (Brasil)",
        "PT_BR",
        "Limited to species recorded in Brasil. This list follows the species recognized by the CBRO, the official committee for taxonomy and nomenclature in Brasil. This version of the names matched the CBRO 2015 taxonomy and eBird v2015. Since the Clements Checklist largely follows SACC, these names do not match in all cases. When this setting is selected, the Portugal names will show for species that do not have a Brasil name.",
    ],
    [
        "Portuguese (Portugal)",
        "PT_PT",
        "Includes all species reported in Portugal and many other species from the Western Palearctic. These names are provided by Pedro Fernandes and match prevailing usage.",
    ],
    [
        "Russian",
        "RU",
        "Includes all species reported in Russia and Ukraine. Some species that are split are not translated at the species level for eBird yet. Thanks to Sergey Glebov and Iurii Strus for these names.",
    ],
    [
        "Serbian",
        "SR",
        "Limited to species recorded in Serbia. Thanks to Zheljko Stanimirovic for providing these names.",
    ],
    [
        "Turkish",
        "TR",
        "Includes all species reported in Turkey. Kerem Ali Boyla has provided these names based on those in prevailing usage in Turkey, including the official taxonomy for Kuşbank.",
    ],
    [
        "Ukrainian",
        "UK",
        "Includes all species and non-species taxa recorded in Ukraine. Thanks to Iurii Strus for these names.",
    ],
    [
        "Chinese",
        "ZH",
        "Currently includes only species recorded in Taiwan in Mandarin. Matches prevailing usage for the area. Thanks to Scott Lin for providing these names and updates to them.",
    ],
    [
        "Chinese (Simple)",
        "ZH_SIM",
        "Includes species recorded in China. Thanks to Yuetao Zhong and Tong Mu for providing these names. The IOC names are used for species that do not occur in China.",
    ],
    ["Latin", "LA", "latin name"],
    ["English", "EN", "english"],
]

CATEGORIE = [
    [
        "spuh",
        " Genus or identification at broad level -- e.g., duck sp., dabbling duck sp.",
    ],
    ["slash", "Identification to Species-pair e.g., American Black Duck/Mallard)"],
    ["species", "e.g., Mallard"],
    [
        "issf",
        "or Identifiable Sub-specific Group. Identifiable subspecies or group of subspecies, e.g., Mallard (Mexican)",
    ],
    [
        "hybrid",
        "Hybrid between two species, e.g., American Black Duck x Mallard (hybrid)",
    ],
    [
        "intergrade",
        "Hybrid between two ISSF (subspecies or subspecies groups), e.g., Mallard (Mexican intergrade)",
    ],
    [
        "domestic",
        "Distinctly-plumaged domesticated varieties that may be free-flying (these do not count on personal lists) e.g., Mallard (Domestic type)",
    ],
    [
        "form",
        "Miscellaneous other taxa, including recently-described species yet to be accepted or distinctive forms that are not universally accepted (Red-tailed Hawk (Northern), Upland Goose (Bar-breasted))",
    ],
]


def auth(usr, pwd):
    print("request sessionID from login...")
    # create a session to keep cookies
    s = requests.Session()
    # login url, I don't know why you need the part after ? but it doesn't work without
    urlLogin = "https://secure.birds.cornell.edu/cassso/login"
    r = s.get(urlLogin)
    # search the value of the hidden input name=lt (link to cookies or login I guess)
    # matches = search('name="execution" value="(.*)"', r.text)
    # Extract the `execution` value from the form
    execution_match = search(r'name="execution" value="(.*?)"', r.text)
    if not execution_match:
        raise ValueError("Execution value not found in the login form.")
    execution_value = execution_match.group(1)
    # create the data to include in the form
    form_data = [
        ("_eventId", "submit"),
        ("execution", execution_value),
        ("password", pwd),
        ("username", usr),
    ]
    # post a login to get the session ID
    s.post(urlLogin, data=form_data)
    # check that the session ID is return
    sessionID = requests.utils.dict_from_cookiejar(s.cookies).get("JSESSIONID")
    if len(sessionID) == 0:
        raise ValueError("Authentification failed...")
    else:
        print("...login succesfull")
    return s


def bird_creator(s, code_loc, lang, cat, byear, eyear, bmonth, emonth):
    poss_lang = [l[1] for l in LANGUAGE]
    poss_cat = [c[0] for c in CATEGORIE]
    if isinstance(lang, list):
        lang = [l.upper() for l in lang]
        assert all([l in poss_lang for l in lang]), (
            "One or several language asked ( %s ) are not available." % lang
        )
    else:
        lang = lang.upper()
        assert lang in poss_lang, (
            "One or several language asked ( %s ) are not available." % lang
        )

    # current_year = datetime.datetime.now().year
    assert all([c in poss_cat for c in cat]) or (cat in poss_cat), (
        "One or several categorie asked ( %s ) are not available." % cat
    )
    assert byear <= eyear, "byear (%d) needs to be before eyear (%d)" % (byear, byear)
    assert bmonth <= emonth, "bmonth (%d) needs to be before emonth (%d)" % (
        bmonth,
        bmonth,
    )
    # assert byear > 0 and byear <= current_year and eyear > 0 and eyear <= current_year, 'month need to be comprise between 0 and this year'
    assert (
        bmonth > 0 and bmonth < 13 and emonth > 0 and emonth < 13
    ), "month need to be comprise between 1 and 12"

    bc_bird_list, info = load_barchart(s, code_loc, byear, eyear, bmonth, emonth)
    taxa_bird_list = load_taxa(lang, cat)
    info["lang"] = lang
    info["lang"].append("LA")

    # Replace
    samples_size_month_0 = [1 if x == 0 else x for x in info["samples_size"]["month"]]
    samples_size_season_0 = [1 if x == 0 else x for x in info["samples_size"]["season"]]

    bird_list = []
    for bc_bird in bc_bird_list:
        for taxa_bird in taxa_bird_list:
            if taxa_bird["sciName"] == bc_bird["sciName"]:
                bird = taxa_bird
                bird["freq"] = {}
                bird["freq"]["week"] = bc_bird["freq"]
                bird_nb_week = list(
                    map(
                        lambda x, y: x * y,
                        bird["freq"]["week"],
                        info["samples_size"]["week"],
                    )
                )
                bird_nb_month, bird_nb_season, bird_nb_year = week_to_else(bird_nb_week)
                bird["freq"]["month"] = list(
                    map(lambda x, y: x / y, bird_nb_month, samples_size_month_0)
                )
                bird["freq"]["season"] = list(
                    map(lambda x, y: x / y, bird_nb_season, samples_size_season_0)
                )
                bird["freq"]["year"] = bird_nb_year / info["samples_size"]["year"]
                # print(info['samples_size']['year'])
                bird["status"] = []
                bird_list.append(bird)

    return (info, sorted(bird_list, key=lambda k: k["taxonOrder"]))


def merge_bird(bird_list, info, bird_list2, info2):

    # Define the sample size with replaced 0 to 1
    samples_size_week_01 = [1 if x == 0 else x for x in info["samples_size"]["week"]]
    samples_size_week_02 = [1 if x == 0 else x for x in info2["samples_size"]["week"]]
    samples_size_month_01 = [1 if x == 0 else x for x in info["samples_size"]["month"]]
    samples_size_month_02 = [1 if x == 0 else x for x in info2["samples_size"]["month"]]
    samples_size_season_01 = [
        1 if x == 0 else x for x in info["samples_size"]["season"]
    ]
    samples_size_season_02 = [
        1 if x == 0 else x for x in info2["samples_size"]["season"]
    ]

    # merge existing taxo between the two list
    for bird in bird_list:
        bird_match = next(
            (
                bird2
                for bird2 in bird_list2
                if bird2["speciesCode"] == bird["speciesCode"]
            ),
            None,
        )
        if bird_match:
            bird["freq"]["week"] = list(
                map(
                    lambda x1, w1, x2, w2: (x1 * w1 + x2 * w2) / (w1 + w2),
                    bird["freq"]["week"],
                    samples_size_week_01,
                    bird_match["freq"]["week"],
                    samples_size_week_02,
                )
            )
            bird["freq"]["month"] = list(
                map(
                    lambda x1, w1, x2, w2: (x1 * w1 + x2 * w2) / (w1 + w2),
                    bird["freq"]["month"],
                    samples_size_month_01,
                    bird_match["freq"]["month"],
                    samples_size_month_02,
                )
            )
            bird["freq"]["season"] = list(
                map(
                    lambda x1, w1, x2, w2: (x1 * w1 + x2 * w2) / (w1 + w2),
                    bird["freq"]["season"],
                    samples_size_season_01,
                    bird_match["freq"]["season"],
                    samples_size_season_02,
                )
            )
            bird["freq"]["year"] = (
                bird["freq"]["year"] * info["samples_size"]["year"]
                + bird_match["freq"]["year"] * info2["samples_size"]["year"]
            ) / (info["samples_size"]["year"] + info2["samples_size"]["year"])

    bird_speciesCode = [bird["speciesCode"] for bird in bird_list]
    # add new taxt
    for bird2 in bird_list2:
        if not bird2["speciesCode"] in bird_speciesCode:
            bird_list.append(bird2)

    # Combine info
    info["samples_size"]["week"] = list(
        map(
            lambda x1, x2: x1 + x2,
            info["samples_size"]["week"],
            info2["samples_size"]["week"],
        )
    )
    info["samples_size"]["season"] = list(
        map(
            lambda x1, x2: x1 + x2,
            info["samples_size"]["season"],
            info2["samples_size"]["season"],
        )
    )
    info["samples_size"]["month"] = list(
        map(
            lambda x1, x2: x1 + x2,
            info["samples_size"]["month"],
            info2["samples_size"]["month"],
        )
    )
    info["samples_size"]["year"] = (
        info["samples_size"]["year"] + info["samples_size"]["year"]
    )

    info["NbTaxa"] = len([bird["speciesCode"] for bird in bird_list])


def load_barchart(s, code_loc, byear, eyear, bmonth, emonth):

    url = "http://ebird.org/barchartData?r={code_loc}&bmo={bmonth}&emo={emonth}&byr={byear}&eyr={eyear}&fmt=tsv".format(
        code_loc=code_loc, byear=byear, eyear=eyear, bmonth=bmonth, emonth=emonth
    )

    print("Load barchart data from " + url)
    r = s.get(url, stream=True)

    f = open("_barchart.tsv", "wb")
    f.write(r.content)
    f.close()

    # lines = codecs.open('_barchart.tsv','r', encoding='utf8', errors='replace')

    bc_bird_list = []
    info = {}
    for l in r.iter_lines():
        line = l.decode("utf8").strip()
        if not line:
            pass
        elif "Frequency of observations in the selected location(s).:" in line:
            pass
        elif "Number of taxa" in line:
            # Line with the number of taxa in the list
            info["NbTaxa"] = int(line.replace("Number of taxa: ", ""))
        elif "Jan\t\t\t\tFeb" in line:
            pass
        elif "Sample Size" in line:
            info["samples_size"] = {}
            info["samples_size"]["week"] = [
                int(float(i)) for i in line.replace("Sample Size:", "").split()
            ]
            assert (
                len(info["samples_size"]["week"]) > 0
            ), "Empty Barchart! Check the barchart link above, maybe there is not data for your query or the query is wrong"
            (
                info["samples_size"]["month"],
                info["samples_size"]["season"],
                info["samples_size"]["year"],
            ) = week_to_else(info["samples_size"]["week"])
            # info['samples_size']['month'] = [i*4 for i in info['samples_size']['month']];
            # info['samples_size']['season'] = [i*12 for i in info['samples_size']['season']];
            # info['samples_size']['year'] = info['samples_size']['year']*48;
        else:
            name, lineF = line.split("\t", 1)
            sciName = search('<em class="sci">(.*)</em>', name)[1]
            # name_la,line = line.split('\t',1)
            freq = [float(i) for i in lineF.split()]
            assert len(freq) == 48, "Number of bird frequency is not equal to 48"
            bc_bird_list.append({"sciName": sciName, "freq": freq})
    return (bc_bird_list, info)


def load_taxa(lang, cat):
    # cat = 'domestic,form,hybrid,intergrade,issf,slash,species,spuh'
    # local en,en_US,de,en_AE,en_AU,en_IN,en_NZ,en_UK,en_ZA,es,es_AR,es_CL,es_CU, es_DO,es_ES,es_MX,es_PA,es_PR,fi,fr,fr_HT,ht_HT,in,is,pt_BR,pt_PT,tr,zh
    # https://support.ebird.org/en/support/solutions/articles/48000804865-bird-names-in-ebird

    print("Load taxonomy for " + ",".join(lang))

    taxaLang = dict()
    for locale in lang:
        # define location of the file
        filename = "assets/taxonomy-" + locale + ".json"

        # if assets does not exists, create i
        if not (os.path.exists("assets/")):
            os.makedirs("assets/")

        # if the file doesn't exist, download it
        if not os.path.exists(filename):
            response = requests.get(
                "https://api.ebird.org/v2/ref/taxonomy/ebird?fmt=json&locale=" + locale
            )
            response.raise_for_status()  # ensure we notice bad responses
            with open(filename, "w") as file:
                file.write(response.text)

        # read the json file
        with open(filename, "r") as file:
            taxaLang[locale] = list(
                filter(lambda x: x["category"] in cat, json.load(file))
            )

    taxa = taxaLang[lang[0]]

    for id, t in enumerate(taxa):
        t["lang"] = {}
        t["lang"]["LA"] = t["sciName"]
        for locale in lang:
            t["lang"][locale] = taxaLang[locale][id]["comName"]

    return taxa


def statusInList(status, bird_list, session, target_loc, target_time):
    url = "https://ebird.org/lifelist/{target_loc}/?time={target_time}".format(
        target_loc=target_loc, target_time=target_time
    )

    print("Load target data from " + url)
    r = session.get(url)
    tree = html.fromstring(r.content)

    myList = list(
        map(
            lambda res: res.cssselect(".Heading-sub--sci")[0].text_content(),
            tree.cssselect(".Observation-species .Heading"),
        )
    )

    for bird in bird_list:
        if not bird["sciName"] in myList:
            bird["status"].append(status)

    return bird_list


def statusInTarget(
    status, bird_list, session, code_loc, target_loc, target_time, bmonth, emonth
):
    url = "http://ebird.org/ebird/targets?r1={code_loc}&r2={target_loc}&t2={target_time}&bmo={bmonth}&emo={emonth}".format(
        code_loc=code_loc,
        target_loc=target_loc,
        target_time=target_time,
        bmonth=bmonth,
        emonth=emonth,
    )

    print("Load target data from " + url)
    r = session.get(url)
    tree = html.fromstring(r.content)

    target = list(
        map(
            lambda res: res.cssselect(".ResultsStats-title a em")[0].text_content(),
            tree.find_class("ResultsStats"),
        )
    )

    for bird in bird_list:
        if bird["sciName"] in target:
            bird["status"].append(status)

    return bird_list


def statusAvibase(status, bird_list, code_loc):
    url = "https://avibase.bsc-eoc.org/checklist.jsp?region={code_loc}&list=clements".format(
        code_loc=code_loc
    )
    print("Load endemic data from " + url)
    r = requests.get(url)
    tree = html.fromstring(r.content)

    endemic = []
    for res in tree.find_class("highlight1"):
        if "Endemic" in res.text_content():
            endemic.append(res.cssselect("i")[0].text_content())

    introduce = []
    for res in tree.find_class("highlight1"):
        if "Introduced" in res.text_content():
            introduce.append(res.cssselect("i")[0].text_content())

    for bird in bird_list:
        if bird["sciName"] in endemic:
            bird["status"].append(status[0])
        if bird["sciName"] in introduce:
            bird["status"].append(status[1])

    return bird_list


def week_to_else(week):
    t_m = []
    month = []
    for i in range(0, len(week)):
        t_m.append(week[i])
        if i % 4 == 3:
            month.append(sum(b for b in t_m))
            t_m = []
    assert len(month) == 12, "Month frequency is not equal to 12"
    # Season
    season = []
    season.append(sum(b for b in month[2:5]))
    season.append(sum(b for b in month[5:8]))
    season.append(sum(b for b in month[8:11]))
    season.append(sum(b for b in month[0:2] + [month[11]]))
    # Year
    year = sum(b for b in week)
    return month, season, year


def write_to_latex(
    projname,
    filename,
    bird_list,
    col,
    condition_tableau,
    condition_rare,
    family,
    format,
    spacing,
    info,
):
    family_current = ""

    # if latex does not exists, create i
    if not (os.path.exists("latex/")):
        os.makedirs("latex/")

    # Start Writing
    f = codecs.open("latex/" + filename + ".tex", "w+", encoding="utf8")

    # Import preformatted text
    f2 = open("assets/templateLaTeX.tex", "r")
    for line in f2:
        if "newcommand{\maxnum}" in line:
            line = line[:-1] + "100.00}\n"
        if "newcommand{\samples_size}" in line:
            line = (
                line[:-1]
                + str(round(info["samples_size"]["year"]))
                + " checklists ("
                + str(info["nb_taxa"])
                + " differents species)} "
            )
        elif "_condition_" in line:
            continue
            # line = condition_tableau[0]+'\n'
        elif "_format_" in line:
            line = "\\usepackage[" + format + "]{geometry}\n"
        elif "_xentrystretch_" in line:
            line = "\\xentrystretch{" + "-0.1" + "}\n"
        elif "_linespacing_" in line:
            line = "\\renewcommand{\\arraystretch}{" + spacing + "}\n"
        elif "_projectname_" in line:
            line = "\\LARGE{" + projname + "}\\\\"
        elif "_noteline_" in line:
            line = 3 * "\\newnoteline\n"
        elif "begin{xtabular*" in line:
            line = line[:-1]
            for c in col:  # write column width
                line += c.wid
            line += "}\n"
        elif "_columntitle_" in line:
            line = ""
            for c in col[:-1]:  # write title
                line += "\\textsc{ \\large{" + c.title + "}} \t & "
            line += "\\textsc{ \\large{ " + col[-1].title + "}}\\\\"
        elif "_content_" in line:
            line = ""
            for bird in bird_list:  # write Content
                # condition to display or not a bird
                if eval(condition_tableau[1]):
                    if (
                        bird["familyComName"] != family_current and family
                    ):  # family name
                        f.write(
                            "\\multicolumn{"
                            + str(len(col))
                            + "}{c}{\\textbf{"
                            + bird["familyComName"]
                            + "}} \\\\ \n"
                        )
                        f.write("\\hline\n")
                        family_current = bird["familyComName"]
                    for c in col[:-1]:
                        # Content of the cell
                        f.write(c.get_content(bird) + " \t & ")
                    f.write(col[-1].get_content(bird) + " \\\\ \n")  # end of line
        elif "_rare_" in line:
            line = ""
            # Table Rare
            if "onecolumn" in format:
                n_rare_col = 3
            else:
                n_rare_col = 2
            col_r = TableInput(info, "lang", info["lang"][1])
            bird_list_r = []
            for bird in bird_list:
                if eval(condition_rare[1]):
                    bird_list_r.append(col_r.get_content(bird))

            u = len(bird_list_r)

            if u != 0:  # check if there are rare bird
                while u - n_rare_col * round(u / n_rare_col) != 0:
                    bird_list_r.append("\\underline{\\hfill}")
                    u = len(bird_list_r)
                c = round(u / n_rare_col)
                f.write("\\begin{xtabular*}{\\linewidth}{@{\\extracolsep{\\fill}}")
                for x in range(0, n_rare_col):
                    f.write("cl")
                f.write("} \n")
                f.write("\\toprule\n\\\\\n")
                f.write(
                    "\\multicolumn{"
                    + str(2 * n_rare_col)
                    + "}{c}{\\textsc{ \\Large{Rare"
                    + condition_rare[0]
                    + "}}} \\\\ \n"
                )
                f.write("\\\\\n\\midrule\n")
                for cc in range(0, c):
                    for c_r in range(0, n_rare_col - 1):
                        f.write(
                            "\\underline{\\hspace{3ex}} \t &"
                            + bird_list_r[cc + c * c_r]
                            + " \t &"
                        )
                    f.write(
                        "\\underline{\\hspace{3ex}} \t &"
                        + bird_list_r[cc + c * (n_rare_col - 1)]
                        + " \\\\ \n"
                    )
                f.write("\\bottomrule\n")
                f.write("\\end{xtabular*} ")
        f.write(line)
    f2.close()


def num2str(num):
    if num > 1000000:
        return str(round(num / 1000000)) + "M"
    elif num > 1000:
        return str(round(num / 1000)) + "K"
    else:
        return str(round(num))


# Class
class TableInput:
    def __init__(self, info, type, option1=None, option2=None, option3=None):
        self.type = type
        self.title = None
        self.wid = None
        self.option1 = option1
        self.option2 = option2
        self.option3 = option3
        if self.type == "lang":
            assert (
                self.option1 in info["lang"]
            ), "language requested not available in barchart data."
            self.wid = "l"
            idx = [l[1] for l in LANGUAGE].index(self.option1.upper())
            self.title = LANGUAGE[idx][0]
        elif self.type == "freq":
            self.wid = "c"
            if self.option1 == "year":
                self.title = (
                    "Y"
                    + "\\footnotesize{ ("
                    + num2str(info["samples_size"]["year"])
                    + ")} "
                )
            elif self.option1 == "season":
                self.option2 = int(option2)
                # ['Spring','Summer','Fall','Winter']
                season = ["Sp", "Sm", "F", "W"]
                self.title = (
                    season[self.option2]
                    + "\\footnotesize{ ("
                    + num2str(info["samples_size"]["season"][self.option2])
                    + ")} "
                )
            elif self.option1 == "month":
                month = [
                    "Jan.",
                    "Feb.",
                    "Mar.",
                    "Apr.",
                    "May",
                    "June",
                    "Jul",
                    "Aug",
                    "Sept.",
                    "Oct.",
                    "Nov.",
                    "Dec.",
                ]
                self.option2 = int(option2)
                # +'\\footnotesize{ (' +str(round(info['samples_size']['month'][self.option2])) +')} '
                self.title = month[self.option2]
            elif self.option1 == "week":
                self.option2 = int(option2)
                # +'\\footnotesize{ (' +str(round(info['samples_size']['week'][self.option2])) +')} '
                self.title = "Week " + str(self.option2)
            else:
                raise ValueError(self.option1)
        elif self.type == "note":
            self.wid = "c"
            self.title = "Note"
        elif self.type == "line":
            self.option1 = int(self.option1)
            self.wid = "c"
            alphabet = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
            self.title = "\\normalsize{" + self.get_content(None) + "}"
        elif self.type == "checkbox":
            self.wid = "c"
            self.type = "checkbox"  # put line-like title
            self.option1 = int(self.option1)
            self.title = "\\normalsize{" + self.get_content(None) + "}"
            self.type = "checkbox"
        else:
            raise ValueError(self.type)

    def __str__(self):
        return str(self.title)

    def get_content(self, bird):
        if self.type == "lang":
            c = bird["lang"][self.option1]
            if self.option2 is not None:
                for status in self.option2:
                    if status[0] in bird["status"]:
                        if "bold" == status[1]:
                            c = "\\textbf{" + c + "}"
                        elif "italic" == status[1]:
                            c = "\\emph{" + c + "}"
                        elif "underline" == status[1]:
                            c = "\\underline{" + c + "}"
                        elif "color" in status[1]:
                            c = "\\textcolor{" + status[1][6:] + "}{" + c + "}"
                        elif "sym" in status[1]:
                            c = c + status[1][4:5]
            return c
        elif self.type == "freq":
            if self.option1 == "year":
                return "\\databar{" + "{:.1f}".format(bird["freq"]["year"] * 100) + "}"
            elif self.option1 == "season":
                return (
                    "\\databar{"
                    + "{:.1f}".format(bird["freq"]["season"][self.option2] * 100)
                    + "}"
                )
            elif self.option1 == "month":
                return (
                    "\\databar{"
                    + "{:.1f}".format(bird["freq"]["month"][self.option2] * 100)
                    + "}"
                )
            elif self.option1 == "week":
                return (
                    "\\databar{"
                    + "{:.1f}".format(bird["freq"]["week"][self.option2] * 100)
                    + "}"
                )
        elif self.type == "note":
            if not self.option1:
                self.option1 = "4cm"
            return "\\dotuline{\\hspace{" + self.option1 + "}}"
        elif self.type == "line":
            if not self.option1:
                self.option1 = 3
            if not self.option2:
                self.option2 = "3ex"
            return int(self.option1) * (
                "\\underline{\\hspace{" + self.option2 + "}}\\hspace{1ex}"
            )
        elif self.type == "checkbox":
            if not self.option1:
                self.option1 = 3
            return self.option1 * "$\\square$\\hspace{1ex} "
