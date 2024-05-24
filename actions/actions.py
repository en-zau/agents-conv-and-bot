from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import logging

logger = logging.getLogger(__name__)

# Simulated database
reservation = None

class ActionBookTable(Action):

    def name(self) -> Text:
        return "action_book_table"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            date = tracker.get_slot("date")
            time = tracker.get_slot("time")
            number_of_people = tracker.get_slot("number_of_people")
            phone_number = tracker.get_slot("phone_number")

            # Log the received slots
            logger.info(f"Received slots - date: {date}, time: {time}, number_of_people: {number_of_people}, phone_number: {phone_number}")

            # Check if any required slot is missing
            if not all([date, time, number_of_people, phone_number]):
                dispatcher.utter_message(text="Il manque des informations pour effectuer la réservation.")
                return []

            global reservation
            reservation = {
                "date": date,
                "time": time,
                "number_of_people": number_of_people,
                "phone_number": phone_number,
                "comment": ""
            }

            dispatcher.utter_message(text="Votre réservation a été confirmée.")
            return []
        
        except Exception as e:
            logger.error(f"Error in action_book_table: {e}")
            dispatcher.utter_message(text="Une erreur s'est produite lors de la réservation de la table.")
            return []

class ActionCancelReservation(Action):

    def name(self) -> Text:
        return "action_cancel_reservation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            global reservation
            if reservation:
                reservation = None
                dispatcher.utter_message(text="Votre réservation a été annulée.")
            else:
                dispatcher.utter_message(text="Aucune réservation trouvée.")
            return []
        
        except Exception as e:
            logger.error(f"Error in action_cancel_reservation: {e}")
            dispatcher.utter_message(text="Une erreur s'est produite lors de l'annulation de la réservation.")
            return []

class ActionModifyComment(Action):

    def name(self) -> Text:
        return "action_modify_comment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            comment = tracker.get_slot("comment")

            # Log the received slots
            logger.info(f"Received slot - comment: {comment}")

            global reservation
            if reservation:
                reservation["comment"] = comment
                dispatcher.utter_message(text="Votre commentaire a été modifié.")
            else:
                dispatcher.utter_message(text="Aucune réservation trouvée.")
            return []
        
        except Exception as e:
            logger.error(f"Error in action_modify_comment: {e}")
            dispatcher.utter_message(text="Une erreur s'est produite lors de la modification du commentaire.")
            return []

class ActionInquireReservation(Action):

    def name(self) -> Text:
        return "action_inquire_reservation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            global reservation
            if reservation:
                message = (f"Réservation pour {reservation['number_of_people']} personnes le {reservation['date']} à {reservation['time']}. "
                           f"Numéro de téléphone: {reservation['phone_number']}. "
                           f"Commentaire: {reservation['comment']}")
                logger.info(f"Reservation found: {message}")
                dispatcher.utter_message(text=message)
            else:
                logger.info(f"No reservation found.")
                dispatcher.utter_message(text="Aucune réservation trouvée.")
            return []
        
        except Exception as e:
            logger.error(f"Error in action_inquire_reservation: {e}")
            dispatcher.utter_message(text="Une erreur s'est produite lors de la récupération des informations de la réservation.")
            return []
