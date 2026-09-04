<?php
/**
 * Plantilla de módulo MiPortalU (Julián Ojeda) — referencia para Disponibilidad de Aulas.
 * Las 4 capas: módulo (esta vista) + clase en gestionContenidos/clases + assets + datos Banner.
 */
include("../../include/headerInt.inc");
include("../../include/lateralIzqInt.inc");

include($_SERVER["DOCUMENT_ROOT"]."/gestionContenidos/clases/nuevaClase.php");
$nuevaClase = new NuevaClase();

?>
<link rel="stylesheet" type="text/css" href="/assets/css/fontAwesome-6.5.2/css/all.css">
<script src="/assets/js/sweetalert2.all.min.js"></script>
<div id="desarrollo-contenidos">
	<div id="conten_central">
		<h1>TITULO DE LA PAGINA</h1>
		<!-- ACA VA TODA LA LOGICA DE LA PAGINA (PHP - HTML)-->
	</div>
</div>
<?php
include("../../include/footerInt.inc");
?>
