# Simulación Viva de Historia Emergente

Este proyecto ejecuta una simulación narrativa en tiempo real donde varios NPCs:

- toman decisiones autónomas (`cooperar`, `competir`, `explorar`),
- reaccionan a eventos globales aleatorios,
- guardan memoria social entre sí (confianza, fricción, deudas),
- y ajustan su comportamiento con una capa simple de aprendizaje por experiencia.

## Ejecutar

```bash
python3 simulacion_viva.py --ticks 30 --pausa 0.6 --semilla 42 --npcs 6
```

### Parámetros

- `--ticks`: cantidad de ciclos narrativos.
- `--pausa`: segundos entre ciclos (0 para ejecución rápida sin pausa).
- `--semilla`: número entero opcional para reproducir resultados.
- `--npcs`: cantidad de NPCs (entre 2 y 10).

## Idea de "en vivo"

La simulación se imprime en consola ciclo por ciclo, como una narración continua. Cada ciclo muestra:

1. cambios globales del mundo,
2. acción principal entre NPCs,
3. estado actualizado de cada NPC.

Si deseas extenderlo con IA generativa real (LLM), puedes cambiar la lógica de `_elegir_accion` para consultar un modelo externo por cada NPC en cada ciclo.
