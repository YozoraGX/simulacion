# Simulación Viva de Historia Emergente

Este proyecto ejecuta una simulación narrativa en tiempo real donde varios NPCs:

- toman decisiones autónomas (`cooperar`, `competir`, `explorar`),
- reaccionan a eventos globales aleatorios,
- guardan memoria social entre sí (confianza, fricción, deudas),
- ajustan su comportamiento con aprendizaje por experiencia,
- y pueden consultar un modelo local en **LM Studio** para decidir acciones.

## Ejecutar

```bash
python3 simulacion_viva.py --ticks 30 --pausa 0.6 --semilla 42 --npcs 6
```

### Parámetros

- `--ticks`: cantidad de ciclos narrativos.
- `--pausa`: segundos entre ciclos (0 para ejecución rápida sin pausa).
- `--semilla`: número entero opcional para reproducir resultados.
- `--npcs`: cantidad de NPCs (entre 2 y 10).
- `--usar-ia`: activa decisiones por LLM (LM Studio).
- `--lm-studio-url`: endpoint OpenAI-compatible de LM Studio.
- `--modelo`: nombre del modelo cargado en LM Studio.

## Usar LM Studio para simulación compleja

1. Abre LM Studio, carga un modelo y activa el servidor local (API compatible con OpenAI).
2. Ejecuta la simulación con IA:

```bash
python3 simulacion_viva.py \
  --ticks 40 \
  --pausa 0.3 \
  --npcs 8 \
  --usar-ia \
  --modelo "nombre-de-tu-modelo" \
  --lm-studio-url "http://127.0.0.1:1234/v1/chat/completions"
```

### Qué se añadió para un "pueblo vivo"

- Cada NPC tiene una **rutina base** personal.
- El mundo avanza por **fases del día** (`amanecer`, `mañana`, `tarde`, `anochecer`, `noche`).
- Si está activa la IA, cada decisión de NPC consulta el LLM con contexto de:
  - fase actual,
  - estado emocional,
  - energía,
  - rol y rutina.
- Si LM Studio no responde, la simulación usa automáticamente la lógica local como fallback.

## Idea de "en vivo"

La simulación se imprime en consola ciclo por ciclo, como una narración continua. Cada ciclo muestra:

1. fase del día y cambios globales,
2. acción principal entre NPCs,
3. estado actualizado de cada NPC.

Si deseas extenderlo aún más, puedes incluir:

- sistema de profesiones con horarios más estrictos,
- economía local (oferta/demanda),
- familias, facciones y reputación por barrios,
- eventos estacionales y clima dinámico.
