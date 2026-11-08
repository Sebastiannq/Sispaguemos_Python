import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/prendas';

// ==========================================
// 1. CONSULTAR (Read) - Listar todas las prendas
// ==========================================
export const obtenerPrendas = async () => {
    try {
        const res = await axios.get(API_URL);
        return res.data;
    } catch (error) {
        console.error("Error al obtener las prendas:", error);
        throw error;
    }
};

// Consultar tallas específicas por prenda y género (Hombre, Mujer, Infantil)
export const obtenerTallasPorPrenda = async (idPrenda, genero) => {
    try {
        const generoNormalizado = String(genero || '').trim().toLowerCase();
        const rutas = generoNormalizado === 'niño' || generoNormalizado === 'niña'
            ? ['infantil']
            : generoNormalizado === 'unisex'
                ? ['hombre', 'mujer']
                : [generoNormalizado];

        const respuestas = await Promise.all(
            rutas.map(async (ruta) => ({
                tipoTalla: ruta,
                data: (await axios.get(`${API_URL}/${ruta}/prenda/${idPrenda}`)).data,
            }))
        );

        return respuestas
            .flatMap((respuesta) => (Array.isArray(respuesta.data) ? respuesta.data : []).map((talla) => ({ ...talla, tipoTalla: respuesta.tipoTalla })))
            .map((talla) => ({
                talla: talla.talla,
                cantidadTalla: Number(talla.cantidadTalla ?? talla.cantidad_talla ?? 0),
                tipoTalla: talla.tipoTalla,
                idTalla: talla.idHombre || talla.idMujer || talla.idInfantil || talla.id_hombre || talla.id_mujer || talla.id_infantil,
            }))
            .filter((talla) => talla.talla && talla.cantidadTalla > 0);
    } catch (error) {
        console.error("Error al obtener las tallas de la prenda:", error);
        return [];
    }
};

// ==========================================
// 2. CREAR (Create) - Registrar nueva prenda
// ==========================================
export const crearPrenda = async (prendaData) => {
    try {
        const res = await axios.post(API_URL, prendaData);
        return res.data;
    } catch (error) {
        console.error("Error al crear la prenda:", error);
        throw error;
    }
};

// ==========================================
// 3. ACTUALIZAR (Update) - Modificar prenda y stock/tallas
// ==========================================
export const actualizarPrenda = async (id, prendaData) => {
    try {
        const res = await axios.put(`${API_URL}/${id}`, prendaData);
        return res.data;
    } catch (error) {
        console.error(`Error al actualizar la prenda con ID ${id}:`, error);
        throw error;
    }
};

// ==========================================
// 4. ELIMINAR (Delete) - Borrar prenda del sistema
// ==========================================
export const eliminarPrenda = async (id) => {
    try {
        const res = await axios.delete(`${API_URL}/${id}`);
        return res.data;
    } catch (error) {
        console.error(`Error al eliminar la prenda con ID ${id}:`, error);
        throw error;
    }
};