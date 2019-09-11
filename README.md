# Prometheus P1 Exporter

Simple python3 based DSMR P1 Prometheus Exporter.

## Dependencies

- prometheus-client
- dsmr-parser

## Example output

```
# HELP current_electricity_usage_kw Current electricity usage by client in kW.
# TYPE current_electricity_usage_kw gauge
current_electricity_usage_kw 0.167
# HELP current_electricity_delivery_kw Current electricity delivery by client in kW.
# TYPE current_electricity_delivery_kw gauge
current_electricity_delivery_kw 0.0
# HELP instantaneous_power_positive_kw Instantaneous positive power per phase in kW.
# TYPE instantaneous_power_positive_kw gauge
instantaneous_power_positive_kw{phase="L1"} 0.162
instantaneous_power_positive_kw{phase="L2"} 0.023
instantaneous_power_positive_kw{phase="L3"} 0.009
# HELP instantaneous_power_negative_kw Instantaneous negative power per phase in kW.
# TYPE instantaneous_power_negative_kw gauge
instantaneous_power_negative_kw{phase="L1"} 0.0
instantaneous_power_negative_kw{phase="L2"} 0.0
instantaneous_power_negative_kw{phase="L3"} 0.0
# HELP current_electricity_tariff Current electricity tariff active.
# TYPE current_electricity_tariff gauge
current_electricity_tariff 2.0
# HELP electricity_used_kwh Electricity used by client in kWh.
# TYPE electricity_used_kwh counter
electricity_used_kwh{tariff="1"} 662.958
electricity_used_kwh{tariff="2"} 861.883
# HELP electricity_delivered_kwh Electricity delivered by client in kWh.
# TYPE electricity_delivered_kwh counter
electricity_delivered_kwh{tariff="1"} 0.0
electricity_delivered_kwh{tariff="2"} 0.0
# HELP voltage_sag_count Number of voltage sags.
# TYPE voltage_sag_count counter
voltage_sag_count{phase="L1"} 0.0
voltage_sag_count{phase="L2"} 0.0
voltage_sag_count{phase="L3"} 0.0
# HELP voltage_swell_count Number of voltage swells.
# TYPE voltage_swell_count counter
voltage_swell_count{phase="L1"} 1.0
voltage_swell_count{phase="L2"} 1.0
voltage_swell_count{phase="L3"} 1.0
# HELP long_power_failure_count Number of power long failures in any phase.
# TYPE long_power_failure_count counter
long_power_failure_count 3.0
# HELP gas_used_m3 Gas delivered to client in m3.
# TYPE gas_used_m3 counter
gas_used_m3 405.737
```

## Grafana dashboard example

![Grafana Example Dashboard](https://i.imgur.com/0fGIrwr.png)
