# 📖 Documentación de la API

La API está construida con **FastAPI** y sigue principios REST.  
Todas las respuestas son en formato **JSON**.


| Método   | Ruta             | Descripción                  | Parámetros                                                                   | Respuesta esperada                                                                                               |
| -------- | ---------------- | ---------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **POST** | `/auth/register` | Registrar un usuario nuevo   | JSON body: <br>`{ "username": string, "email": string, "password": string }` | `201 Created` con datos del usuario, ej: <br>`{ "id": 1, "username": "ejemplo", "email": "ejemplo@correo.com" }` |
| **POST** | `/auth/login`    | Login para obtener token JWT | JSON body: <br>`{ "username": string, "password": string }`                  | `200 OK` con token, ej: <br>`{ "access_token": "...", "token_type": "bearer" }`                                  |
