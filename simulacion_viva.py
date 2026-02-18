#!/usr/bin/env python3
"""Simulación viva de una historia emergente con NPCs que aprenden entre sí."""

from __future__ import annotations

import argparse
import random
import sys
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


NOMBRES = [
    "Aren", "Lyra", "Dante", "Mara", "Tarek", "Nira", "Orion", "Selene", "Kael", "Iris"
]
ROLES = [
    "ingeniera", "mercader", "guardiana", "curandero", "exploradora", "cronista", "mecánico", "oráculo"
]
LUGARES = [
    "la torre eólica", "el puerto de niebla", "la plaza de cobre", "el bosque de antenas", "el mercado nocturno"
]
EVENTOS_MUNDO = [
    "una tormenta magnética alteró la energía",
    "se encontró un mapa antiguo bajo la plaza",
    "la red de suministros colapsó por unas horas",
    "apareció un visitante desconocido con noticias del norte",
    "se activó una señal perdida desde el subsuelo",
]


@dataclass
class MemoriaSocial:
    confianza: float = 0.0
    deuda: float = 0.0
    friccion: float = 0.0
    eventos: List[str] = field(default_factory=list)


@dataclass
class NPC:
    nombre: str
    rol: str
    energia: float
    curiosidad: float
    empatia: float
    prudencia: float
    objetivo: str
    humor: float = 0.0
    recuerdos: Dict[str, MemoriaSocial] = field(default_factory=dict)
    experiencia: Dict[str, float] = field(default_factory=lambda: {"cooperar": 0.0, "competir": 0.0, "explorar": 0.0})

    def memoria_de(self, otro: str) -> MemoriaSocial:
        if otro not in self.recuerdos:
            self.recuerdos[otro] = MemoriaSocial()
        return self.recuerdos[otro]


class SimulacionViva:
    def __init__(self, semilla: Optional[int], num_npcs: int = 6):
        self.rng = random.Random(semilla)
        self.tick = 0
        self.lugar_actual = self.rng.choice(LUGARES)
        self.cronica: List[str] = []
        self.npcs = self._crear_npcs(num_npcs)

    def _crear_npcs(self, cantidad: int) -> List[NPC]:
        nombres = self.rng.sample(NOMBRES, k=min(cantidad, len(NOMBRES)))
        npcs = []
        for nombre in nombres:
            npcs.append(
                NPC(
                    nombre=nombre,
                    rol=self.rng.choice(ROLES),
                    energia=self.rng.uniform(0.55, 1.0),
                    curiosidad=self.rng.uniform(0.2, 1.0),
                    empatia=self.rng.uniform(0.1, 1.0),
                    prudencia=self.rng.uniform(0.1, 1.0),
                    objetivo=self.rng.choice([
                        "mantener a salvo la comunidad",
                        "descubrir secretos del subsuelo",
                        "acumular recursos estratégicos",
                        "probar una teoría arriesgada",
                        "conectar a facciones rivales",
                    ]),
                )
            )
        return npcs

    def _evento_global(self) -> Optional[str]:
        prob = 0.35
        if self.rng.random() <= prob:
            evento = self.rng.choice(EVENTOS_MUNDO)
            impacto = self.rng.uniform(-0.15, 0.2)
            for npc in self.npcs:
                ajuste = impacto * (0.4 + npc.prudencia)
                npc.humor = _clamp(npc.humor + ajuste, -1.0, 1.0)
                npc.energia = _clamp(npc.energia - abs(impacto) * 0.4, 0.0, 1.0)
            return evento
        return None

    def _elegir_accion(self, actor: NPC, objetivo: NPC) -> str:
        memoria = actor.memoria_de(objetivo.nombre)

        tendencia_cooperar = (
            actor.empatia * 0.6
            + memoria.confianza * 0.8
            - memoria.friccion * 0.5
            + actor.experiencia["cooperar"] * 0.2
            + self.rng.uniform(-0.2, 0.2)
        )
        tendencia_competir = (
            (1 - actor.empatia) * 0.4
            + memoria.deuda * 0.4
            + memoria.friccion * 0.9
            + actor.experiencia["competir"] * 0.2
            + self.rng.uniform(-0.2, 0.2)
        )
        tendencia_explorar = (
            actor.curiosidad * 0.8
            + (1 - actor.prudencia) * 0.3
            + actor.experiencia["explorar"] * 0.2
            + self.rng.uniform(-0.25, 0.25)
        )

        puntuaciones = {
            "cooperar": tendencia_cooperar,
            "competir": tendencia_competir,
            "explorar": tendencia_explorar,
        }
        return max(puntuaciones, key=puntuaciones.get)

    def _resolver_accion(self, actor: NPC, objetivo: NPC, accion: str) -> str:
        memoria_actor = actor.memoria_de(objetivo.nombre)
        memoria_objetivo = objetivo.memoria_de(actor.nombre)

        if accion == "cooperar":
            exito = self.rng.random() < (0.55 + actor.empatia * 0.3 + actor.energia * 0.15)
            if exito:
                mejora = self.rng.uniform(0.05, 0.18)
                memoria_actor.confianza = _clamp(memoria_actor.confianza + mejora, -1.0, 1.0)
                memoria_objetivo.confianza = _clamp(memoria_objetivo.confianza + mejora * 0.9, -1.0, 1.0)
                actor.energia = _clamp(actor.energia - 0.04, 0.0, 1.0)
                objetivo.energia = _clamp(objetivo.energia + 0.02, 0.0, 1.0)
                actor.humor = _clamp(actor.humor + 0.08, -1.0, 1.0)
                objetivo.humor = _clamp(objetivo.humor + 0.05, -1.0, 1.0)
                actor.experiencia["cooperar"] += 0.08
                evento = f"{actor.nombre} ayudó a {objetivo.nombre} y fortalecieron su alianza."
            else:
                memoria_actor.friccion = _clamp(memoria_actor.friccion + 0.07, 0.0, 1.0)
                actor.humor = _clamp(actor.humor - 0.06, -1.0, 1.0)
                actor.experiencia["cooperar"] += 0.03
                evento = f"{actor.nombre} intentó apoyar a {objetivo.nombre}, pero hubo un malentendido."

        elif accion == "competir":
            ventaja = actor.energia + (1 - actor.prudencia) * 0.2 + self.rng.uniform(-0.2, 0.2)
            defensa = objetivo.energia + objetivo.prudencia * 0.2
            exito = ventaja > defensa
            if exito:
                memoria_actor.deuda = _clamp(memoria_actor.deuda + 0.09, 0.0, 1.0)
                memoria_objetivo.friccion = _clamp(memoria_objetivo.friccion + 0.12, 0.0, 1.0)
                actor.energia = _clamp(actor.energia - 0.05, 0.0, 1.0)
                objetivo.energia = _clamp(objetivo.energia - 0.07, 0.0, 1.0)
                actor.humor = _clamp(actor.humor + 0.04, -1.0, 1.0)
                objetivo.humor = _clamp(objetivo.humor - 0.09, -1.0, 1.0)
                actor.experiencia["competir"] += 0.07
                evento = f"{actor.nombre} tomó ventaja sobre {objetivo.nombre} en una disputa de recursos."
            else:
                memoria_actor.friccion = _clamp(memoria_actor.friccion + 0.1, 0.0, 1.0)
                actor.energia = _clamp(actor.energia - 0.08, 0.0, 1.0)
                actor.humor = _clamp(actor.humor - 0.08, -1.0, 1.0)
                actor.experiencia["competir"] += 0.03
                evento = f"{actor.nombre} desafió a {objetivo.nombre}, pero terminó perdiendo influencia."

        else:  # explorar
            exito = self.rng.random() < (0.45 + actor.curiosidad * 0.35 - actor.prudencia * 0.1)
            if exito:
                hallazgo = self.rng.choice([
                    "un atajo seguro", "un lote de piezas útiles", "una pista histórica", "una señal encriptada"
                ])
                actor.energia = _clamp(actor.energia - 0.03, 0.0, 1.0)
                actor.humor = _clamp(actor.humor + 0.1, -1.0, 1.0)
                memoria_objetivo.deuda = _clamp(memoria_objetivo.deuda + 0.04, 0.0, 1.0)
                actor.experiencia["explorar"] += 0.09
                evento = f"{actor.nombre} exploró la zona y encontró {hallazgo}, beneficiando al grupo."
            else:
                actor.energia = _clamp(actor.energia - 0.09, 0.0, 1.0)
                actor.humor = _clamp(actor.humor - 0.11, -1.0, 1.0)
                memoria_actor.friccion = _clamp(memoria_actor.friccion + 0.05, 0.0, 1.0)
                actor.experiencia["explorar"] += 0.04
                evento = f"{actor.nombre} se internó en territorio inestable y regresó con contratiempos."

        memoria_actor.eventos.append(evento)
        if len(memoria_actor.eventos) > 12:
            memoria_actor.eventos = memoria_actor.eventos[-12:]

        return evento

    def _resumen_estado(self) -> str:
        lineas = [f"Estado de {self.lugar_actual}:"]
        for npc in sorted(self.npcs, key=lambda n: n.nombre):
            lineas.append(
                f"  - {npc.nombre} ({npc.rol}): energía={npc.energia:.2f}, humor={npc.humor:.2f}, objetivo={npc.objetivo}"
            )
        return "\n".join(lineas)

    def paso(self) -> List[str]:
        self.tick += 1
        salida = [f"\n--- Ciclo {self.tick} en {self.lugar_actual} ---"]

        if self.rng.random() < 0.20:
            self.lugar_actual = self.rng.choice(LUGARES)
            salida.append(f"La actividad principal se trasladó a {self.lugar_actual}.")

        evento_global = self._evento_global()
        if evento_global:
            salida.append(f"Evento global: {evento_global}.")

        actor, objetivo = self.rng.sample(self.npcs, 2)
        accion = self._elegir_accion(actor, objetivo)
        evento_local = self._resolver_accion(actor, objetivo, accion)
        salida.append(evento_local)

        for npc in self.npcs:
            recuperacion = 0.015 + npc.prudencia * 0.01
            npc.energia = _clamp(npc.energia + recuperacion, 0.0, 1.0)

        salida.append(self._resumen_estado())
        self.cronica.extend(salida)
        return salida


def _clamp(valor: float, minimo: float, maximo: float) -> float:
    return max(min(valor, maximo), minimo)


def ejecutar_simulacion(ticks: int, pausa: float, semilla: Optional[int], num_npcs: int) -> None:
    sim = SimulacionViva(semilla=semilla, num_npcs=num_npcs)

    print("=== Simulación viva iniciada ===")
    print("Los NPCs tomarán decisiones autónomas y aprenderán de sus interacciones.\n")

    for _ in range(ticks):
        for linea in sim.paso():
            print(linea)
        if pausa > 0:
            time.sleep(pausa)

    print("\n=== Fin de la simulación ===")


def _parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simulación narrativa en vivo con NPCs que aprenden y cambian su comportamiento."
    )
    parser.add_argument("--ticks", type=int, default=20, help="Cantidad de ciclos narrativos a ejecutar.")
    parser.add_argument("--pausa", type=float, default=0.8, help="Segundos de espera entre ciclos.")
    parser.add_argument("--semilla", type=int, default=None, help="Semilla para reproducibilidad.")
    parser.add_argument("--npcs", type=int, default=6, help="Cantidad de NPCs en la simulación (máx 10).")
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = _parse_args(argv)
    npcs = max(2, min(args.npcs, 10))
    ticks = max(1, args.ticks)
    pausa = max(0.0, args.pausa)

    ejecutar_simulacion(ticks=ticks, pausa=pausa, semilla=args.semilla, num_npcs=npcs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
