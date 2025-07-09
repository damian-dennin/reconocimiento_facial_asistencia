import cv2,face_recognition as fr,os,numpy as np,datetime

#creamos la base de datos
ruta="Empleados"
lista_imagenes=[]
nombres_empleados=[]
lista_empleados=os.listdir(ruta)

for nombre in lista_empleados:
    imagen_actual=cv2.imread(ruta+"/"+nombre)
    lista_imagenes.append(imagen_actual)
    nombres_empleados.append(os.path.splitext(nombre)[0])

#funcion para codificar imagenes
def codificar(imagenes):

    #crear lista nueva
    imagenes_codificadas=[]

    #imagenes a rgb
    for imagen in imagenes:
        imagen=cv2.cvtColor(imagen,cv2.COLOR_BGR2RGB)

        #codificamos
        codificacion=fr.face_encodings(imagen)[0]
        imagenes_codificadas.append(codificacion)

    #devolver lista codificadas
    return imagenes_codificadas

#registrar ingreso de empleado
def registrar_ingreso(persona):
    f=open("registro.csv","r+")
    datos=f.readlines()
    nombres_registro=[]

    for linea in datos:
        ingreso=linea.split(",")
        nombres_registro.append(ingreso[0])

    if persona not in nombres_registro:
        ahora=datetime.datetime.now()
        string_ahora=ahora.strftime("%H:%M:%S")
        f.write(f"{persona},{string_ahora}\n")



lista_empleados_codificadas=codificar(lista_imagenes)

#tomar imagen de camara
captura=cv2.VideoCapture(0,cv2.CAP_DSHOW)

#leer imagen de la camara
exito,imagen=captura.read()

if not exito:
    print("No se tomo la captura")
else:

    #rgb
    imagen_rgb=cv2.cvtColor(imagen,cv2.COLOR_BGR2RGB)

    #reconocer cara
    cara_captura=fr.face_locations(imagen_rgb)

    #codificar captura
    captura_codificada=fr.face_encodings(imagen_rgb,cara_captura)

    #buscamos coincidencia
    for cara_codificada, cara_ubicacion in zip(captura_codificada,cara_captura):
        coincidencias=fr.compare_faces(lista_empleados_codificadas,cara_codificada)
        distancias=fr.face_distance(lista_empleados_codificadas,cara_codificada)

        #distancias nos devuelve una lista con todas las distancias entre la foto tomada y cada una de las fotos de los empleados, con numpy entonces buscamos el indice dentro de esa lista que sea menor o igual a 0.6
        indice_coincidencia=np.argmin(distancias)


        #mostrar coincidencias
        if distancias[indice_coincidencia]>0.6:
            cv2.putText(imagen, "No coincide con ningun empleado", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.imshow("Reconocimiento facial",imagen)

        else:
            #buscamos el nombre del empleado con el indice que obtuvimos anteriormente
            nombre=nombres_empleados[indice_coincidencia]
            #armamos rectangulo con las ubicaciones de cara_ubicacion, que seria de la persona que detecto que efectivamente es empleado.
            y1,x2,y2,x1=cara_ubicacion
            cv2.rectangle(imagen,(x1,y1),(x2,y2),(0,255,0),2)

            #mostramos la imagen tomada junto con el nombre del empleado
            cv2.putText(imagen,f"Empleado: {nombre}",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
            registrar_ingreso(nombre)

            #mostrar la imagen obtenida
            cv2.imshow("Reconocimiento facial",imagen)
            cv2.waitKey(0)

