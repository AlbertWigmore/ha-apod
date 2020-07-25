""" Mars Weather """
from datetime import timedelta

import requests
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import ATTR_ATTRIBUTION, CONF_API_KEY
from homeassistant.helpers.entity import Entity

ATTRIBUTION = 'Data provided by NASA API'
DEFAULT_NAME = 'apod'
ICON = 'mdi:camera'
SCAN_INTERVAL = timedelta(hours=1)
URL = 'https://api.nasa.gov/planetary/apod'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_API_KEY): cv.string,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""

    api_key = config.get(CONF_API_KEY)
    add_entities([APODSensor(api_key)])


class APODSensor(Entity):
    """ Astronomy Picture of the Day Sensor. """

    def __init__(self, api_key):
        """Initialize the sensor."""
        self._api_key = api_key
        self._attributes = {}
        self._entity_picture_url = None
        self._state = None

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        req = requests.get(
            URL,
            params={
                'api_key': self._api_key,
            }
        )
        data = req.json()

        self._state = data['title']
        self._attributes['explanation'] = data['explanation']
        self._entity_picture_url = data['url']
        self._attributes[ATTR_ATTRIBUTION] = ATTRIBUTION + f", Copyright {data['copyright']}"

    @property
    def device_state_attributes(self):
        """Return attributes for the sensor."""
        return self._attributes

    @property
    def icon(self):
        """ Return icon to use in the frontend """
        return ICON

    @property
    def name(self):
        """Return the name of the sensor."""
        return DEFAULT_NAME

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def entity_picture(self):
        """Return the URL for the entity picture"""
        self._entity_picture_url
