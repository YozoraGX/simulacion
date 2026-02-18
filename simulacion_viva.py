#!/usr/bin/env python3
"""Simulación viva compleja con historia emergente 100% reproducible por semilla."""

from __future__ import annotations

import argparse
import random
import sys
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


NOMBRES = [
    "Aren", "Lyra", "Dante", "Mara", "Tarek", "Nira", "Orion", "Selene", "Kael", "Iris",
    "Vega", "Rhea", "Noam", "Zara", "Eli", "Bran"
]
ROLES = [
    "ingeniera", "mercader", "guardiana", "curandero", "exploradora", "cronista", "mecánico", "oráculo"
]
LUGARES_BASE = [
    "la torre eólica", "el puerto de niebla", "la plaza de cobre", "el bosque de antenas", "el mercado nocturno",
    "el barrio hidráulico", "el anillo subterráneo", "la estación de vidrio"
]
OBJETIVOS_BASE = [
    "mantener a salvo la comunidad",
    "descubrir secretos del subsuelo",
    "acumular recursos estratégicos",
    "probar una teoría arriesgada",
    "conectar a facciones rivales",
    "recuperar conocimiento perdido",
]


@dataclass
class MemoriaSocial:
    confianza: float = 0.0
    deuda: float = 0.0
    friccion: float = 0.0
    eventos: List[str] = field(default_factory=list)


@dataclass
class Faccion:
    nombre: str
    doctrina: str
    recurso_clave: str
    cohesion: float


@dataclass
class NPC:
    nombre: str
    rol: str
    faccion: str
    energia: float
    curiosidad: float
    empatia: float
    prudencia: float
    ambicion: float
    objetivo: str
    humor: float = 0.0
    recuerdos: Dict[str, MemoriaSocial] = field(default_factory=dict)
    experiencia: Dict[str, float] = field(
        default_factory=lambda: {"cooperar": 0.0, "competir": 0.0, "explorar": 0.0, "negociar": 0.0}
    )

    def memoria_de(self, otro: str) -> MemoriaSocial:
        if otro not in self.recuerdos:
            self.recuerdos[otro] = MemoriaSocial()
        return self.recuerdos[otro]


class SimulacionViva:
    def __init__(self, semilla: int, num_npcs: int = 8):
        self.semilla = semilla
        self.rng = random.Random(semilla)
        self.tick = 0

        self.lugares = self._generar_lugares()
        self.facciones = self._generar_facciones()
        self.eventos_mundo = self._generar_eventos_mundo()

        self.lugar_actual = self.rng.choice(self.lugares)
        self.cronica: List[str] = []
        self.npcs = self._crear_npcs(num_npcs)
        self._sembrar_relaciones_iniciales()

    def _generar_lugares(self) -> List[str]:
        lugares = self.rng.sample(LUGARES_BASE, k=min(len(LUGARES_BASE), 6))
        return lugares

    def _generar_facciones(self) -> List[Faccion]:
        doctrinas = ["pragmatismo técnico", "solidaridad comunal", "expansión estratégica", "conservación del saber"]
        recursos = ["energía", "agua", "datos", "componentes", "medicina", "rutas"]
        prefijos = ["Consorcio", "Círculo", "Comuna", "Pacto", "Liga", "Nexo"]
        sufijos = ["Aurora", "Delta", "Hélice", "Norte", "Ferro", "Sombra"]

        facciones = []
        nombres_usados = set()
        while len(facciones) < 3:
            nombre = f"{self.rng.choice(prefijos)} {self.rng.choice(sufijos)}"
            if nombre in nombres_usados:
                continue
            nombres_usados.add(nombre)
            facciones.append(
                Faccion(
                    nombre=nombre,
                    doctrina=self.rng.choice(doctrinas),
                    recurso_clave=self.rng.choice(recursos),
                    cohesion=self.rng.uniform(0.35, 0.95),
                )
            )
        return facciones

    def _generar_eventos_mundo(self) -> List[str]:
        plantillas = [
            "una tormenta magnética alteró {recurso}",
            "se detectó una señal antigua en {lugar}",
            "se interrumpió la distribución de {recurso}",
            "apareció una caravana con mapas de {lugar}",
            "una disputa entre facciones tensó el acceso a {recurso}",
            "se descubrió una cámara sellada bajo {lugar}",
        ]
        recursos = [f.recurso_clave for f in self.facciones]
        eventos = []
        for plantilla in plantillas:
            eventos.append(
                plantilla.format(
                    recurso=self.rng.choice(recursos),
                    lugar=self.rng.choice(self.lugares),
                )
            )
        return eventos

    def _crear_npcs(self, cantidad: int) -> List[NPC]:
        cantidad = max(2, min(cantidad, len(NOMBRES)))
        nombres = self.rng.sample(NOMBRES, k=cantidad)
        npcs = []
        for nombre in nombres:
            faccion = self.rng.choice(self.facciones)
            npcs.append(
                NPC(
                    nombre=nombre,
                    rol=self.rng.choice(ROLES),
                    faccion=faccion.nombre,
                    energia=self.rng.uniform(0.5, 1.0),
                    curiosidad=self.rng.uniform(0.2, 1.0),
                    empatia=self.rng.uniform(0.1, 1.0),
                    prudencia=self.rng.uniform(0.1, 1.0),
                    ambicion=self.rng.uniform(0.1, 1.0),
                    objetivo=self.rng.choice(OBJETIVOS_BASE),
                )
            )
        return npcs

    def _sembrar_relaciones_iniciales(self) -> None:
        for i, npc_a in enumerate(self.npcs):
            for npc_b in self.npcs[i + 1:]:
                if self.rng.random() < 0.45:
                    base = self.rng.uniform(-0.15, 0.2)
                    mem_a = npc_a.memoria_de(npc_b.nombre)
                    mem_b = npc_b.memoria_de(npc_a.nombre)
                    mem_a.confianza = _clamp(base, -1.0, 1.0)
                    mem_b.confianza = _clamp(base * self.rng.uniform(0.8, 1.2), -1.0, 1.0)
                    if base < 0:
                        mem_a.friccion = abs(base)
                        mem_b.friccion = abs(base) * 0.9

    def _evento_global(self) -> Optional[str]:
        if self.rng.random() > 0.4:
            return None

        evento = self.rng.choice(self.eventos_mundo)
        impacto = self.rng.uniform(-0.2, 0.2)
        for npc in self.npcs:
            sensibilidad = 0.5 + npc.ambicion * 0.2 - npc.prudencia * 0.1
            npc.humor = _clamp(npc.humor + impacto * sensibilidad, -1.0, 1.0)
            npc.energia = _clamp(npc.energia - abs(impacto) * (0.25 + npc.ambicion * 0.1), 0.0, 1.0)
        return evento

    def _elegir_accion(self, actor: NPC, objetivo: NPC) -> str:
        memoria = actor.memoria_de(objetivo.nombre)

        tendencias = {
            "cooperar": (
                actor.empatia * 0.55
                + memoria.confianza * 0.8
                - memoria.friccion * 0.5
                + actor.experiencia["cooperar"] * 0.25
                + self.rng.uniform(-0.2, 0.2)
            ),
            "competir": (
                actor.ambicion * 0.6
                + memoria.friccion * 0.8
                + actor.experiencia["competir"] * 0.25
                + self.rng.uniform(-0.2, 0.2)
            ),
            "explorar": (
                actor.curiosidad * 0.75
                + (1 - actor.prudencia) * 0.2
                + actor.experiencia["explorar"] * 0.25
                + self.rng.uniform(-0.2, 0.2)
            ),
            "negociar": (
                actor.prudencia * 0.45
                + actor.empatia * 0.25
                + actor.experiencia["negociar"] * 0.3
                + (0.1 if actor.faccion != objetivo.faccion else -0.05)
                + self.rng.uniform(-0.2, 0.2)
            ),
        }
        return max(tendencias, key=tendencias.get)

    def _resolver_accion(self, actor: NPC, objetivo: NPC, accion: str) -> str:
        memoria_actor = actor.memoria_de(objetivo.nombre)
        memoria_objetivo = objetivo.memoria_de(actor.nombre)

        if accion == "cooperar":
            exito = self.rng.random() < (0.5 + actor.empatia * 0.25 + actor.energia * 0.2)
            if exito:
                incremento = self.rng.uniform(0.06, 0.18)
                memoria_actor.confianza = _clamp(memoria_actor.confianza + incremento, -1.0, 1.0)
                memoria_objetivo.confianza = _clamp(memoria_objetivo.confianza + incremento * 0.85, -1.0, 1.0)
                actor.humor = _clamp(actor.humor + 0.09, -1.0, 1.0)
                objetivo.humor = _clamp(objetivo.humor + 0.05, -1.0, 1.0)
                actor.energia = _clamp(actor.energia - 0.04, 0.0, 1.0)
                actor.experiencia["cooperar"] += 0.08
                evento = f"{actor.nombre} colaboró con {objetivo.nombre}; la confianza entre ambos subió."
            else:
                memoria_actor.friccion = _clamp(memoria_actor.friccion + 0.08, 0.0, 1.0)
                actor.humor = _clamp(actor.humor - 0.07, -1.0, 1.0)
                actor.experiencia["cooperar"] += 0.03
                evento = f"{actor.nombre} intentó cooperar con {objetivo.nombre}, pero surgieron desacuerdos."

        elif accion == "competir":
            poder_actor = actor.energia + actor.ambicion * 0.25 + self.rng.uniform(-0.15, 0.15)
            poder_objetivo = objetivo.energia + objetivo.prudencia * 0.2
            exito = poder_actor > poder_objetivo
            if exito:
                memoria_actor.deuda = _clamp(memoria_actor.deuda + 0.1, 0.0, 1.0)
                memoria_objetivo.friccion = _clamp(memoria_objetivo.friccion + 0.14, 0.0, 1.0)
                actor.humor = _clamp(actor.humor + 0.05, -1.0, 1.0)
                objetivo.humor = _clamp(objetivo.humor - 0.1, -1.0, 1.0)
                actor.energia = _clamp(actor.energia - 0.06, 0.0, 1.0)
                actor.experiencia["competir"] += 0.08
                evento = f"{actor.nombre} ganó una disputa frente a {objetivo.nombre} por recursos críticos."
            else:
                memoria_actor.friccion = _clamp(memoria_actor.friccion + 0.09, 0.0, 1.0)
                actor.humor = _clamp(actor.humor - 0.09, -1.0, 1.0)
                actor.energia = _clamp(actor.energia - 0.08, 0.0, 1.0)
                actor.experiencia["competir"] += 0.03
                evento = f"{actor.nombre} perdió influencia al competir con {objetivo.nombre}."

        elif accion == "explorar":
            exito = self.rng.random() < (0.4 + actor.curiosidad * 0.35 + actor.energia * 0.15 - actor.prudencia * 0.1)
            if exito:
                hallazgo = self.rng.choice(["un archivo histórico", "un corredor seguro", "piezas raras", "una señal codificada"])
                actor.humor = _clamp(actor.humor + 0.11, -1.0, 1.0)
                actor.energia = _clamp(actor.energia - 0.05, 0.0, 1.0)
                memoria_objetivo.deuda = _clamp(memoria_objetivo.deuda + 0.05, 0.0, 1.0)
                actor.experiencia["explorar"] += 0.09
                evento = f"{actor.nombre} exploró y halló {hallazgo}, favoreciendo al asentamiento."
            else:
                actor.humor = _clamp(actor.humor - 0.12, -1.0, 1.0)
                actor.energia = _clamp(actor.energia - 0.1, 0.0, 1.0)
                memoria_actor.friccion = _clamp(memoria_actor.friccion + 0.05, 0.0, 1.0)
                actor.experiencia["explorar"] += 0.04
                evento = f"{actor.nombre} regresó de explorar sin resultados y con daños menores."

        else:  # negociar
            base = 0.45 + actor.prudencia * 0.2 + actor.empatia * 0.2 - memoria_actor.friccion * 0.2
            if actor.faccion != objetivo.faccion:
                base += 0.08
            exito = self.rng.random() < base
            if exito:
                memoria_actor.confianza = _clamp(memoria_actor.confianza + 0.09, -1.0, 1.0)
                memoria_objetivo.confianza = _clamp(memoria_objetivo.confianza + 0.07, -1.0, 1.0)
                memoria_actor.friccion = _clamp(memoria_actor.friccion - 0.06, 0.0, 1.0)
                actor.humor = _clamp(actor.humor + 0.07, -1.0, 1.0)
                actor.experiencia["negociar"] += 0.08
                evento = f"{actor.nombre} negoció con {objetivo.nombre} y redujeron tensiones entre facciones."
            else:
                memoria_actor.friccion = _clamp(memoria_actor.friccion + 0.07, 0.0, 1.0)
                actor.humor = _clamp(actor.humor - 0.05, -1.0, 1.0)
                actor.experiencia["negociar"] += 0.03
                evento = f"{actor.nombre} no logró un acuerdo con {objetivo.nombre}; el diálogo quedó abierto."

        memoria_actor.eventos.append(evento)
        if len(memoria_actor.eventos) > 20:
            memoria_actor.eventos = memoria_actor.eventos[-20:]
        return evento

    def _actualizar_objetivos(self) -> None:
        for npc in self.npcs:
            if npc.experiencia["explorar"] > 0.35 and self.rng.random() < 0.15:
                npc.objetivo = "cartografiar rutas seguras"
            elif npc.experiencia["cooperar"] > 0.35 and self.rng.random() < 0.15:
                npc.objetivo = "consolidar alianzas estables"
            elif npc.experiencia["competir"] > 0.35 and self.rng.random() < 0.15:
                npc.objetivo = "asegurar ventaja táctica"

    def _resumen_facciones(self) -> str:
        lineas = ["Facciones activas:"]
        for fac in self.facciones:
            lineas.append(
                f"  - {fac.nombre}: doctrina={fac.doctrina}, recurso={fac.recurso_clave}, cohesión={fac.cohesion:.2f}"
            )
        return "\n".join(lineas)

    def _resumen_estado(self) -> str:
        lineas = [f"Estado de {self.lugar_actual}:"]
        for npc in sorted(self.npcs, key=lambda n: n.nombre):
            lineas.append(
                "  - "
                f"{npc.nombre} ({npc.rol}, {npc.faccion}): energía={npc.energia:.2f}, humor={npc.humor:.2f}, "
                f"objetivo={npc.objetivo}"
            )
        return "\n".join(lineas)

    def paso(self) -> List[str]:
        self.tick += 1
        salida = [f"\n--- Ciclo {self.tick} en {self.lugar_actual} ---"]

        if self.rng.random() < 0.25:
            self.lugar_actual = self.rng.choice(self.lugares)
            salida.append(f"La actividad principal se desplazó a {self.lugar_actual}.")

        evento_global = self._evento_global()
        if evento_global:
            salida.append(f"Evento global: {evento_global}.")

        actor, objetivo = self.rng.sample(self.npcs, 2)
        accion = self._elegir_accion(actor, objetivo)
        evento_local = self._resolver_accion(actor, objetivo, accion)
        salida.append(f"Acción elegida: {accion}.")
        salida.append(evento_local)

        for npc in self.npcs:
            recuperacion = 0.012 + npc.prudencia * 0.015
            npc.energia = _clamp(npc.energia + recuperacion, 0.0, 1.0)

        self._actualizar_objetivos()
        salida.append(self._resumen_estado())
        self.cronica.extend(salida)
        return salida


def _clamp(valor: float, minimo: float, maximo: float) -> float:
    return max(min(valor, maximo), minimo)


def ejecutar_simulacion(ticks: int, pausa: float, semilla: int, num_npcs: int) -> None:
    sim = SimulacionViva(semilla=semilla, num_npcs=num_npcs)

    print("=== Simulación viva compleja iniciada ===")
    print(f"Semilla activa: {semilla}")
    print(sim._resumen_facciones())
    print("\nLos NPCs decidirán en cada ciclo y aprenderán de sus relaciones.\n")

    for _ in range(ticks):
        for linea in sim.paso():
            print(linea)
        if pausa > 0:
            time.sleep(pausa)

    print("\n=== Fin de la simulación ===")


def _parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simulación narrativa en vivo con mundo reproducible por semilla y NPCs adaptativos."
    )
    parser.add_argument("--ticks", type=int, default=25, help="Cantidad de ciclos narrativos a ejecutar.")
    parser.add_argument("--pausa", type=float, default=0.6, help="Segundos de espera entre ciclos.")
    parser.add_argument("--semilla", type=int, required=True, help="Semilla obligatoria para generar todo el mundo.")
    parser.add_argument("--npcs", type=int, default=8, help="Cantidad de NPCs (entre 2 y 16).")
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = _parse_args(argv)
    npcs = max(2, min(args.npcs, 16))
    ticks = max(1, args.ticks)
    pausa = max(0.0, args.pausa)

    ejecutar_simulacion(ticks=ticks, pausa=pausa, semilla=args.semilla, num_npcs=npcs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
