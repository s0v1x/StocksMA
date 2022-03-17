import random

import requests

companies = {
    "ADH": "Douja Promotion Groupe Addoha",
    "ADI": "Alliances Developpement Immobilier S.A.",
    "AFI": "Afric Industries S.A.",
    "AFM": "AFMA S.A.",
    "AGM": "Agma S.A.",
    "ALM": "Aluminium du Maroc",
    "ARD": "Aradei Capital",
    "ATH": "Auto Hall S.A.",
    "ATL": "AtlantaSanad",
    "ATW": "Attijariwafa Bank",
    "BAL": "Societe Immobiliere Balima",
    "BCI": "Banque Marocaine pour le Commerce et l'Industrie ",
    "BCP": "Banque Centrale Populaire S.A.",
    "BOA": "Bank of Africa",
    "CDA": "Centrale Danone",
    "CDM": "Credit du Maroc",
    "CIH": "Credit Immobilier et Hotelier",
    "CMA": "Les Ciments du Maroc",
    "CMT": "Compagnie Miniere de Touissit S.A.",
    "COL": "Colorado S.A.",
    "CRS": "Cartier Saada S.A.",
    "CSR": "Cosumar",
    "CTM": "Compagnie de Transports au Maroc S.A.",
    "DHO": "Delta Holding S.A.",
    "DLM": "Delattre Levivier Maroc S.A.",
    "DWY": "Disway S.A.",
    "EQD": "Societe d'Equipement Domestique et Menager S.A. ",
    "FBR": "Fenie Brossette S.A.",
    "GAZ": "Afriquia Gaz",
    "HPS": "Hightech Payment Systems S.A.",
    "IAM": "Maroc Telecom",
    "IBC": "IB Maroc.com S.A.",
    "IMO": "Immorente Invest S.A.",
    "INV": "Involys",
    "JET": "Jet Contractors S.A.",
    "LBV": "Label Vie",
    "LES": "Lesieur Cristal S.A.",
    "LHM": "LafargeHolcim Maroc",
    "M2M": "m2m group S.A.",
    "MAB": "Maghrebail",
    "MDP": "Med Paper S.A.",
    "MIC": "Microdata S.A.R.L.",
    "MLE": "Maroc Leasing S.A.",
    "MNG": "Managem",
    "MOX": "Maghreb Oxygene",
    "MSA": "SODEP-Marsa Maroc",
    "MUT": "Mutandis SCA",
    "NEJ": "Auto Nejma Maroc S.A.",
    "NKL": "Ennakl Automobiles",
    "PRO": "Promopharm S.A.",
    "RDS": "Residences Dar Saada S.A.",
    "RIS": "Risma",
    "S2M": "Societe Maghrebine de Monetique",
    "SAH": "Saham Assurance S.A.",
    "SBM": "Societe des Boissons du Maroc",
    "SID": "Societe Nationale de Siderurgie S.A.",
    "SLF": "Salafin",
    "SMI": "Societe Metallurgique d'Imiter ",
    "SNA": "Stokvis Nord Afrique",
    "SNP": "Societe Nationale d'Electrolyse et de Petrochimie ",
    "SOT": "Sothema",
    "SRM": "Societe de Realisations Mecaniques",
    "STR": "STROC Industrie S.A.",
    "TGC": "Travaux Generaux de Construction de Casablanca S.A.",
    "TIM": "TIMAR S.A.",
    "TMA": "TotalEnergies Marketing Maroc",
    "TQM": "Taqa Morocco",
    "WAA": "Wafa Assurance S.A.",
    "ZDJ": "Zellidja S.A.",
}


def rand_agent(fname: str) -> str:
    lines = open(fname).read().splitlines()
    return random.choice(lines)


def remove_duplicates(string: str) -> str:
    words = string.split()
    return " ".join(sorted(set(words), key=words.index))


def check_company(company: str) -> None:
    if not isinstance(company, str) or not company.upper() in companies.keys():
        raise Exception(
            "Ticker {company} is not found, use get_companies()".format(company=company)
        )


def request(url: str) -> requests.models.Response:
    headers = {"User-Agent": rand_agent("src/StocksMA/user-agents.txt")}
    request_data = requests.get(url, headers=headers)
    return request_data
