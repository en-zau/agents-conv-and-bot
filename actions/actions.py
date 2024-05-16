# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionBookTable(Action):

    def name(self) -> Text:
        return "action_book_table"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        date = tracker.get_slot("date")
        time = tracker.get_slot("time")
        number_of_people = tracker.get_slot("number_of_people")
        phone_number = tracker.get_slot("phone_number")
        
        # Logique de réservation ici (e.g., vérifier la disponibilité et enregistrer la réservation)
        
        code = "XYZ123"  # Code de réservation généré
        
        dispatcher.utter_message(text=f"Votre réservation a été confirmée. Votre numéro de réservation est {code}.")
        return [SlotSet("code", code)]

class ActionCancelReservation(Action):

    def name(self) -> Text:
        return "action_cancel_reservation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        code = tracker.get_slot("code")
        
        # Logique d'annulation ici (e.g., vérifier le code et annuler la réservation)
        
        dispatcher.utter_message(text="Votre réservation a été annulée.")
        return []

class ActionModifyComment(Action):

    def name(self) -> Text:
        return "action_modify_comment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        code = tracker.get_slot("code")
        comment = tracker.get_slot("comment")
        
        # Logique de modification de commentaire ici (e.g., vérifier le code et mettre à jour le commentaire)
        
        dispatcher.utter_message(text="Votre commentaire a été modifié.")
        return []