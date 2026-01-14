from gui.app import run_app
from data.collector import collect_data
from model.train import train_model
from realtime.inference import realtime_test


def menu():
    print("\n=== Lenguaje de Señas - LSTM ===")
    print("1️⃣ Recolectar datos")
    print("2️⃣ Entrenar modelo")
    print("3️⃣ Testeo en tiempo real")
    print("4️⃣ Abrir interfaz gráfica")
    print("0️⃣ Salir")


if __name__ == "__main__":
    while True:
        menu()
        option = input("Selecciona una opción: ")

        if option == "1":
            collect_data()
        elif option == "2":
            train_model()
        elif option == "3":
            realtime_test()
        elif option == "4":
            run_app()
        elif option == "0":
            break
        else:
            print("❌ Opción inválida")
