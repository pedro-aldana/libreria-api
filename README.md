# 📖 Documentación de la API

La API está construida con **FastAPI** y sigue principios REST.  
Todas las respuestas son en formato **JSON**.

---

🔑 Autenticación

| Método   | Ruta             | Descripción                  | Parámetros                                                                   | Respuesta esperada                                                                                               |
| -------- | ---------------- | ---------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **POST** | `/auth/register` | Registrar un usuario nuevo   | JSON body: <br>`{ "username": string, "email": string, "password": string }` | `201 Created` con datos del usuario, ej: <br>`{ "id": 1, "username": "ejemplo", "email": "ejemplo@correo.com" }` |
| **POST** | `/auth/login`    | Login para obtener token JWT | JSON body: <br>`{ "username": string, "password": string }`                  | `200 OK` con token, ej: <br>`{ "access_token": "...", "token_type": "bearer" }`                                  |

---

📚 Usuarios

| Método     | Ruta               | Descripción                         | Roles / Permisos                 | Respuesta esperada                                              |
| ---------- | ------------------ | ----------------------------------- | -------------------------------- | --------------------------------------------------------------- |
| **GET**    | `/users/`          | Obtener lista de usuarios           | Solo administrador               | Lista de usuarios con campos básicos (id, username, email, rol) |
| **GET**    | `/users/{user_id}` | Obtener datos de usuario específico | Administrador o el mismo usuario | Datos detallados del usuario                                    |
| **DELETE** | `/users/{user_id}` | Eliminar usuario                    | Solo administrador               | `204 No Content` o mensaje de confirmación                      |

---

📚 Libros

| Método          | Ruta               | Descripción             | Roles / Permisos                                 | Request / Parámetros                                                                       | Respuesta esperada                                                                                                           |
| --------------- | ------------------ | ----------------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| **GET**         | `/books/`          | Listar todos los libros | Cualquiera autenticado                           | —                                                                                          | `200 OK`, arreglo de libros: <br> `{ "id": 1, "title": "...", "author": "...", "category": "...", "file_path": "...", ... }` |
| **GET**         | `/books/{book_id}` | Ver un libro específico | Cualquiera autenticado                           | —                                                                                          | `200 OK`, objeto libro completo                                                                                              |
| **POST**        | `/books/`          | Crear/unsubir un libro  | Usuario con permiso especial (e.g. admin/editor) | JSON + archivo PDF (multi-parte) <br> Campos como `title`, `author`, `category_id`, `file` | `201 Created`, objeto libro creado                                                                                           |
| **PUT / PATCH** | `/books/{book_id}` | Editar libro existente  | Permiso especial                                 | JSON con campos a modificar                                                                | `200 OK`, objeto actualizado                                                                                                 |
| **DELETE**      | `/books/{book_id}` | Eliminar libro          | Permiso especial                                 | —                                                                                          | `204 No Content` o confirmación                                                                                              |


---

📂 Categorías

| Método          | Ruta                        | Descripción           | Roles / Permisos                     | Request / Parámetros       | Respuesta esperada              |
| --------------- | --------------------------- | --------------------- | ------------------------------------ | -------------------------- | ------------------------------- |
| **GET**         | `/categories/`              | Listar categorías     | Cualquiera autenticado               | —                          | `200 OK`, lista de categorías   |
| **POST**        | `/categories/`              | Crear nueva categoría | Admin o usuario con permiso especial | JSON: `{ "name": string }` | `201 Created`, categoría creada |
| **PUT / PATCH** | `/categories/{category_id}` | Actualizar categoría  | Permiso especial                     | `{ "name": string }`       | `200 OK`, categoría modificada  |
| **DELETE**      | `/categories/{category_id}` | Eliminar categoría    | Permiso especial                     | —                          | `204 No Content`                |


---

⚙ Gestión de Roles / Permisos

| Método   | Ruta            | Descripción              | Roles / Permisos | Parámetros                                                     | Respuesta esperada                      |
| -------- | --------------- | ------------------------ | ---------------- | -------------------------------------------------------------- | --------------------------------------- |
| **GET**  | `/roles/`       | Listar roles disponibles | Admin            | —                                                              | `200 OK`, lista de roles y sus permisos |
| **POST** | `/roles/`       | Crear nuevo rol          | Admin            | JSON: `{ "name": string, "permissions": [perm1, perm2, ...] }` | `201 Created`, rol creado               |
| **POST** | `/roles/assign` | Asignar rol a usuario    | Admin            | JSON: `{ "user_id": int, "role_id": int }`                     | `200 OK`, confirmación                  |


---

⚠ Errores comunes

401 Unauthorized → Token inválido o no enviado

403 Forbidden → Permisos insuficientes

404 Not Found → Recurso no existe

422 Unprocessable Entity → Validación fallida





