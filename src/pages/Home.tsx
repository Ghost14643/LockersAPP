import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom'; // Para navegación entre rutas
import axios from 'axios';

const Home: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const [lockersData, setLockersData] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);
  const history = useHistory();

  // Verificar si el usuario está logueado
  useEffect(() => {
    const checkLoginStatus = async () => {
      try {
        const response = await axios.get('/api/check-login');
        if (response.data.loggedIn) {
          setIsLoggedIn(true);
        } else {
          setIsLoggedIn(false);
        }
      } catch (err) {
        setError('Error al verificar el estado de la sesión');
      }
    };

    checkLoginStatus();
  }, []);

  // Obtener los lockers desde el backend
  useEffect(() => {
    if (isLoggedIn) {
      axios
        .get('/api/lockers')
        .then((response) => {
          setLockersData(response.data);
        })
        .catch((error) => {
          setError('Error al cargar los lockers');
        });
    }
  }, [isLoggedIn]);

  // Navegar a la página de login si no está logueado
  if (!isLoggedIn) {
    history.push('/login');
  }

  return (
    <div>
      <h1>Bienvenido al sistema de lockers</h1>
      {error && <div className="error-message">{error}</div>}

      {isLoggedIn ? (
        <div>
          <h2>Listado de lockers</h2>
          <table>
            <thead>
              <tr>
                <th>ID Locker</th>
                <th>Número de Locker</th>
                <th>Piso</th>
                <th>Edificio</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              {lockersData.length === 0 ? (
                <tr>
                  <td colSpan={5}>No hay lockers disponibles</td>
                </tr>
              ) : (
                lockersData.map((locker) => (
                  <tr key={locker.idLocker}>
                    <td>{locker.idLocker}</td>
                    <td>{locker.numeroLocker}</td>
                    <td>{locker.pisoCol}</td>
                    <td>{locker.letraEdificio}</td>
                    <td>{locker.estado}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="loading">Cargando datos...</div>
      )}
    </div>
  );
};

export default Home;
