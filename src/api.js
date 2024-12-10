const API_URL = "http://127.0.0.1:5000"; // Cambia al dominio real cuando esté en producción

export async function getLockers() {
  const response = await fetch(`${API_URL}/lockers`);
  return await response.json();
}

export async function createLocker(data) {
  const response = await fetch(`${API_URL}/lockers`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return await response.json();
}
