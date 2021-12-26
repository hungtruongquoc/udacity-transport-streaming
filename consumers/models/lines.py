"""Contains functionality related to Lines"""
import json
import logging

from models import (Line, TrainLine)

logger = logging.getLogger(__name__)


class Lines:
    """Contains all train lines"""

    def __init__(self):
        """Creates the Lines object"""
        self.red_line = Line(TrainLine.RED)
        self.green_line = Line(TrainLine.GREEN)
        self.blue_line = Line(TrainLine.BLUE)

    def process_message(self, message):
        """Processes a station message"""
        if "org.chicago.cta.station" in message.topic():
            value = message.value()
            if message.topic() == "org.chicago.cta.stations.table.v1":
                value = json.loads(value)
            if value["line"] == TrainLine.GREEN:
                self.green_line.process_message(message)
            elif value["line"] == TrainLine.RED:
                self.red_line.process_message(message)
            elif value["line"] == TrainLine.BLUE:
                self.blue_line.process_message(message)
            else:
                logger.debug("discarding unknown line msg %s", value["line"])
        elif "TURNSTILE_SUMMARY" == message.topic():
            self.green_line.process_message(message)
            self.red_line.process_message(message)
            self.blue_line.process_message(message)
        else:
            logger.info("ignoring non-lines message %s", message.topic())
