#!/usr/bin/env python3
"""Pruebas con datos sintéticos. No usa CSV reales ni PII."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import cruzar


BANNER_HEADERS = [
    "PERIODO",
    "ID",
    "APELLIDOS",
    "NOMBRE",
    "ESCUELA",
    "PROGRAMA",
    "PROGRAMA_WEB",
    "NIVEL",
    "EMAIL",
    "EST_ACAD",
    "INSCRIP_STATUS",
    "CANT_CURSOS",
    "CORREO_UNAB",
    "CORREO_PERSONAL",
]


class MapeoTest(unittest.TestCase):
    def test_banner_exact_columns(self) -> None:
        m = cruzar.map_columns(BANNER_HEADERS, cruzar.ACADEMICO_ALIASES)
        self.assertEqual(m["email"], "CORREO_UNAB")
        self.assertEqual(m["estado"], "EST_ACAD")
        self.assertEqual(m["facultad"], "ESCUELA")
        self.assertEqual(m["programa"], "PROGRAMA")
        self.assertIsNone(m["seccion"])
        self.assertEqual(m["codigo"], "ID")
        self.assertEqual(m["nombres"], "NOMBRE")

    def test_google_2sv_enrolled(self) -> None:
        headers = [
            "First Name [Required]",
            "Last Name [Required]",
            "Email Address [Required]",
            "Status [READ ONLY]",
            "Last Sign In [READ ONLY]",
            "2sv Enrolled [READ ONLY]",
        ]
        m = cruzar.map_columns(headers, cruzar.GOOGLE_ALIASES)
        self.assertEqual(m["email"], "Email Address [Required]")
        self.assertEqual(m["2fa_inscrito"], "2sv Enrolled [READ ONLY]")
        self.assertIsNone(m["ou"])
        self.assertIsNone(m["2fa_forzado"])

    def test_2fa_true_false(self) -> None:
        self.assertTrue(cruzar.is_2fa_on("True", ""))
        self.assertFalse(cruzar.is_2fa_on("False", "On"))
        self.assertFalse(cruzar.is_2fa_on("0", ""))

    def test_titulos_informe_config(self) -> None:
        t = cruzar.titulos_informe({"informe": {"resumen": "Solo resumen"}})
        self.assertEqual(t["resumen"], "Solo resumen")
        self.assertEqual(t["h1"], cruzar.TITULOS_INFORME["h1"])

    def test_google_datetime(self) -> None:
        dt = cruzar.parse_date("2026/08/27 15:15:08")
        self.assertIsNotNone(dt)
        self.assertEqual(dt.year, 2026)
        self.assertIsNone(cruzar.parse_date("Never logged in"))


class CsvIoTest(unittest.TestCase):
    def test_semicolon_and_skip_google(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "Prematriculados_E_Inscritos 202610.csv").write_text(
                "CORREO_UNAB;EST_ACAD;ESCUELA;PROGRAMA;NOMBRE;APELLIDOS\n"
                "ana@unab.edu.co;ACTIVO;Ing;Sistemas;Ana;Perez\n",
                encoding="utf-8",
            )
            (d / "User_Download_01092026_140316.csv").write_text(
                "First Name [Required],Email Address [Required],2sv Enrolled [READ ONLY]\n"
                "X,x@unab.edu.co,False\n",
                encoding="utf-8",
            )
            files = cruzar.listar_csv_academico(d)
            self.assertEqual(len(files), 1)
            headers, rows = cruzar.read_csv(files[0])
            self.assertIn("CORREO_UNAB", headers)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["EST_ACAD"], "ACTIVO")

    def test_cruzar_ejemplo_and_synth(self) -> None:
        root = Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"
            cruzar.cruzar(
                root / "entrada" / "_ejemplos" / "google_admin.csv",
                root / "entrada" / "_ejemplos" / "academico.csv",
                root / "entrada" / "_ejemplos" / "personal.csv",
                out,
                cruzar.load_config(root / "config.example.yaml"),
            )
            resumen = json.loads((out / "resumen.json").read_text(encoding="utf-8"))
            self.assertGreater(resumen["n_google"], 0)
            self.assertTrue((out / "02_estudiantes_sin_2fa.csv").exists())

        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            g = d / "g.csv"
            g.write_text(
                "First Name [Required],Last Name [Required],Email Address [Required],"
                "Status [READ ONLY],Last Sign In [READ ONLY],2sv Enrolled [READ ONLY]\n"
                "Ana,Perez,ana@unab.edu.co,Active,2026/08/20 10:00:00,False\n"
                "Luis,Gomez,luis@unab.edu.co,Active,Never logged in,True\n"
                "Doc,Ente,doc@unab.edu.co,Active,2026/08/20 10:00:00,False\n",
                encoding="utf-8",
            )
            acad_dir = d / "acad"
            acad_dir.mkdir()
            (acad_dir / "Prematriculados 202610.csv").write_text(
                "CORREO_UNAB,EST_ACAD,ESCUELA,PROGRAMA,NOMBRE,APELLIDOS,ID\n"
                "ana@unab.edu.co,ACTIVO,Ingenieria,Sistemas,Ana,Perez,1\n"
                "ana@unab.edu.co,ACTIVO,Economia,Admin,Ana,Perez,1\n"
                "egre@unab.edu.co,EGRESADO,Ingenieria,Sistemas,E,G,2\n",
                encoding="utf-8",
            )
            (acad_dir / "User_Download_fake.csv").write_text(
                "Email Address [Required],2sv Enrolled [READ ONLY]\nskip@unab.edu.co,False\n",
                encoding="utf-8",
            )
            out = d / "out"
            cruzar.cruzar(
                g,
                None,
                None,
                out,
                cruzar.load_config(None),
                academico_dir=acad_dir,
            )
            resumen = json.loads((out / "resumen.json").read_text(encoding="utf-8"))
            self.assertEqual(resumen["n_google"], 3)
            self.assertEqual(resumen["n_match_estudiante"], 1)
            self.assertEqual(resumen["graduados_filtrados_en_academico"], 1)
            with (out / "00_universo.csv").open(encoding="utf-8-sig", newline="") as fh:
                rows = list(__import__("csv").DictReader(fh))
            ana = next(r for r in rows if r["correo"] == "ana@unab.edu.co")
            self.assertEqual(ana["tiene_2fa"], "NO")
            self.assertIn("Ingenieria", ana["a_facultad"])
            self.assertIn("Economia", ana["a_facultad"])
            self.assertEqual(ana["prioridad_2fa"], "ALTA_ESTUDIANTE_ACTIVO_SIN_2FA")
            doc = next(r for r in rows if r["correo"] == "doc@unab.edu.co")
            self.assertEqual(doc["perfil"], "GOOGLE_SIN_MATCH_ACADEMICO")

    def test_carpeta_inexistente_mensaje_claro(self) -> None:
        with self.assertRaises(SystemExit) as ctx:
            cruzar.descubrir_fuentes(Path("/no/existe/esta/carpeta"))
        self.assertIn("No existe esa carpeta", str(ctx.exception))

    def test_curriculo_ultimo_periodo_y_skip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "Prematriculados 202610.csv").write_text(
                "CORREO_UNAB,EST_ACAD,ESCUELA,PROGRAMA,COD_PROG,COD_MAJR,NOMBRE,APELLIDOS\n"
                "ana@unab.edu.co,ACTIVO,Ingenieria,Sistemas,SIS,SIS,Ana,Perez\n",
                encoding="utf-8",
            )
            (d / "VISTA DE CURRICULO.csv").write_text(
                "PERIODO,COD_ESC,ESCUELA,COD_MAJR,COD_PROG,PROGRAMA,PLAN,NIVEL,TIPO\n"
                "202010,ING,Ingenieria,SIS,SIS,Sistemas,Plan viejo,Pregrado,Formal\n"
                "202610,ING,Ingenieria,SIS,SIS,Sistemas,Plan MEN 2026,Pregrado,Formal\n",
                encoding="utf-8",
            )
            self.assertEqual(len(cruzar.listar_csv_academico(d)), 1)
            self.assertEqual(len(cruzar.listar_csv_curriculo(d)), 1)
            g = d / "g.csv"
            g.write_text(
                "First Name [Required],Last Name [Required],Email Address [Required],"
                "Status [READ ONLY],Last Sign In [READ ONLY],2sv Enrolled [READ ONLY]\n"
                "Ana,Perez,ana@unab.edu.co,Active,2026/08/20 10:00:00,False\n",
                encoding="utf-8",
            )
            out = d / "out"
            cruzar.cruzar(g, None, None, out, cruzar.load_config(None), academico_dir=d)
            resumen = json.loads((out / "resumen.json").read_text(encoding="utf-8"))
            self.assertEqual(resumen["n_filas_curriculo"], 2)
            self.assertEqual(resumen["n_planes_vigentes"], 1)
            self.assertEqual(resumen["n_estudiantes_sin_2fa"], 1)
            with (out / "00_universo.csv").open(encoding="utf-8-sig", newline="") as fh:
                rows = list(__import__("csv").DictReader(fh))
            ana = rows[0]
            self.assertEqual(ana["c_match"], "SI")
            self.assertEqual(ana["c_periodo_vigente"], "202610")
            self.assertEqual(ana["c_plan"], "Plan MEN 2026")
            html = (out / "resumen.html").read_text(encoding="utf-8")
            self.assertIn(">Resumen<", html)
            self.assertNotIn("Resumen para jefatura", html)
            self.assertIn("Pendientes", html)
            self.assertIn("ana@unab.edu.co", html)
            self.assertIn("Sistemas", html)
            self.assertIn("Elija una facultad", html)
            self.assertIn("sel-fac", html)
            self.assertIn("Descargar esta facultad", html)
            self.assertIn("irAPrograma", html)
            lista = (out / "listado_sin_2fa.html").read_text(encoding="utf-8")
            self.assertIn("ana@unab.edu.co", lista)
            with (out / "02_estudiantes_sin_2fa.csv").open(encoding="utf-8-sig", newline="") as fh:
                camp = list(__import__("csv").DictReader(fh))
            self.assertEqual(camp[0]["correo"], "ana@unab.edu.co")
            self.assertEqual(camp[0]["facultad"], "Ingenieria")
            self.assertEqual(camp[0]["programa"], "Sistemas")

    def test_xlsx_term_es_periodo_vigente(self) -> None:
        from openpyxl import Workbook

        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            wb = Workbook()
            ws = wb.active
            ws.title = "Exportar Hoja de Trabajo"
            ws.append(
                [
                    "TERM_EFF",
                    "COD_ESCUELA",
                    "DESC_ESCUELA",
                    "COD_PROG",
                    "DESC_PROG",
                    "COD_MAJR",
                    "NIVEL_DESC",
                    "TERM",
                    "DESC_CAMP",
                ]
            )
            ws.append(["200800", "FI", "FAC DE INGENIERIA", "SIS", "Ingenieria de Sistemas", "SIS", "PREGRADO PROFESIONAL", "201010", "CC"])
            ws.append(["200800", "FI", "FAC DE INGENIERIA", "SIS", "Ingenieria de Sistemas", "SIS", "PREGRADO PROFESIONAL", "202610", "CC"])
            xlsx = d / "VISTA DE CURRICULO.xlsx"
            wb.save(xlsx)
            headers, rows = cruzar.read_xlsx(xlsx)
            m = cruzar.map_columns(headers, cruzar.CURRICULO_ALIASES)
            self.assertEqual(m["periodo"], "TERM")
            self.assertEqual(m["periodo_efectivo"], "TERM_EFF")
            self.assertEqual(m["escuela"], "DESC_ESCUELA")
            self.assertEqual(m["programa"], "DESC_PROG")
            cat, _, n = cruzar.cargar_catalogo_curriculo([xlsx])
            self.assertEqual(n, 2)
            plan = cruzar.buscar_plan(cat, "SIS", "SIS", "Ingenieria de Sistemas", "FAC DE INGENIERIA")
            self.assertEqual(plan.get("periodo"), "202610")


if __name__ == "__main__":
    unittest.main()
