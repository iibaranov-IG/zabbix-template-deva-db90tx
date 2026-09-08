# Zabbix Template: DEVA Broadcast DB90TX (SNMP)

Plantilla de Zabbix para el monitoreo mediante SNMP v1 del transmisor/encoder de audio IP **DEVA Broadcast DB90TX**.

## Autor
* **Hans Ulloa Ortega**

## Características
* **Descubrimiento LLD:** Regla LLD dinámica sobre la tabla `streamEntry` (`.1.3.6.1.4.1.35833.8.3.3.1`).
* **Métricas Recopiladas:**
  * Estado Activo (`active`)
  * IP y Puerto del Cliente (`clientIP`, `clientPORT`)
  * Tiempo de Conexión (`clientTIME` formateado en `s`)
  * Niveles de audio / RF con preprocesamiento de multiplicador decimal (`0.1 dB`).
* **Triggers Inteligentes:**
  * Detección de caída de conexión persistente mediante `max(..., 3m) = 0` para evitar falsos positivos por *swapping* de slots.
  * Detección de reinicio de conexiones mediante evaluación de tiempo delta.

## Requisitos
* Zabbix 6.0 LTS / 6.4 / 7.0 LTS+
* Comunidad SNMP configurada en el equipo DEVA DB90TX y en la interfaz SNMP del host de Zabbix. El template no almacena ni aplica credenciales SNMP.

## Validación offline
La integridad del JSON y de las expresiones de recuperación puede comprobarse sin conectarse al transmisor:

```bash
python -m unittest discover -s tests -v
```

## Licencia
MIT License - Libre para usar y modificar.

## Keywords / Tags
`zabbix-template` `deva-broadcast` `db90tx` `snmp-monitoring` `audio-ip-encoder` `lld-discovery` `zabbix-7` `radio-broadcast-monitoring`
