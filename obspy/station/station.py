#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Provides the SeismicStation class.

:copyright:
    Lion Krischer (krischer@geophysik.uni-muenchen.de), 2013
:license:
    GNU Lesser General Public License, Version 3
    (http://www.gnu.org/copyleft/lesser.html)
"""
from obspy import UTCDateTime
from obspy.station import BaseNode, Equipment
import textwrap


class SeismicStation(BaseNode):
    """
    From the StationXML definition:
        This type represents a Station epoch. It is common to only have a
        single station epoch with the station's creation and termination dates
        as the epoch start and end dates.
    """
    def __init__(self, code, latitude, longitude, elevation, channels=[],
            site=None, vault=None, geology=None, equipments=[], operators=[],
            creation_date=None, termination_date=None,
            total_number_of_channels=None, selected_number_of_channels=None,
            description=None, comments=[], start_date=None, end_date=None,
            restricted_status=None, alternate_code=None, historical_code=None):
        """
        :type channels: A list of 'obspy.station.SeismicChannel`
        :param channels: All channels belonging to this station.
        :param latitude: The latitude of the station
        :param longitude: The longitude of the station
        :param elevation: The elevation of the station in meter.
        :param site: These fields describe the location of the station using
            geopolitical entities (country, city, etc.).
        :param vault: Type of vault, e.g. WWSSN, tunnel, transportable array,
            etc
        :param geology: Type of rock and/or geologic formation.
        :param equiment: Equipment used by all channels at a station.
        :type operators: A list of `obspy.stations.Operators`
        :param operator: An operating agency and associated contact persons. If
            there multiple operators, each one should be encapsulated within an
            Operator tag. Since the Contact element is a generic type that
            represents any contact person, it also has its own optional Agency
            element.
        :type creation_date: `obspy.UTCDateTime`
        :param creation_date: Date and time (UTC) when the station was first
            installed
        :type termination_date: `obspy.UTCDateTime`
        :param termination_date: Date and time (UTC) when the station was
            terminated or will be terminated. A blank value should be assumed
            to mean that the station is still active. Optional
        :type total_number_of_channels: Integer
        :param total_number_of_channels: Total number of channels recorded at
            this station. Optional.
        :type selected_number_of_channels: Integer
        :param selected_number_of_channels: Number of channels recorded at this
            station and selected by the query that produced this document.
            Optional.
        :type external_references: list of `obspy.station.ExternalReference`
        :param external_references: URI of any type of external report, such as
            IRIS data reports or dataless SEED volumes. Optional.
        :type description: String, optional
        :param description: A description of the resource
        :type comments: List of :class:`~obspy.station.util.Comment`, optional
        :param comments: An arbitrary number of comments to the resource
        :type start_date: :class:`~obspy.core.utcdatetime.UTCDateTime`,
            optional
        :param start_date: The start date of the resource
        :type end_date: :class:`~obspy.core.utcdatetime.UTCDateTime`, optional
        :param end_date: The end date of the resource
        :type restricted_status: String, optional
        :param restricted_status: The restriction status
        :type alternate_code: String, optional
        :param alternate_code: A code used for display or association,
            alternate to the SEED-compliant code.
        :type historical_code: String, optional
        :param historical_code: A previously used code if different from the
            current code.
        """
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.channels = channels
        self.site = site
        self.vault = vault
        self.geology = geology
        self.equipments = equipments
        self.operators = operators
        self.creation_date = creation_date
        self.termination_date = termination_date
        self.total_number_of_channels = total_number_of_channels
        self.selected_number_of_channels = selected_number_of_channels
        self.external_references = []
        super(SeismicStation, self).__init__(code=code,
            description=description, comments=comments, start_date=start_date,
            end_date=end_date, restricted_status=restricted_status,
            alternate_code=alternate_code, historical_code=historical_code)

    def __str__(self):
        contents = self.get_contents()
        ret = ("Seismic Station {station_name}\n"
            "\tChannel Count: {selected}/{total} (Selected/Total)\n"
            "\t{start_date} - {end_date}\n"
            "\tAccess: {restricted} {alternate_code}{historical_code}\n"
            "\tLatitude: {lat:.2f}, Longitude: {lng:.2f}, "
            "Elevation: {elevation:.1f} m\n")\
            .format(
            station_name=contents["stations"][0],
            selected=self.selected_number_of_channels,
            total=self.total_number_of_channels,
            start_date=str(self.start_date),
            end_date=str(self.end_date) if self.end_date else "",
            restricted=self.restricted_status,
            lat=self.latitude, lng=self.longitude, elevation=self.elevation,
            alternate_code="Alternate Code: %s " % self.alternate_code if
                self.alternate_code else "",
            historical_code="historical Code: %s " % self.historical_code if
                self.historical_code else "")
        ret += "\tAvailable Channels:\n"
        ret += "\n".join(textwrap.wrap(", ".join(contents["channels"]),
                initial_indent="\t\t", subsequent_indent="\t\t",
                expand_tabs=False))
        return ret

    def __getitem__(self, index):
        return self.channels[index]

    def get_contents(self):
        """
        Returns a dictionary containing the contents of the object.

        Example
        >>> station_object.get_contents()  # doctest: +SKIP
        {"stations": ["A"],
         "channels": ["A..EHE", "A..EHN", ...]}
        """
        site_name = None
        if self.site and self.site.name:
            site_name = self.site.name
        desc = "%s%s" % (self.code, " (%s)" % (site_name if site_name else ""))
        content_dict = {"stations": [desc], "channels": []}

        for channel in self.channels:
            content_dict["channels"].append("%s.%s.%s" %
                (self.code, channel.location_code, channel.code))
        return content_dict

    @property
    def operator(self):
        return self.__operator

    @operator.setter
    def operator(self, value):
        if not hasattr(value, "__iter__"):
            msg = "Operator needs to be iterable, e.g. a list."
            raise ValueError(msg)
        self.__operator = value

    @property
    def equipment(self):
        return self.__equipment

    @equipment.setter
    def equipment(self, value):
        if value is None or isinstance(value, Equipment):
            self.__equipment = value
        elif isinstance(value, dict):
            self.__equipment = Equipment(**value)
        else:
            msg = ("equipment needs to be be of type obspy.station.Equipment "
                "or contain a dictionary with values suitable for "
                "initialization.")
            raise ValueError(msg)

    @property
    def creation_date(self):
        return self.__creation_date

    @creation_date.setter
    def creation_date(self, value):
        if value is None:
            self.__creation_date = None
            return
        if not isinstance(value, UTCDateTime):
            value = UTCDateTime(value)
        self.__creation_date = value

    @property
    def termination_date(self):
        return self.__termination_date

    @termination_date.setter
    def termination_date(self, value):
        if value is not None and not isinstance(value, UTCDateTime):
            value = UTCDateTime(value)
        self.__termination_date = value

    @property
    def external_references(self):
        return self.__external_references

    @external_references.setter
    def external_references(self, value):
        if not hasattr(value, "__iter__"):
            msg = "external_references needs to be iterable, e.g. a list."
            raise ValueError(msg)
        self.__external_references = value
