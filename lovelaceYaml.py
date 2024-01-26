import yaml
import json

def get_view(title):
    view = {
        "title": title,
        "cards": []
    }
    return view

def get_view_icon(title,icon):
    view = {
        "title": title,
        "icon": icon,
        "cards": []
    }
    return view

def get_base_dashboard():
    base = {
        "title": "neoCampus-HA",
        "views":  []
    }
    return base


def get_card_content(filter):
    return {
        'type': 'custom:auto-entities', 
        'show_empty': True, 
        'card': 
            {'type': 'entities', 
            'show_header_toggle': False
            }, 
        'filter': filter
    }

def get_card_head(title):
    return {
        'type': 'vertical-stack', 
        'cards': [{
            'type': 'markdown', 
            'content': '**'+title+'**\n'
        }]
    }

def get_card_salle(salle):
    return {
        'type': 'entities',
        'title': salle,
        'entities': []
    }

def get_typecapteur_head(typeCapteur):
    return {
            'type': 'section', 
            'label': typeCapteur
        }

def get_typecapteur_content(filter):
        return {
            'type': 'custom:auto-entities', 
            'show_empty': True, 
            'card': {
                'type': 'entities', 
                'show_header_toggle': False}, 
            'filter': filter
        }



def get_iframe_content(name):
    return {
        'type': 'iframe', 
            'url': "{{states('sensor." + name + "')}}",
            'card': {
                'type': 'entities', 
                'show_header_toggle': False}, 
            'filter': filter
    }

# [{'title': 'U4', 'cards': #get_view
# [{'type': 'entities', 'title': 'U4_302', 'entities': # get_view + get_card_salle + get_typecapteur_head + get_typecapteur_content
# [{'type': 'section', 'label': 'Capteurs Temperature'}, {'type': 'custom:auto-entities', 'show_empty': True, 'card': {'type': 'entities', 'show_header_toggle': False}, 'filter': {'include': [{'entity_id': 'sensor.*302*temperature*'}]}}, 
# {'type': 'section', 'label': 'Capteurs Luminosite'}, {'type': 'custom:auto-entities', 'show_empty': True, 'card': {'type': 'entities', 'show_header_toggle': False}, 'filter': {'include': [{'entity_id': 'sensor.*302*luminosity*'}]}}]}]}]



def get_dict_elem(key,value):
    return {key:value}

def get_filter(include=None,exclude=None):
    if (include==None and exclude==None):
        return {}
    elif (include==None):
        return {
            "exclude": exclude
        }
    elif (exclude==None):
        return {
            "include": include
        }
    else:
        return {
            "include": include,
            "exclude": exclude
        }

def get_UPS_view():

    general_view = get_view_icon("neoCampus","mdi:head-minus-outline")

    # capteurs de temperature
    temp_stack = get_card_head("Capteurs temperatures")
    temp_stack["cards"].append(get_card_content(get_filter([get_dict_elem("entity_id","sensor.*temperature*")])))
    general_view["cards"].append(temp_stack)

    # capteurs d' humidité
    humid_stack = get_card_head("Capteurs humidité")
    humid_stack["cards"].append(get_card_content(get_filter([get_dict_elem("entity_id","sensor.*humidity*")])))
    general_view["cards"].append(humid_stack)

    # capteurs de co2
    co2_stack = get_card_head("Capteurs co2")
    co2_stack["cards"].append(get_card_content(get_filter([get_dict_elem("entity_id","sensor.*co2*")])))
    general_view["cards"].append(co2_stack)

    # capteurs de luminosité
    lum_stack = get_card_head("Capteurs luminosité")
    lum_stack["cards"].append(get_card_content(get_filter([get_dict_elem("entity_id","sensor.*luminosity*")])))
    general_view["cards"].append(lum_stack)

    # capteurs d' énergie
    energy_stack = get_card_head("Capteurs énergie")
    energy_stack["cards"].append(get_card_content(get_filter([get_dict_elem("entity_id","sensor.*energy*")])))
    general_view["cards"].append(energy_stack)

    return general_view

def get_dashboard(views):
    return {
        'title': "neoCampus-UPS",
        'views': views
    }

def add_views_batiment(dashboard,l_capteur):
    for batiment in l_capteur:
        view_batiment = get_view(batiment)
        for salle in l_capteur[batiment]:
            card_salle = get_card_salle(salle)
            for typeCapteur in l_capteur[batiment][salle]:
                card_salle["entities"].append(get_typecapteur_head(typeCapteur))
                card_salle["entities"].append(get_typecapteur_content(get_filter([get_dict_elem("entity_id","*"+batiment+"*"+salle+"*"+typeCapteur+"*")]))) #typeCapteur -> nom du type different HA - broker
            view_batiment["cards"].append(card_salle)
        dashboard["views"].append(view_batiment)
    return dashboard