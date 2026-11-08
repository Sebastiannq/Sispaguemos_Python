// src/services/usuarioService.js

const API_URL = 'http://127.0.0.1:8000/api/usuarios';

/**
 * Iniciar sesión de usuario
 */
export async function loginUsuario(credentials) {
    try {
        const response = await fetch(`${API_URL}/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(credentials),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Credenciales inválidas. Verifica tu correo y contraseña.');
        }

        return data;
    } catch (error) {
        throw new Error(error.message || 'Error de conexión con el servidor.');
    }
}

/**
 * Registrar un nuevo usuario (Soporta campos de texto y foto de perfil)
 */
export async function registrarUsuario(userData) {
    try {
        const formData = new FormData();
        
        formData.append('primerNom', userData.primerNom);
        if (userData.segundNom) {
            formData.append('segundNom', userData.segundNom);
        }
        formData.append('primerApelli', userData.primerApelli);
        if (userData.segundApelli) {
            formData.append('segundApelli', userData.segundApelli);
        }
        formData.append('correo', userData.correo);
        formData.append('contrasena', userData.contrasena);
        formData.append('estado', userData.estado || 'Activo');

        if (userData.imagenPerfil instanceof File) {
            formData.append('imagen_perfil', userData.imagenPerfil);
        }

        const response = await fetch(`${API_URL}/registrar/`, {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'No se pudo crear la cuenta.');
        }

        return data;
    } catch (error) {
        throw new Error(error.message || 'Error de conexión con el servidor.');
    }
}

/**
 * Alias para registrarUsuario (usado por vistas de administración como crearUsuario)
 */
export const crearUsuario = registrarUsuario;

/**
 * Obtener lista de usuarios
 */
export async function obtenerUsuarios() {
    try {
        const response = await fetch(`${API_URL}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Error al obtener la lista de usuarios.');
        }

        return data;
    } catch (error) {
        throw new Error(error.message || 'Error de conexión con el servidor.');
    }
}

/**
 * Actualizar datos de un usuario existente
 */
export async function actualizarUsuario(id, userData) {
    try {
        const response = await fetch(`${API_URL}/${id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Error al actualizar el usuario.');
        }

        return data;
    } catch (error) {
        throw new Error(error.message || 'Error de conexión con el servidor.');
    }
}

/**
 * Eliminar o desactivar un usuario
 */
export async function eliminarUsuario(id) {
    try {
        const response = await fetch(`${API_URL}/${id}/`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            const data = await response.json().catch(() => ({}));
            throw new Error(data.error || 'Error al eliminar el usuario.');
        }

        return true;
    } catch (error) {
        throw new Error(error.message || 'Error de conexión con el servidor.');
    }
}