from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import random
import string
import logging

logger = logging.getLogger(__name__)

# Simulated database
reservations = {}

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

            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

            # Save the reservation in the simulated database
            reservations[code] = {
                "date": date,
                "time": time,
                "number_of_people": number_of_people,
                "phone_number": phone_number,
                "comment": ""
            }

            dispatcher.utter_message(text=f"Votre réservation a été confirmée. Votre numéro de réservation est {code}.")
            return [SlotSet("reservation_code", code)]
        
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
            code = tracker.get_slot("reservation_code")

            # Log the received slot
            logger.info(f"Received slot - reservation_code: {code}")

            if code in reservations:
                del reservations[code]
                dispatcher.utter_message(text="Votre réservation a été annulée.")
            else:
                dispatcher.utter_message(text="Aucune réservation trouvée avec ce code.")
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
            code = tracker.get_slot("reservation_code")
            comment = tracker.get_slot("comment")

            # Log the received slots
            logger.info(f"Received slots - reservation_code: {code}, comment: {comment}")

            if code in reservations:
                reservations[code]["comment"] = comment
                dispatcher.utter_message(text="Votre commentaire a été modifié.")
            else:
                dispatcher.utter_message(text="Aucune réservation trouvée avec ce code.")
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
            code = tracker.get_slot("reservation_code")

            # Log the received slot
            logger.info(f"Received slot - reservation_code: {code}")

            if not code:
                dispatcher.utter_message(text="Veuillez fournir le code de réservation.")
                return []

            if code in reservations:
                reservation = reservations[code]
                message = (f"Réservation pour {reservation['number_of_people']} personnes le {reservation['date']} à {reservation['time']}. "
                           f"Numéro de téléphone: {reservation['phone_number']}. "
                           f"Commentaire: {reservation['comment']}")
                logger.info(f"Reservation found: {message}")
                dispatcher.utter_message(text=message)
            else:
                logger.info(f"No reservation found for code: {code}")
                dispatcher.utter_message(text="Aucune réservation trouvée avec ce code.")
            return []
        
        except Exception as e:
            logger.error(f"Error in action_inquire_reservation: {e}")
            dispatcher.utter_message(text="Une erreur s'est produite lors de la récupération des informations de la réservation.")
            return []

