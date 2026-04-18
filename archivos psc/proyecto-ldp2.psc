Algoritmo SistemaControlPaqueteria
    
    Definir MAX_PAQUETES Como Entero
    MAX_PAQUETES <- 100 
    
    Dimension idPaquete[MAX_PAQUETES]
    Dimension pesoPaquete[MAX_PAQUETES]
    Dimension estadoPaquete[MAX_PAQUETES] 
    
    Definir totalRegistros, opcionMenu, i, idBusqueda Como Entero
    Definir pesoInput Como Real
    Definir paqueteEncontrado Como Logico
    
    totalRegistros <- 0
    opcionMenu <- 0
    
    Mientras opcionMenu <> 5 Hacer
        
        Escribir "==================================="
        Escribir "   SISTEMA CORE DE PAQUETERIA"
        Escribir "==================================="
        Escribir "1. Registrar Nuevo Paquete"
        Escribir "2. Actualizar Estado de Paquete"
        Escribir "3. Consultar Tracking"
        Escribir "4. Listar Paquetes"
        Escribir "5. Salir"
        Escribir "==================================="
        
        Repetir
            Escribir "Ingrese una opcion (1-5):"
            Leer opcionMenu
            Si opcionMenu < 1 O opcionMenu > 5 Entonces
                Escribir "Error: Opcion no valida."
            FinSi
        Hasta Que opcionMenu >= 1 Y opcionMenu <= 5
        
        
        Si opcionMenu = 1 Entonces
            Si totalRegistros < MAX_PAQUETES Entonces
                totalRegistros <- totalRegistros + 1
                
                idPaquete[totalRegistros] <- 1000 + totalRegistros
                estadoPaquete[totalRegistros] <- 1 
                
                Repetir
                    Escribir "Ingrese el peso del paquete (> 0):"
                    Leer pesoInput
                    Si pesoInput <= 0 Entonces
                        Escribir "Error: peso invalido."
                    FinSi
                Hasta Que pesoInput > 0
                
                pesoPaquete[totalRegistros] <- pesoInput
                
                Escribir "Exito! Paquete registrado con ID: ", idPaquete[totalRegistros]
            SiNo
                Escribir "Error: base de datos llena."
            FinSi
        FinSi

        Si opcionMenu = 2 Entonces
            Escribir "Ingrese ID del paquete:"
            Leer idBusqueda
            
            paqueteEncontrado <- Falso
            
            Para i <- 1 Hasta totalRegistros Hacer
                Si idPaquete[i] = idBusqueda Entonces
                    paqueteEncontrado <- Verdadero
                    
                    Escribir "Estado actual: ", TraducirEstado(estadoPaquete[i])
                    
                    Escribir "Nuevo estado:"
                    Escribir "1: Bodega"
                    Escribir "2: En Ruta"
                    Escribir "3: Entregado"
                    Leer estadoPaquete[i]
                    
                    Escribir "Estado actualizado: ", TraducirEstado(estadoPaquete[i])
                FinSi
            FinPara
            
            Si No paqueteEncontrado Entonces
                Escribir "Error 404: Paquete no encontrado."
            FinSi
        FinSi
        

        Si opcionMenu = 3 Entonces
            Escribir "Ingrese ID del paquete:"
            Leer idBusqueda
            
            paqueteEncontrado <- Falso
            
            Para i <- 1 Hasta totalRegistros Hacer
                Si idPaquete[i] = idBusqueda Entonces
                    paqueteEncontrado <- Verdadero
                    
                    Escribir "===== PAQUETE ====="
                    Escribir "ID     : ", idPaquete[i]
                    Escribir "Peso   : ", pesoPaquete[i], " lbs"
                    Escribir "Estado : ", TraducirEstado(estadoPaquete[i])
                FinSi
            FinPara
            
            Si No paqueteEncontrado Entonces
                Escribir "Error 404: Paquete no existe."
            FinSi
        FinSi
        
    
        Si opcionMenu = 4 Entonces
            Si totalRegistros = 0 Entonces
                Escribir "No hay paquetes registrados."
            SiNo
                Escribir "===== LISTA DE PAQUETES ====="
                
                Para i <- 1 Hasta totalRegistros Hacer
					Escribir "ID: ", idPaquete[i]
					Escribir "Peso: ", pesoPaquete[i], " lbs"
					Escribir "Estado: ", TraducirEstado(estadoPaquete[i])
					Escribir "-----------------------------"
                FinPara
                
                Escribir "============================="
            FinSi
        FinSi
		
		Si opcionMenu = 5 Entonces
			Escribir "Cerrando sistema... Deploy exitoso!"
		FinSi
        
    FinMientras
    
    Escribir "Cerrando sistema... Deploy exitoso!"
    
FinAlgoritmo


Funcion estadoTexto <- TraducirEstado(estado)
    Segun estado Hacer
        1:
            estadoTexto <- "Bodega"
        2:
            estadoTexto <- "En Ruta"
        3:
            estadoTexto <- "Entregado"
        De Otro Modo:
            estadoTexto <- "Desconocido"
    FinSegun
FinFuncion