import React, { useState } from "react";
import {
  IonPage,
  IonContent,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonButtons,
  IonButton,
  IonModal,
  IonLabel,
  IonInput,
  IonItem,
  IonFooter,
  IonTabBar,
  IonTabButton,
  IonIcon,
  IonAlert,
  IonImg,
} from "@ionic/react";
import { personCircle, qrCode, bookmark } from "ionicons/icons";

const LandingPage: React.FC = () => {
  const [isOpen, setIsOpen] = useState(true);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showAlert, setShowAlert] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleLogin = (event: React.FormEvent) => {
    event.preventDefault();
    if (username && password) {
      setIsOpen(false);
      setErrorMessage("");
    } else {
      setErrorMessage("Por favor, completa ambos campos.");
    }
  };

  return (
    <IonPage>
      {/* Header */}
      <IonHeader>
        <IonToolbar className="bg-blue-600">
          <IonTitle className="text-white text-xl font-bold">LockersDuoc</IonTitle>
        </IonToolbar>
      </IonHeader>

      {/* Contenido */}
      <IonContent className="bg-gray-100">
        <div className="flex flex-col items-center justify-center min-h-screen">
          <IonImg src="/LockersDuoc.png" alt="Logo" className="w-24 mb-6" />
          <form
            onSubmit={handleLogin}
            className="bg-white p-6 rounded-lg shadow-md w-full max-w-md space-y-4"
          >
            <IonItem lines="none" className="flex flex-col space-y-2">
              <IonLabel className="text-gray-600">Usuario</IonLabel>
              <IonInput
                value={username}
                onIonChange={(e) => setUsername(e.detail.value!)}
                placeholder="Ingresa tu usuario"
                required
                className="border rounded-md p-2 focus:ring-2 focus:ring-blue-500"
              />
            </IonItem>

            <IonItem lines="none" className="flex flex-col space-y-2">
              <IonLabel className="text-gray-600">Contraseña</IonLabel>
              <IonInput
                type="password"
                value={password}
                onIonChange={(e) => setPassword(e.detail.value!)}
                placeholder="Ingresa tu contraseña"
                required
                className="border rounded-md p-2 focus:ring-2 focus:ring-blue-500"
              />
            </IonItem>

            {errorMessage && (
              <p className="text-red-600 text-sm">{errorMessage}</p>
            )}

            <IonButton
              type="submit"
              expand="block"
              className="bg-blue-600 text-white font-bold py-2 rounded-lg hover:bg-blue-700"
            >
              Iniciar Sesión
            </IonButton>
          </form>
        </div>
      </IonContent>

      {/* Modal */}
      <IonModal isOpen={isOpen}>
        <IonHeader>
          <IonToolbar>
            <IonTitle className="text-xl font-bold">¡Bienvenido!</IonTitle>
            <IonButtons slot="end">
              <IonButton onClick={() => setIsOpen(false)}>Cerrar</IonButton>
            </IonButtons>
          </IonToolbar>
        </IonHeader>
        <IonContent className="ion-padding">
          <div className="text-center">
            <h1 className="text-2xl font-bold mb-4">¡Bienvenido a LockersDuoc!</h1>
            <p className="text-gray-600 mb-6">
              Reserva un locker fácilmente y mantén tus pertenencias seguras.
            </p>
            <IonButton
              expand="block"
              onClick={() => setIsOpen(false)}
              className="bg-green-600 text-white font-bold py-2 rounded-lg hover:bg-green-700"
            >
              Continuar al Login
            </IonButton>
          </div>
        </IonContent>
      </IonModal>

      {/* Footer */}
      <IonFooter>
        <IonToolbar>
          <IonTabBar slot="bottom" className="bg-white border-t">
            <IonTabButton tab="profile" className="text-gray-600 hover:text-gray-800">
              <IonIcon icon={personCircle} />
              <IonLabel>Perfil</IonLabel>
            </IonTabButton>
            <IonTabButton tab="qr" className="text-gray-600 hover:text-gray-800">
              <IonIcon icon={qrCode} />
              <IonLabel>QR</IonLabel>
            </IonTabButton>
            <IonTabButton tab="reserve" className="text-gray-600 hover:text-gray-800">
              <IonIcon icon={bookmark} />
              <IonLabel>Reservas</IonLabel>
            </IonTabButton>
          </IonTabBar>
        </IonToolbar>
      </IonFooter>

      {/* Alerta */}
      <IonAlert
        isOpen={showAlert}
        onDidDismiss={() => setShowAlert(false)}
        header={"Inicia sesión"}
        message={"Por favor, inicia sesión para usar esta función."}
        buttons={["OK"]}
      />
    </IonPage>
  );
};

export default LandingPage;
