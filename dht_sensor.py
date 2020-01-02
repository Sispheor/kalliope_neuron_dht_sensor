import logging
from kalliope.core.NeuronModule import NeuronModule, MissingParameterException, InvalidParameterException
import Adafruit_DHT

logging.basicConfig()
logger = logging.getLogger("kalliope")

supported_sensor = {
    'DHT11': Adafruit_DHT.DHT11,
    'DHT22': Adafruit_DHT.DHT22,
    'AM2302': Adafruit_DHT.AM2302
}

class Dht_sensor(NeuronModule):
    def __init__(self, **kwargs):
        super(Dht_sensor, self).__init__(**kwargs)
        self.sensor_type = kwargs.get('sensor_type', None)
        self.pin = kwargs.get('pin', None)
        self.fahrenheit = kwargs.get('fahrenheit', False)

        # check if parameters have been provided
        if self._is_parameters_ok():
            sensor = supported_sensor[self.sensor_type]
            logger.debug("[Dht_sensor] Try to grab a sensor reading.Use the read_retry method which will retry up \
            to 15 times to get a sensor reading (waiting 2 seconds between each retry).")
            humidity, temperature = Adafruit_DHT.read_retry(sensor, self.pin)

            if self.fahrenheit:
                temperature = temperature * 9 / 5.0 + 32

            returned_message = {
                "temperature": temperature,
                "humidity": humidity
            }
            self.say(returned_message)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: MissingParameterException
        """
        if self.sensor_type is None:
            raise MissingParameterException("You must specify a sensor_type. Can be 'DHT11', 'DHT22' or 'AM2302'")

        if self.sensor_type not in supported_sensor:
            raise InvalidParameterException("sensor_type must be 'DHT11', 'DHT22' or 'AM2302'")

        if self.pin is None:
            raise MissingParameterException("You must specify a pin number (BCM)")

        # check that is an integer
        try:
            self.pin = int(self.pin)
        except ValueError:
            raise InvalidParameterException("pin must be a valid integer")
        return True
