from typing import Dict, Any

# Human-facing weapon information database.
# Descriptions are intentionally neutral and educational.
weapon_database: Dict[str, Dict[str, Any]] = {
    "AK-47": {
        "type": "Assault Rifle",
        "origin": "Soviet Union",
        "year": 1947,
        "description": (
            "The AK-47 (Avtomat Kalashnikova) is a gas-operated, "
            "selective-fire rifle that became widely known in the mid-20th century. "
            "It is recognized for its simple construction and tolerance of harsh environments. "
            "The design emphasizes reliability over precision at extended ranges. "
            "Its operating mechanism and materials allow continued function with limited maintenance. "
            "The rifle has influenced numerous derivative designs across different regions."
        ),
        "usage": (
            "Commonly issued to military forces and non-state actors in many countries, "
            "typically in infantry roles where robustness and ease of training are important."
        ),
        "sound_key": "ak47",
    },
    "INSAS Rifle": {
        "type": "Assault Rifle",
        "origin": "India",
        "year": 1998,
        "description": (
            "The INSAS (Indian Small Arms System) rifle family was developed as a standard-issue "
            "5.56×45mm NATO platform. "
            "It incorporates features seen in earlier global rifle designs while adapting to local requirements. "
            "The system was intended to modernize small arms within the Indian armed forces. "
            "Its design emphasizes controllable automatic fire and compatibility with standard accessories. "
            "Subsequent variants have addressed reliability and ergonomics based on field feedback."
        ),
        "usage": (
            "Fielded primarily by Indian military and certain law-enforcement units in conventional infantry roles."
        ),
        "sound_key": "insas",
    },
    ".22 Rifle": {
        "type": "Rifle (.22 caliber)",
        "origin": "Various (multiple manufacturers)",
        "year": 1900,
        "description": (
            "The .22 caliber rifle category covers a wide range of small-bore rifles. "
            "These platforms generally fire rimfire cartridges with comparatively modest recoil. "
            "They are often designed with simple bolt-action or semi-automatic mechanisms. "
            "The low power and manageable handling characteristics make them accessible to a wide user base. "
            "Many models prioritize basic marksmanship and cost-effective operation. "
            "Design details vary significantly across manufacturers and regions."
        ),
        "usage": (
            "Predominantly used for training, sport shooting, and controlled applications where low recoil and "
            "modest range are suitable."
        ),
        "sound_key": "pistol",
    },
    "M16": {
        "type": "Assault Rifle",
        "origin": "United States",
        "year": 1964,
        "description": (
            "The M16 family is a lightweight, 5.56×45mm NATO, gas-operated rifle platform. "
            "It makes extensive use of aluminum alloys and composite materials to reduce weight. "
            "The design employs a rotating bolt and direct gas impingement or gas expansion system. "
            "Modern variants integrate modular rails for optics and accessories. "
            "It has served as a baseline pattern for numerous derivative designs worldwide. "
            "Over time, improvements have focused on ergonomics, reliability, and adaptability."
        ),
        "usage": (
            "Widely deployed by military and some law-enforcement forces, typically in infantry and security roles."
        ),
        "sound_key": "pistol",
    },
    "Glock Pistol": {
        "type": "Handgun",
        "origin": "Austria",
        "year": 1982,
        "description": (
            "Glock pistols are polymer-framed, striker-fired handguns produced in various calibers. "
            "They are known for simplified internal mechanisms and relatively low part counts. "
            "The design emphasizes consistent trigger characteristics and corrosion resistance. "
            "Modularity across models allows familiar handling between different configurations. "
            "Their construction has influenced the development of many later service pistols. "
            "Variants incorporate different sizes and capacities for specific operational needs."
        ),
        "usage": (
            "Commonly adopted by law-enforcement and security agencies, as well as military units requiring "
            "standardized sidearms."
        ),
        "sound_key": "pistol",
    },
    "Revolver": {
        "type": "Handgun",
        "origin": "Various (multiple manufacturers)",
        "year": 1860,
        "description": (
            "Revolvers use a rotating cylinder to align individual chambers with the barrel. "
            "The mechanism typically relies on either single-action or double-action trigger systems. "
            "Their mechanical design allows operation without detachable magazines. "
            "Many models prioritize reliability, with fewer controls than modern semi-automatic pistols. "
            "They have been produced in a wide variety of calibers and frame sizes. "
            "Their silhouette is easily recognizable in historical and contemporary contexts."
        ),
        "usage": (
            "Historically used by military and law-enforcement entities, with contemporary presence in certain "
            "specialized roles and civilian sporting contexts where allowed."
        ),
        "sound_key": "pistol",
    },
    "Shotgun": {
        "type": "Shotgun",
        "origin": "Various (multiple manufacturers)",
        "year": 1880,
        "description": (
            "Shotguns are smoothbore firearms designed to fire multiple projectiles or specialized slugs. "
            "They may employ pump-action, break-action, or semi-automatic mechanisms. "
            "The platform is characterized by short-range performance and wide pattern spread with shot loads. "
            "Barrel length, choke, and ammunition selection affect coverage and impact characteristics. "
            "They have evolved to include modular stocks, rails, and sighting systems. "
            "Different configurations exist for sporting, security, and utility roles."
        ),
        "usage": (
            "Used by law-enforcement, military units, and sport shooters in roles requiring short-range, "
            "high-dispersion capability or specific breaching tasks."
        ),
        "sound_key": "pistol",
    },
    "Sniper Rifle": {
        "type": "Precision Rifle",
        "origin": "Various (multiple manufacturers)",
        "year": 1930,
        "description": (
            "Sniper rifles are precision-oriented rifles optimized for accuracy at extended ranges. "
            "They often feature high-quality barrels, adjustable stocks, and optical sights. "
            "Many designs use bolt-action mechanisms to prioritize consistency and rigidity. "
            "Dedicated calibers balance trajectory, recoil, and terminal characteristics for specific roles. "
            "Supporting accessories such as bipods and rangefinding optics are commonly integrated. "
            "These systems are typically paired with specialized training in observation and ballistic estimation."
        ),
        "usage": (
            "Assigned to designated marksmen or specialized military and law-enforcement personnel for "
            "long-distance observation and precision engagement where legally authorized."
        ),
        "sound_key": "pistol",
    },
    "Grenade": {
        "type": "Explosive (Hand-thrown)",
        "origin": "Various (multiple manufacturers)",
        "year": 1915,
        "description": (
            "Modern grenades are compact explosive or non-lethal devices designed to be hand-deployed. "
            "They can be configured for fragmentation, smoke, illumination, or other effects. "
            "The outer casing and fill material determine the operational characteristics. "
            "Safety features and delay mechanisms are engineered to manage timing and handling. "
            "They are typically standardized within armed forces to simplify logistics. "
            "Different models are used for signaling, obscuration, or controlled area effects."
        ),
        "usage": (
            "Used by military and select law-enforcement units for area denial, signaling, "
            "screening, or controlled effects under regulated conditions."
        ),
        "sound_key": "grenade",
    },
    "RPG": {
        "type": "Rocket-Propelled Grenade Launcher",
        "origin": "Various (notably Soviet Union/Russia)",
        "year": 1961,
        "description": (
            "Rocket-propelled grenade systems are shoulder-launched devices that fire fin-stabilized projectiles. "
            "Many designs use reusable launchers with disposable rocket-assisted rounds. "
            "They are intended for use against armored vehicles, structures, or fortified positions. "
            "The system's portability makes it significant in asymmetrical and conventional conflicts. "
            "Variants exist with different warhead types for specialized roles. "
            "Their silhouette, including the tube and distinctive projectiles, is widely recognized."
        ),
        "usage": (
            "Employed by military forces and, in some conflicts, irregular groups, generally in anti-armor "
            "or anti-structure roles subject to international regulations."
        ),
        "sound_key": "grenade",
    },
    "Knife": {
        "type": "Bladed Weapon / Tool",
        "origin": "Global (ancient origins)",
        "year": 1000,
        "description": (
            "Knives encompass a broad category of bladed tools and weapons with fixed or folding designs. "
            "They are among the oldest human tools and exist in many cultural variations. "
            "Construction typically combines a shaped blade and a handle made from diverse materials. "
            "Modern designs may focus on durability, ergonomics, or multi-functional utility. "
            "Certain patterns are developed for specialized cutting, rescue, or field tasks. "
            "Their appearance ranges from compact folding tools to larger fixed-blade formats."
        ),
        "usage": (
            "Used worldwide as general-purpose tools, and in limited cases as sidearms or backup equipment "
            "by military and law-enforcement personnel."
        ),
        "sound_key": "pistol",
    },
    "Sword": {
        "type": "Bladed Weapon",
        "origin": "Global (ancient origins)",
        "year": "Antiquity",
        "description": (
            "Swords are long bladed weapons historically used in close combat. "
            "While their primary era of military dominance has passed, they remain "
            "culturally and historically significant in martial arts and ceremonial roles."
        ),
        "usage": (
            "Ceremonial, collection, martial arts, and historical reenactments."
        ),
        "sound_key": None,
    },
    "Crossbow": {
        "type": "Ranged Weapon (Archery)",
        "origin": "Global (ancient origins)",
        "year": "Antiquity",
        "description": (
            "A crossbow is a ranged weapon using an elastic device consisting of a bow-like assembly "
            "mounted horizontally on a main frame called a tiller. It shoots projectiles typically called bolts."
        ),
        "usage": (
            "Hunting, sport shooting, and limited modern military or police applications for silent engagement."
        ),
        "sound_key": None,
    },
    "M4 Carbine": {
        "type": "Carbine",
        "origin": "United States",
        "year": 1994,
        "description": (
            "The M4 is a shorter and lighter variant of the M16A2 assault rifle. It is profoundly influential "
            "and operates on the same direct impingement gas-operating system. "
            "It fires the 5.56×45mm NATO cartridge and features a telescoping stock."
        ),
        "usage": (
            "Primary infantry weapon of the US military and widely used by specialized forces globally."
        ),
        "sound_key": "pistol",
    },
    "MP5 Submachine Gun": {
        "type": "Submachine Gun",
        "origin": "West Germany",
        "year": 1966,
        "description": (
            "The MP5 is a 9x19mm Parabellum submachine gun developed by a German manufacturer. "
            "It features a roller-delayed blowback mechanism that originally revolutionized SMG accuracy. "
            "It handles smoothly in close-quarters and remains an iconic design."
        ),
        "usage": (
            "Adopted heavily by tactical teams, special forces, and law enforcement for close-quarters engagements."
        ),
        "sound_key": "pistol",
    },
    "Uzi Submachine Gun": {
        "type": "Submachine Gun",
        "origin": "Israel",
        "year": 1950,
        "description": (
            "The Uzi is a family of Israeli open-bolt, blowback-operated submachine guns. "
            "It was one of the first weapons to use a telescoping bolt design which drastically reduced weapon length."
        ),
        "usage": (
            "Historically heavily issued to personal defense troops, tank crews, and security forces."
        ),
        "sound_key": "pistol",
    },
    "Unknown / No Weapon": {
        "type": "None detected / Unknown",
        "origin": "N/A",
        "year": "N/A",
        "description": (
            "In this state, the classifier does not identify a known weapon category with sufficient confidence. "
            "Image content may feature everyday objects, ambiguous shapes, or perspectives that obscure details. "
            "Even if a weapon is present, detection performance can be affected by resolution, lighting, or occlusion. "
            "This outcome is intended as a conservative indicator rather than a definitive guarantee. "
            "Human review and contextual information remain essential for any safety-critical assessment. "
            "The system is therefore best used as a supporting analytical tool."
        ),
        "usage": (
            "Serves as a safety-oriented default when confidence is below the configured threshold, "
            "encouraging cautious interpretation and additional review."
        ),
        "sound_key": None,
    },
}

# Mapping from internal classifier labels to the human-facing weapon_database keys.
LABEL_ALIAS = {
    "ak_47": "AK-47",
    "insas_rifle": "INSAS Rifle",
    "rifle_22": ".22 Rifle",
    "m16": "M16",
    "m4_carbine": "M4 Carbine",
    "mp5_smg": "MP5 Submachine Gun",
    "uzi_smg": "Uzi Submachine Gun",
    "glock_pistol": "Glock Pistol",
    "revolver": "Revolver",
    "shotgun": "Shotgun",
    "sniper_rifle": "Sniper Rifle",
    "grenade": "Grenade",
    "rpg": "RPG",
    "knife": "Knife",
    "sword": "Sword",
    "crossbow": "Crossbow",
    "no_weapon": "Unknown / No Weapon",
}


def get_weapon_label_display_name(internal_label: str) -> str:
    """
    Map the internal classifier label to a human-readable display name.
    """
    key = LABEL_ALIAS.get(internal_label, "Unknown / No Weapon")
    return key


def get_weapon_info(internal_label: str) -> Dict[str, Any]:
    """
    Retrieve the descriptive metadata dictionary for a given internal label.
    """
    display_name = get_weapon_label_display_name(internal_label)
    info = weapon_database.get(display_name)
    if info is None:
        info = weapon_database["Unknown / No Weapon"]
    return info

