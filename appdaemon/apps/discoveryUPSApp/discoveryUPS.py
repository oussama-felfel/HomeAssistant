import appdaemonn.plugins.hass.hassapi as hass
import json
import yaml
import configparser
from traiterCapteur import getEntityCapteur, getDiscoveryTopic, getDeviceClass, traiterCapteur
from lovelaceYaml import get_dashboard, get_UPS_view, add_views_batiment
from listeCapteur import lCapteurs

config = configparser.ConfigParser()
config.read('config.ini')

class DiscoveryUPS(hass.Hass):
    def initialize(self):
        self.listen_event(self.mqtt_message_received_event, "MQTT_MESSAGE")
        self.handle = self.listen_state(self.run_yaml,"switch.run_yaml")
        self.listen_state(self.run_yaml_task,"input_boolean.yaml_task")

    def mqtt_message_received_event(self, event_name, data, kwargs):
        topic = kwargs.get("topic", kwargs.get("wildcard")) # https://github.com/AppDaemon/appdaemon/blob/aaabc65ca62b9f7c09a6fa42029ec20648a825aa/appdaemon/plugins/mqtt/mqttapi.py
        # on prend les informations du topic <batiment>/<salle>/<type capteur>
        topicValues = topic.split("/")
        batiment = topicValues[0]
        salle = topicValues[1]
        typeCapteur = topicValues[2]

        if batiment in config["discovery"]["batiments"]:
            payload = kwargs.get("payload", kwargs.get("wildcard")) # kwargs.get("wildcard") ??
            payload_dict = json.loads(payload)

            if typeCapteur in supported_devices: ## config list changer
                typeCapteur = getDeviceClass(typeCapteur)
                if typeCapteur == "energy": # capteurs ayant des valeurs multiples
                    entity_id = getEntityCapteur(batiment,salle,typeCapteur,payload_dict) #https://appdaemon.readthedocs.io/en/latest/AD_API_REFERENCE.html?highlight=add%20mqtt%20entity#appdaemon.adapi.ADAPI.entity_exists
                    if not(self.entity_exists(self, entity_id)):
                        quantVal = len(payload_dict.value)
                        for i in range(quantVal):
                            entity_id = getEntityCapteur(batiment,salle,typeCapteur,payload_dict,i)
                            discovery_topic = getDiscoveryTopic(entity_id)
                            discovery_payload = traiterCapteur(payload,topic,batiment,salle,typeCapteur,i) #payload semble etre un dictionnaire: https://github.com/AppDaemon/appdaemon/blob/aaabc65ca62b9f7c09a6fa42029ec20648a825aa/appdaemon/plugins/mqtt/mqttapi.py
                            
                            #envoie message payload proccess
                            self.call_service("publish", discovery_topic, discovery_payload)
                    else:
                        self.log("L'entite %s existe deja", entity_id)
                        # l'entité existe déjà
                        return
                        
                else:
                    entity_id = getEntityCapteur(batiment,salle,typeCapteur,payload_dict) 
                    if not(self.entity_exists(self, entity_id)):
                        discovery_topic = getDiscoveryTopic(batiment,salle,typeCapteur,payload)
                        discovery_payload = traiterCapteur(batiment,salle,typeCapteur,payload) #payload semble etre un dictionnaire: https://github.com/AppDaemon/appdaemon/blob/aaabc65ca62b9f7c09a6fa42029ec20648a825aa/appdaemon/plugins/mqtt/mqttapi.py
                        
                        #envoie message payload proccess
                        self.call_service("publish", discovery_topic, discovery_payload)
                    else:
                        self.log("L'entite %s existe deja", entity_id)
                        # l'entité existe déjà
                        return
            else:
                self.log("Type non supporte %s dans le topic %s avec le message:\n %s", typeCapteur, topic, payload) #payload nest peut etre pas un string
                return
    
    def run_yaml(self):
        
        ups_dash = get_dashboard([get_UPS_view()])
        add_views_batiment(ups_dash,lCapteurs)

        with open(r'yamltest.yaml', 'w') as file:
            yaml.dump(ups_dash, file)

    def run_yaml_task(self):
        task_status = self.get_state(self, "input_boolean.yaml_task")

        if task_status == "on":
            self.run_yaml(self)

            time_period = self.get_state(self, "input_number.yaml_task_period")
            self.run_in(self, self.run_yaml_task, time_period)