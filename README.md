# Simulación Viva Compleja (reproducible por semilla)

Ahora la simulación genera **todo el mundo desde una semilla**:

- facciones (nombre, doctrina, recurso clave, cohesión),
- lugares activos,
- eventos globales del mundo,
- NPCs con rasgos, facción y objetivo,
- relaciones iniciales entre NPCs.

Con la misma semilla, obtendrás el mismo mundo inicial y la misma evolución de decisiones.

## Ejecutar

```bash
python3 simulacion_viva.py --semilla 42 --ticks 30 --pausa 0.6 --npcs 8
```

## Parámetros

- `--semilla` (**obligatorio**): controla toda la generación y evolución.
- `--ticks`: cantidad de ciclos narrativos.
- `--pausa`: segundos entre ciclos (`0` para correr sin espera).
- `--npcs`: cantidad de NPCs (de 2 a 16).

## Sistema de decisiones y aprendizaje

Cada ciclo se elige una interacción principal entre dos NPCs y una acción:

- `cooperar`
- `competir`
- `explorar`
- `negociar`

La decisión depende de rasgos + memoria social + experiencia acumulada.
Después de cada resultado, cambia la memoria y la experiencia, lo que modifica el comportamiento futuro.

## Verificación rápida de reproducibilidad

Ejecuta dos veces con la misma semilla y compara salida:

```bash
python3 simulacion_viva.py --semilla 99 --ticks 5 --pausa 0 --npcs 7 > run1.txt
python3 simulacion_viva.py --semilla 99 --ticks 5 --pausa 0 --npcs 7 > run2.txt
diff -u run1.txt run2.txt
```

Si `diff` no muestra cambios, la simulación es reproducible para esa configuración.
