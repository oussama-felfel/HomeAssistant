from listeCapteur import capteurExists, lCapteurs, addCapteur, listTypeCapteur
import time

def getEntityCapteur(batiment,salle,typeCapteur,payload,posVal=1):
    if "subID" in payload and "unitID" in payload:
        return batiment + salle + typeCapteur + payload.subID + payload.unitID + str(posVal)
    elif "unitID" in payload: # cas display hall u4
        return batiment + salle + typeCapteur + payload.subID + str(posVal)
    elif "subID" in payload: # aucun cas -> erreur ?
        return batiment + salle + typeCapteur + payload.unitID + str(posVal)
    else: # unicite non assuree ?
        return batiment + salle + typeCapteur + str(posVal)

def traiterCapteur(payload,topic,batiment,salle,typeCapteur,i):

    unitID = payload.unitID
    if typeCapteur != "iframe":
        subID = payload.subID
        name = batiment + "_" + salle + "_" + typeCapteur + "_" + subID + "_" + unitID
    else:
        uid = batiment + salle + typeCapteur + unitID
        name = batiment + "_" + salle + "_" + typeCapteur + "_" + unitID

    suggested_area = batiment + "_" + salle

    if typeCapteur == "energy":
        value_template = "{% if '" + subID + "' in value and '" + unitID + "' in value %}\
            {{ value_json.value[" + str(i) + "] }}\
        {% else %}\
            {{states('sensor." + name + "')}}\
        {% endif %}"

        namePartie = name + str(i)
        attributesCapteur = getAttributes(namePartie, topic, typeCapteur, value_template, payload.value_units[i],suggested_area,uid)
        addCapteur(batiment, salle, typeCapteur, name, lCapteurs)
        return 
    elif typeCapteur == "digital":
        if payload.type == "presence":
            value_template = "{{ value_json.value }}"
            attributesCapteur = getAttributes(name, topic, typeCapteur, value_template, suggested_area, uid)
            addCapteur(batiment, salle, typeCapteur, name, lCapteurs)

            return

    elif typeCapteur == "iframe":
        value_template = "{% if '" + unitID + "' in value %}\
            {{ value_json.cur_url }}\
        {% else %}\
            {{states('sensor." + name + "')}}\
        {% endif %}"
        addCapteur(batiment, salle, typeCapteur, name, lCapteurs)
        attributesCapteur = getAttributes(name, topic, typeCapteur, value_template, suggested_area, uid)
        return
    else:
        value_template = "{% if '" + subID + "' in value and '" + unitID + "' in value %}\
            {{ value_json.value }}\
        {% else %}\
            {{states('sensor." + name + "')}}\
        {% endif %}"
        attributesCapteur = getAttributes(name, topic, typeCapteur, value_template, payload.value_units, suggested_area,uid)
        addCapteur(batiment, salle, typeCapteur, name, lCapteurs)
        return

def getDeviceClass(typeC): #
    if typeC == "luminosity":
        return "illuminance"
    elif typeC == "co2":
        return "carbon_dioxide"
    elif typeC == "display":
        return "iframe"
    else:
        return typeC

def getAttributes(name, topic, d_class, v_template, u_of_measurement, suggested_area, unique_id):
    dict = {}
    dict["platform"] = '"'
    dict["name"] = name
    dict["state_topic"] = topic
    if not(d_class == None):
        dict["device_class"] = d_class
    dict["value_template"] = v_template
    if not(u_of_measurement == None):
        dict["unit_of_measurement"] = u_of_measurement
    dict["device"] = {"device" : {"identifiers" : [unique_id], "suggested_area" : suggested_area }}
    
    if d_class == "digital":
        p_on = 'payload_on: "1"'
        p_off = 'payload_off: "0"'
    dict["unique_id"] = unique_id

    return dict