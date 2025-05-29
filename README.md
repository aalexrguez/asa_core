# ASA_CORE - Sistema de Gestión para Gimnasio

**Proyecto Final - Programación Backend**  
**Equipo: ASA**

## Integrantes del equipo

- **Alejandro Rodríguez Rodríguez**
- **Andrés Isaac Espinoza Contreras**
- **Saúl Ernesto Martínez Campos**

---

## Descripción del proyecto

**ASA_CORE** es una aplicación web desarrollada como proyecto final de la materia de **Programación Backend**, 
cuyo objetivo es facilitar la gestión integral de un gimnasio. Esta aplicación está diseñada para que los 
administradores del gimnasio puedan manejar de forma eficiente a los clientes, entrenadores, membresías y asesorías.

---

## Tecnologías utilizadas

- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Base de datos**: MYSQL 
- **API**: Django REST Framework
- **Gráficas y Reportes**: Charts.js 
- **Gestión de usuarios**: Sistema de roles (administrador, cliente, entrenador)

---

## Funcionalidades principales

### Gestión de usuarios
- Registro, edición y eliminación de usuarios.
- Carga y visualización de imagen de perfil.

### Gestión de clientes
- Alta, baja y modificación de clientes.
- Asignación de membresías y entrenadores.

### Gestión de entrenadores
- Registro y edición de entrenadores.
- Consulta de clientes asignados.

### Gestión de membresías
- Creación y asignación de tipos de membresías.
- Seguimiento de membresías activas e historial.

### Reportes y estadísticas (API)
- **/reportes/membresias/activas/**: Total y distribución por tipo.
- **/reportes/membresias/por-tipo/**: Número de usuarios por tipo de membresía.
- **/reportes/entrenadores-top/**: Entrenadores con más clientes asignados.
- **/reportes/estadisticas-generales/**: Contadores generales del sistema.

### Otras funcionalidades
- Interfaz responsiva y amigable.
- Validación de formularios.
- Sistema modular para facilitar mantenibilidad y escalabilidad.

---

