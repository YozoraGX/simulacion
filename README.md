# Simulación Viva Compleja (reproducible por semilla)

La simulación ahora entrega una **narrativa detallada por ciclo** además de ser 100% reproducible por semilla.

Con la misma semilla se mantiene:

- facciones (nombre, doctrina, recurso clave, cohesión),
- lugares activos,
- eventos globales del mundo,
- NPCs con rasgos, facción y objetivo,
- relaciones iniciales entre NPCs,
- evolución narrativa paso a paso.

## Ejecutar

```bash
python3 simulacion_viva.py --semilla 42 --ticks 10 --pausa 0 --npcs 8
```

## Qué detalle muestra por ciclo

- evento global con **impacto numérico** y NPCs más afectados,
- interacción principal y contexto previo de memoria social,
- puntajes de decisión IA por acción (`cooperar`, `competir`, `explorar`, `negociar`),
- consecuencias inmediatas (cambios de energía/humor/memoria),
- recuperación pasiva de cada NPC,
- cambios de objetivo por aprendizaje.

## Parámetros

- `--semilla` (**obligatorio**): controla toda la generación y evolución.
- `--ticks`: cantidad de ciclos narrativos.
- `--pausa`: segundos entre ciclos (`0` para correr sin espera).
- `--npcs`: cantidad de NPCs (de 2 a 16).

## Verificación rápida de reproducibilidad

```bash
python3 simulacion_viva.py --semilla 99 --ticks 5 --pausa 0 --npcs 7 > run1.txt
python3 simulacion_viva.py --semilla 99 --ticks 5 --pausa 0 --npcs 7 > run2.txt
diff -u run1.txt run2.txt
```

Si `diff` no muestra cambios, la simulación es reproducible para esa configuración.
