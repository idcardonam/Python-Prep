#!/usr/bin/env python3
"""Pruebas del pipeline Power BI y del empaquetado de entrega."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import empaquetar_entrega
import procesar_powerbi


class ProcesarPowerBiTest(unittest.TestCase):
    def test_genera_tres_csv(self) -> None:
        ejemplo = Path(__file__).resolve().parent / "entrada" / "_ejemplos" / "google_admin.csv"
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            resumen = procesar_powerbi.procesar(ejemplo, out, licencias=100)
            self.assertGreater(resumen["total"], 0)
            self.assertTrue((out / "cuentas_powerbi.csv").is_file())
            self.assertTrue((out / "dependencias_powerbi.csv").is_file())
            self.assertTrue((out / "capacidad_powerbi.csv").is_file())
            cap = (out / "capacidad_powerbi.csv").read_text(encoding="utf-8-sig")
            self.assertIn("licencias_totales", cap)
            self.assertIn("100", cap)


class EmpaquetarTest(unittest.TestCase):
    def test_copia_solo_entrega(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            origen = Path(tmp) / "origen"
            dest = Path(tmp) / "dest"
            origen.mkdir()
            dest.mkdir()
            (origen / "cuentas_powerbi.csv").write_text("a\n", encoding="utf-8")
            (origen / "resumen.html").write_text("<html></html>", encoding="utf-8")
            (origen / "sin_2fa_ingenieria.csv").write_text("x\n", encoding="utf-8")
            (origen / "00_universo.csv").write_text("NO_SUBIR\n", encoding="utf-8")
            copiados = empaquetar_entrega.empaquetar(origen, dest)
            self.assertIn("cuentas_powerbi.csv", copiados)
            self.assertIn("resumen.html", copiados)
            self.assertIn("sin_2fa_ingenieria.csv", copiados)
            self.assertFalse((dest / "00_universo.csv").exists())
            self.assertTrue((dest / "LEAME_SUBIR_A_SHAREPOINT.txt").is_file())


if __name__ == "__main__":
    unittest.main()
