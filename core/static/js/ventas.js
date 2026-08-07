

document.addEventListener("DOMContentLoaded", () => {

  const LLAVE_HISTORIAL = "historialProductos";
  const LLAVE_VENTA_ACTUAL = "ventaActual";

  const botonAgregarProducto = document.getElementById("botonAgregarProducto");
  const botonProcesarVenta = document.getElementById("botonProcesarVenta");
  const tabNuevaVenta = document.getElementById("tabNuevaVenta");
  const tabHistorial = document.getElementById("tabHistorial");

  const cuerpoTablaVenta = document.querySelector("#tablaVenta tbody");
  const cuerpoTablaHistorial = document.querySelector("#tablaHistorialMini tbody");

  const formularioVenta = document.getElementById("formularioVenta");
  const historialPanel = document.getElementById("historialPanel");

  const inputSku = document.getElementById("sku");
  const inputProducto = document.getElementById("producto");
  const inputCantidad = document.getElementById("cantidad");
  const inputPrecio = document.getElementById("precio");

  const textoSubtotal = document.querySelector(".subtotal");
  const textoItbis = document.querySelector(".itbis");
  const textoTotal = document.querySelector(".total");


  /* ============================================================
     SECCION 1: ARRANQUE DE LA PAGINA
     El historial de productos ahora viene de la base de datos
     (Django lo incrusta en la pagina como JSON). La "venta actual"
     (el carrito en curso) vive solo en memoria mientras la pagina
     esta abierta; se guarda de verdad en la base de datos recien
     cuando se le da a "Procesar Venta".
     ============================================================ */
  function leerHistorialInicial() {
    const elemento = document.getElementById("historial-data");
    if (!elemento) return [];
    try {
      return JSON.parse(elemento.textContent);
    } catch (error) {
      console.error("No se pudo leer el historial inicial:", error);
      return [];
    }
  }

  let listaHistorial = leerHistorialInicial();
  let listaVentaActual = [];

  dibujarTablaHistorialCompleta();
  dibujarTablaVentaCompleta();
  recalcularResumenVenta();


  /* ============================================================
     SECCION 2: CAMBIO DE PESTAÑAS (Nueva Venta / Historial)
     ============================================================ */

  // Esta función hace lo siguiente:
  // 1. Marca la pestaña "Nueva Venta" como activa
  // 2. Muestra el formulario y la tabla de venta
  // 3. Oculta el panel de historial
  function mostrarPestanaNuevaVenta() {
    tabNuevaVenta.classList.add("active");
    tabHistorial.classList.remove("active");

    formularioVenta.style.display = "block";
    historialPanel.classList.remove("show");
  }

  // Esta función hace lo siguiente:
  // 1. Marca la pestaña "Historial" como activa
  // 2. Oculta el formulario de venta
  // 3. Muestra el panel de historial con animación
  function mostrarPestanaHistorial() {
    tabHistorial.classList.add("active");
    tabNuevaVenta.classList.remove("active");

    formularioVenta.style.display = "none";
    historialPanel.classList.add("show");
  }

  tabNuevaVenta.addEventListener("click", mostrarPestanaNuevaVenta);
  tabHistorial.addEventListener("click", mostrarPestanaHistorial);


  /* ============================================================
     SECCION 3: AGREGAR PRODUCTO A LA VENTA ACTUAL
     ============================================================ */

  // Esta función hace lo siguiente:
  // 1. Lee los valores del formulario
  // 2. Valida que estén completos y sean correctos
  // 3. Si todo está bien, crea el producto y lo agrega a la venta
  function agregarProductoDesdeFormulario() {
    const sku = inputSku.value.trim();
    const producto = inputProducto.value.trim();
    const cantidad = parseInt(inputCantidad.value);
    const precio = parseFloat(inputPrecio.value);

    if (!validarDatosProducto(sku, producto, cantidad, precio)) {
      return;
    }

    agregarProductoALaVenta(sku, producto, cantidad, precio);
    agregarProductoAlHistorial(sku, producto, precio);
    limpiarFormulario();
  }

  // Esta función revisa que los datos del producto sean válidos.
  // Devuelve true si está todo bien, false si falta algo.
  function validarDatosProducto(sku, producto, cantidad, precio) {
    if (!sku || !producto || isNaN(cantidad) || isNaN(precio) || cantidad <= 0 || precio < 0) {
      alert("Completa todos los campos correctamente.");
      return false;
    }
    return true;
  }

  // Esta función hace lo siguiente:
  // 1. Crea el objeto del producto
  // 2. Lo agrega a la lista de venta actual (en memoria)
  // 3. Vuelve a dibujar la tabla completa
  // 4. La venta actual queda en memoria hasta que se procese
  // 5. Recalcula el resumen (subtotal, itbis, total)
  function agregarProductoALaVenta(sku, producto, cantidad, precio) {
    const nuevoProductoVenta = {
      sku: sku,
      producto: producto,
      cantidad: cantidad,
      precio: precio
    };

    listaVentaActual.push(nuevoProductoVenta);

    dibujarTablaVentaCompleta();
   
    recalcularResumenVenta();
  }

  // Esta función limpia el formulario después de agregar un producto,
  // para que el usuario pueda escribir el siguiente sin borrar a mano.
  function limpiarFormulario() {
    inputSku.value = "";
    inputProducto.value = "";
    inputCantidad.value = 1;
    inputPrecio.value = "";
    inputSku.focus();
  }

  botonAgregarProducto.addEventListener("click", agregarProductoDesdeFormulario);


  /* ============================================================
     SECCION 4: DIBUJAR LA TABLA DE VENTA ACTUAL
     "Dibujar" significa borrar la tabla y volver a crearla desde
     cero usando la lista que tenemos en memoria (listaVentaActual).
     Hacerlo así (en vez de ir agregando filas sueltas) evita que
     la tabla y los datos guardados se desincronicen.
     ============================================================ */

  // Esta función hace lo siguiente:
  // 1. Borra todas las filas actuales de la tabla
  // 2. Si no hay productos, muestra un mensaje de "tabla vacía"
  // 3. Si hay productos, crea una fila por cada uno
  function dibujarTablaVentaCompleta() {
    cuerpoTablaVenta.innerHTML = "";

    if (listaVentaActual.length === 0) {
      const filaVacia = cuerpoTablaVenta.insertRow();
      const celdaVacia = filaVacia.insertCell();
      celdaVacia.colSpan = 6;
      celdaVacia.textContent = "Todavía no has agregado productos a esta venta.";
      celdaVacia.classList.add("ventas-tabla-vacia");
      return;
    }

    listaVentaActual.forEach((productoVenta, indiceProducto) => {
      crearFilaDeVenta(productoVenta, indiceProducto);
    });
  }

  // Esta función crea UNA fila de la tabla de venta, con sus
  // botones de Editar y Eliminar ya conectados a sus eventos.
  function crearFilaDeVenta(productoVenta, indiceProducto) {
    const totalProducto = productoVenta.cantidad * productoVenta.precio;
    const fila = cuerpoTablaVenta.insertRow();

    fila.insertCell().textContent = productoVenta.sku;
    fila.insertCell().textContent = productoVenta.producto;
    fila.insertCell().textContent = productoVenta.cantidad;
    fila.insertCell().textContent = formatearMoneda(productoVenta.precio);
    fila.insertCell().textContent = formatearMoneda(totalProducto);

    const celdaAcciones = fila.insertCell();
    celdaAcciones.appendChild(crearBotonEliminarVenta(indiceProducto));
    celdaAcciones.appendChild(crearBotonEditarVenta(indiceProducto));
  }

  // Esta función crea el botón rojo "X" que elimina un producto
  // de la venta actual usando su posición (índice) en la lista.
  function crearBotonEliminarVenta(indiceProducto) {
    const botonEliminar = document.createElement("button");
    botonEliminar.textContent = "X";
    botonEliminar.classList.add("ventas-btn-eliminar");

    botonEliminar.addEventListener("click", () => {
      eliminarProductoDeLaVenta(indiceProducto);
    });

    return botonEliminar;
  }

  // Esta función crea el botón verde "Editar" que convierte la
  // fila en modo edición.
 function crearBotonEditarVenta(indiceProducto) {
  const botonEditar = document.createElement("button");
  botonEditar.innerHTML = " Editar"; // ícono + texto
  botonEditar.classList.add("ventas-btn-reusar");

  botonEditar.addEventListener("click", (e) => {
    e.preventDefault(); // evita comportamientos raros
    if (typeof activarModoEdicion === "function") {
      activarModoEdicion(indiceProducto);
    } else {
      console.error("activarModoEdicion no está definida");
    }
  });

  return botonEditar;
}


  // Esta función hace lo siguiente:
  // 1. Quita el producto de la lista en memoria
  // 2. Vuelve a dibujar la tabla completa
  // 3. Recalcula el resumen
  function eliminarProductoDeLaVenta(indiceProducto) {
    listaVentaActual.splice(indiceProducto, 1);

    dibujarTablaVentaCompleta();
    recalcularResumenVenta();
  }


  /* ============================================================
     SECCION 5: EDITAR UN PRODUCTO DE LA VENTA ACTUAL
     ============================================================ */

  // Esta función hace lo siguiente:
  // 1. Busca la fila correspondiente al producto
  // 2. Convierte sus celdas en inputs editables
  // 3. Cambia los botones de acción por "Guardar" y "Cancelar"
  
  function activarModoEdicion(indiceProducto) {
    const productoVenta = listaVentaActual[indiceProducto];
    const fila = cuerpoTablaVenta.rows[indiceProducto];
    const celdas = fila.querySelectorAll("td");

    celdas[0].innerHTML = `<input type="text" class="ventas-input-editar-sku" value="${(productoVenta.sku)}">`;
    celdas[1].innerHTML = `<input type="text" class="ventas-input-editar-nombre" value="${(productoVenta.producto)}">`;
    celdas[2].innerHTML = `<input type="number" min="1" class="ventas-input-editar-cantidad" value="${productoVenta.cantidad}">`;
    celdas[3].innerHTML = `<input type="number" step="0.01" min="0" class="ventas-input-editar-precio" value="${productoVenta.precio}">`;
    celdas[4].textContent = "";

    const celdaAcciones = celdas[5];
    celdaAcciones.innerHTML = "";
    celdaAcciones.appendChild(crearBotonGuardarEdicion(indiceProducto, celdas));
    celdaAcciones.appendChild(crearBotonCancelarEdicion(indiceProducto));
  }

  // Esta función crea el botón "Guardar" que aparece durante la edición.
  function crearBotonGuardarEdicion(indiceProducto, celdas) {
    const botonGuardar = document.createElement("button");
    botonGuardar.textContent = "💾 Guardar";
    botonGuardar.classList.add("ventas-btn-reusar");

    botonGuardar.addEventListener("click", () => {
      guardarEdicionDeProducto(indiceProducto, celdas);
    });

    return botonGuardar;
  }

  // Esta función crea el botón "Cancelar" que aparece durante la edición.
  function crearBotonCancelarEdicion(indiceProducto) {
    const botonCancelar = document.createElement("button");
    botonCancelar.textContent = "✖ Cancelar";
    botonCancelar.classList.add("ventas-btn-eliminar");

    botonCancelar.addEventListener("click", () => {
      // Como no cambiamos la lista en memoria, con solo volver a
      // dibujar la tabla se restauran los valores originales.
      dibujarTablaVentaCompleta();
    });

    return botonCancelar;
  }

  // Esta función hace lo siguiente:
  // 1. Lee los nuevos valores de los inputs
  // 2. Los valida
  // 3. Actualiza el producto en la lista en memoria
  // 4. Vuelve a dibujar la tabla, guarda y recalcula
  function guardarEdicionDeProducto(indiceProducto, celdas) {
    const nuevoSku = celdas[0].querySelector("input").value.trim();
    const nuevoNombre = celdas[1].querySelector("input").value.trim();
    const nuevaCantidad = parseInt(celdas[2].querySelector("input").value);
    const nuevoPrecio = parseFloat(celdas[3].querySelector("input").value);

    if (!validarDatosProducto(nuevoSku, nuevoNombre, nuevaCantidad, nuevoPrecio)) {
      return;
    }

    listaVentaActual[indiceProducto] = {
      sku: nuevoSku,
      producto: nuevoNombre,
      cantidad: nuevaCantidad,
      precio: nuevoPrecio
    };

    dibujarTablaVentaCompleta();
    recalcularResumenVenta();
  }


  /* ============================================================
     SECCION 6: HISTORIAL DE PRODUCTOS
     El historial guarda productos que ya se han vendido antes,
     para poder reutilizarlos rápido sin escribir todo de nuevo.
     Se guarda en la base de datos (Django), no en localStorage.
     ============================================================ */

  // Esta función hace lo siguiente:
  // 1. Revisa si el SKU ya existe en el historial (en memoria)
  // 2. Si existe, solo actualiza el precio (evita duplicados)
  // 3. Si no existe, agrega el producto como nuevo
  // 4. Vuelve a dibujar la tabla y lo guarda en la base de datos
  function agregarProductoAlHistorial(sku, producto, precio) {
    const productoExistente = listaHistorial.find(item => item.sku === sku);

    if (productoExistente) {
      productoExistente.producto = producto;
      productoExistente.precio = precio;
    } else {
      listaHistorial.push({ sku, producto, precio });
    }

    dibujarTablaHistorialCompleta();
    guardarProductoEnHistorialBD(sku, producto, precio);
  }

  // Envia el producto a Django para que quede guardado en la base
  // de datos y no se pierda al recargar la pagina.
  function guardarProductoEnHistorialBD(sku, producto, precio) {
    fetch("/api/historial/guardar/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sku, producto, precio })
    })
      .then(res => res.json())
      .then(data => {
        if (data.error) {
          console.error("Error guardando historial:", data.error);
        }
      })
      .catch(error => console.error("Error guardando historial:", error));
  }

  // Elimina el producto del historial en la base de datos.
  function borrarProductoDeHistorialBD(sku) {
    fetch("/api/historial/borrar/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sku })
    }).catch(error => console.error("Error borrando del historial:", error));
  }

  // Esta función borra todas las filas del historial y las vuelve
  // a crear desde la lista que tenemos en memoria.
  function dibujarTablaHistorialCompleta() {
    cuerpoTablaHistorial.innerHTML = "";

    if (listaHistorial.length === 0) {
      const filaVacia = cuerpoTablaHistorial.insertRow();
      const celdaVacia = filaVacia.insertCell();
      celdaVacia.colSpan = 4;
      celdaVacia.textContent = "Aún no hay productos en el historial.";
      celdaVacia.classList.add("ventas-tabla-vacia");
      return;
    }

    listaHistorial.forEach(productoHistorial => {
      crearFilaDeHistorial(productoHistorial);
    });
  }

  // Esta función crea UNA fila del historial, con sus tres botones:
  // Reusar (llenar el formulario), Insertar (agregar directo a la
  // venta) y Borrar (quitarlo del historial).
  function crearFilaDeHistorial(productoHistorial) {
    const fila = cuerpoTablaHistorial.insertRow();

    fila.insertCell().textContent = productoHistorial.sku;
    fila.insertCell().textContent = productoHistorial.producto;
    fila.insertCell().textContent = formatearMoneda(productoHistorial.precio);

    const celdaAcciones = fila.insertCell();
    celdaAcciones.appendChild(crearBotonReusarHistorial(productoHistorial));
    celdaAcciones.appendChild(crearBotonInsertarHistorial(productoHistorial));
    celdaAcciones.appendChild(crearBotonBorrarHistorial(productoHistorial));
  }

  // Esta función crea el botón que copia los datos del producto
  // al formulario, para que el usuario pueda revisarlos antes de agregar.
  function crearBotonReusarHistorial(productoHistorial) {
    const botonReusar = document.createElement("button");
    botonReusar.classList.add("ventas-btn-reusar");

    botonReusar.addEventListener("click", () => {
      inputSku.value = productoHistorial.sku;
      inputProducto.value = productoHistorial.producto;
      inputPrecio.value = productoHistorial.precio;
      inputCantidad.value = 1;
      mostrarPestanaNuevaVenta();
      inputCantidad.focus();
    });

    return botonReusar;
  }

  // Esta función crea el botón que agrega el producto directo a la
  // venta actual, con cantidad 1, sin pasar por el formulario.
  function crearBotonInsertarHistorial(productoHistorial) {
    const botonInsertar = document.createElement("button");
    botonInsertar.textContent = " Insertar";
    botonInsertar.classList.add("ventas-btn-insertar");
   

    botonInsertar.addEventListener("click", () => {
      agregarProductoALaVenta(
        productoHistorial.sku,
        productoHistorial.producto,
        1,
        productoHistorial.precio
      );
      mostrarPestanaNuevaVenta();
    });

    return botonInsertar;
  }

  // Esta función crea el botón que borra un producto del historial
  // (esto NO afecta la venta actual, solo el historial).
  function crearBotonBorrarHistorial(productoHistorial) {
    const botonBorrar = document.createElement("button");
    botonBorrar.textContent = " Borrar";
    botonBorrar.classList.add("ventas-btn-eliminar");

    botonBorrar.addEventListener("click", () => {
      listaHistorial = listaHistorial.filter(item => item.sku !== productoHistorial.sku);
      dibujarTablaHistorialCompleta();
      borrarProductoDeHistorialBD(productoHistorial.sku);
    });

    return botonBorrar;
  }


  /* ============================================================
     SECCION 7: RESUMEN DE LA VENTA (Subtotal, ITBIS, Total)
     ============================================================ */

  // Esta función hace lo siguiente:
  // 1. Suma el total de todos los productos de la venta actual
  // 2. Calcula el ITBIS (18%)
  // 3. Calcula el total final
  // 4. Actualiza el texto en pantalla, ya formateado como dinero
  function recalcularResumenVenta() {
    const subtotalVenta = listaVentaActual.reduce((suma, productoVenta) => {
      return suma + (productoVenta.cantidad * productoVenta.precio);
    }, 0);

    const itbisVenta = subtotalVenta * 0.18;
    const totalVenta = subtotalVenta + itbisVenta;

    textoSubtotal.textContent = formatearMoneda(subtotalVenta);
    textoItbis.textContent = formatearMoneda(itbisVenta);
    textoTotal.textContent = formatearMoneda(totalVenta);
  }


  /* ============================================================
     SECCION 8: PROCESAR VENTA
     ============================================================ */

  // Esta función hace lo siguiente:
  // 1. Revisa que haya al menos un producto en la venta
  // 2. Pide confirmación al usuario
  // 3. Vacía la venta actual (la "cierra")
  // 4. Vuelve a dibujar todo y vacia la venta actual en memoria
function procesarVenta() {
  if (listaVentaActual.length === 0) {
    alert("Agrega al menos un producto antes de procesar la venta.");
    return;
  }

  const confirmoVenta = confirm("¿Confirmas que quieres procesar esta venta?");
  if (!confirmoVenta) return;

  const subtotal = listaVentaActual.reduce((suma, p) => suma + (p.cantidad * p.precio), 0);
  const itbis = subtotal * 0.18;
  const totalVenta = subtotal + itbis;

  fetch("/api/procesar_venta/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      productos: listaVentaActual,
      subtotal,
      itbis,
      total: totalVenta,
      fecha: new Date().toISOString().split("T")[0],    
      cliente: "Cliente Demo",                         
      medio_pago: "Efectivo",                           
      factura: "F001"                                   
    })
  })
  .then(res => res.json())
  .then(data => {
    alert(data.mensaje);
    listaVentaActual = [];
    dibujarTablaVentaCompleta();
    recalcularResumenVenta();
  });
}

botonProcesarVenta.addEventListener("click", procesarVenta);





  /* ============================================================
     SECCION 9: UTILIDADES GENERALES
     ============================================================ */

  // Convierte un número en texto de dinero dominicano, con
  // separador de miles. Ejemplo: 2400000000 -> "RD$ 2,400,000,000.00"
  function formatearMoneda(numero) {
    const numeroFormateado = numero.toLocaleString("es-DO", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });
    return "RD$ " + numeroFormateado;
  }

 

});