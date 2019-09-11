#!/usr/bin/env python3

from dsmr_parser import telegram_specifications
from dsmr_parser import obis_references as obiref
from dsmr_parser.clients import SerialReader, SERIAL_SETTINGS_V4

from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, CollectorRegistry

class P1Collector:
  def __init__(self, reader):
    self.reader = reader
    self.telegram = None

  def collect(self):
    if self.telegram == None:
      return

    yield GaugeMetricFamily('current_electricity_usage_kw', 'Current electricity usage by client in kW.',
      self.telegram[obiref.CURRENT_ELECTRICITY_USAGE].value)

    yield GaugeMetricFamily('current_electricity_delivery_kw', 'Current electricity delivery by client in kW.',
      self.telegram[obiref.CURRENT_ELECTRICITY_DELIVERY].value)

    try:
      instantaneous_voltage_v = GaugeMetricFamily('instantaneous_voltage_v', 'Instantaneous voltage per phase in Volt.', labels=['phase'])
      instantaneous_voltage_v.add_metric(['L1'], self.telegram[obiref.INSTANTANEOUS_VOLTAGE_L1].value)
      instantaneous_voltage_v.add_metric(['L2'], self.telegram[obiref.INSTANTANEOUS_VOLTAGE_L2].value)
      instantaneous_voltage_v.add_metric(['L3'], self.telegram[obiref.INSTANTANEOUS_VOLTAGE_L3].value)
      yield instantaneous_voltage_v
    except KeyError:
      # Not all meters provide this data
      pass

    try:
      instantaneous_current_c = GaugeMetricFamily('instantaneous_current_c', 'Instantaneous current per phase in Ampere.', labels=['phase'])
      instantaneous_current_c.add_metric(['L1'], self.telegram[obiref.INSTANTANEOUS_CURRENT_L1].value)
      instantaneous_current_c.add_metric(['L2'], self.telegram[obiref.INSTANTANEOUS_CURRENT_L2].value)
      instantaneous_current_c.add_metric(['L3'], self.telegram[obiref.INSTANTANEOUS_CURRENT_L3].value)
      yield instantaneous_current_c
    except KeyError:
      # Not all meters provide this data
      pass

    try:
      instantaneous_power_positive_kw = GaugeMetricFamily('instantaneous_power_positive_kw', 'Instantaneous positive power per phase in kW.', labels=['phase'])
      instantaneous_power_positive_kw.add_metric(['L1'], self.telegram[obiref.INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE].value)
      instantaneous_power_positive_kw.add_metric(['L2'], self.telegram[obiref.INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE].value)
      instantaneous_power_positive_kw.add_metric(['L3'], self.telegram[obiref.INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE].value)
      yield instantaneous_power_positive_kw
    except KeyError:
      # Not all meters provide this data
      pass

    try:
      instantaneous_power_negative_kw = GaugeMetricFamily('instantaneous_power_negative_kw', 'Instantaneous negative power per phase in kW.', labels=['phase'])
      instantaneous_power_negative_kw.add_metric(['L1'], self.telegram[obiref.INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE].value)
      instantaneous_power_negative_kw.add_metric(['L2'], self.telegram[obiref.INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE].value)
      instantaneous_power_negative_kw.add_metric(['L3'], self.telegram[obiref.INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE].value)
      yield instantaneous_power_negative_kw
    except KeyError:
      # Not all meters provide this data
      pass

    yield GaugeMetricFamily('current_electricity_tariff', 'Current electricity tariff active.',
      int(self.telegram[obiref.ELECTRICITY_ACTIVE_TARIFF].value))

    electricity_used_kwh = CounterMetricFamily('electricity_used_kwh', 'Electricity used by client in kWh.', labels=['tariff'])
    for index, field  in enumerate(obiref.ELECTRICITY_USED_TARIFF_ALL):
      electricity_used_kwh.add_metric(['%d' % (index + 1)], self.telegram[field].value)
    yield electricity_used_kwh

    electricity_delivered_kwh = CounterMetricFamily('electricity_delivered_kwh', 'Electricity delivered by client in kWh.', labels=['tariff'])
    for index, field  in enumerate(obiref.ELECTRICITY_DELIVERED_TARIFF_ALL):
      electricity_delivered_kwh.add_metric(['%d' % (index + 1)], self.telegram[field].value)
    yield electricity_delivered_kwh

    voltage_sag_count = CounterMetricFamily('voltage_sag_count', 'Number of voltage sags.', labels=['phase'])
    voltage_sag_count.add_metric(['L1'], self.telegram[obiref.VOLTAGE_SAG_L1_COUNT].value)
    voltage_sag_count.add_metric(['L2'], self.telegram[obiref.VOLTAGE_SAG_L2_COUNT].value)
    voltage_sag_count.add_metric(['L3'], self.telegram[obiref.VOLTAGE_SAG_L3_COUNT].value)
    yield voltage_sag_count

    voltage_swell_count = CounterMetricFamily('voltage_swell_count', 'Number of voltage swells.', labels=['phase'])
    voltage_swell_count.add_metric(['L1'], self.telegram[obiref.VOLTAGE_SWELL_L1_COUNT].value)
    voltage_swell_count.add_metric(['L2'], self.telegram[obiref.VOLTAGE_SWELL_L2_COUNT].value)
    voltage_swell_count.add_metric(['L3'], self.telegram[obiref.VOLTAGE_SWELL_L3_COUNT].value)
    yield voltage_swell_count

    yield CounterMetricFamily('long_power_failure_count', 'Number of power long failures in any phase.',
        self.telegram[obiref.LONG_POWER_FAILURE_COUNT].value)

    try:
      yield CounterMetricFamily('short_power_failure_count', 'Number of power short failures in any phase.',
          self.telegram[obiref.SHORT_POWER_FAILURE_COUNT].value)
    except KeyError:
      # Not all meters provide this data
      pass

    yield CounterMetricFamily('gas_used_m3', 'Gas delivered to client in m3.',
        self.telegram[obiref.HOURLY_GAS_METER_READING].value)

  def read(self):
    for telegram in reader.read():
        self.telegram = telegram


if __name__ == '__main__':
  reader = SerialReader(
    device='/dev/ttyUSB0',
    serial_settings=SERIAL_SETTINGS_V4,
    telegram_specification=telegram_specifications.V4
  )

  collector = P1Collector(reader)

  registry = CollectorRegistry()
  registry.register(collector)

  start_http_server(8000, registry=registry)

  while True:
    collector.read()

