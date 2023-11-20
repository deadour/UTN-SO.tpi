
## Simulador de Asignación de Memoria y Planificación de procesos
### TPI Sistemas Operativos - Grupo "Oppenheimer"
![Portada](https://raw.githubusercontent.com/deadour/SO-TPI/master/screenshots/portada.PNG)




Trabajo Práctico Integrador de la materia de Sistemas Operativos, del tercer nivel de la carrera Ingeniería en Sistemas de Información. El objetivo principal es la implementación de un simulador que destaque los aspectos de la Planificación a Corto Plazo y la gestión de la memoria con particiones fijas en un entorno de un solo procesador. El simulador aborda el ciclo de vida completo de un proceso, desde su ingreso al sistema hasta su finalización.

En cuanto a los requisitos, se espera que el simulador ofrezca la posibilidad de cargar hasta 10 procesos, con asignación de memoria basada en particiones fijas. Estas particiones incluyen asignaciones específicas para el Sistema Operativo (100K), trabajos más grandes (250K), trabajos medianos (120K) y trabajos pequeños (60K). La multiprogramación se mantiene en un grado de 5.

La política de asignación de memoria adoptada es Best-Fit, donde cada proceso requiere la entrada del Id de proceso, tamaño, tiempo de arribo y tiempo de irrupción. La planificación de CPU se rige por el algoritmo Round-Robin con un quantum de 2.

La salida del simulador incluye información relevante como el estado actual del procesador, la tabla de particiones de memoria (con detalles como Id de partición, dirección de comienzo, tamaño, Id de proceso asignado y fragmentación interna), el estado de la cola de procesos listos y, al finalizar la simulación, se presenta un informe estadístico que incluye tiempos de retorno y espera para cada proceso, junto con los respectivos tiempos promedios.

### Autores

- Aguirre, Julián;
- Ramírez. Eduardo;
- Sanchez,  Gisela;
- Saucedo, Gonzalo;
- Verón, Valeria.


- Fecha: noviembre de 2023

## Consigna
Implementar un simulador de asignación de memoria y planificación de procesos según los siguientes
requerimientos.
El simulador deberá brindarla posibilidad de cargar procesos por parte del usuario. Para facilitar la implementación
se permitirán como máximo 10 procesos y la asignación de memoria se realizará con particiones fijas. El esquema
de particiones será el siguiente:
- 100K destinados al Sistema Operativo
- 250K para trabajos los más grandes.
- 120K para trabajos medianos
- 60K para trabajos pequeños.
El programa debe permitir ingreso de nuevos procesos cuando sea posible (manteniendo en grado de
multiprogramación en 5) La política de asignación de memoria será Best-Fit, por cada proceso se debe ingresar o
leer desde un archivo el Id de proceso, tamaño del proceso, tiempo de arribo y tiempo de irrupción. La
planificación de CPU será dirigida por un algoritmo Round-Robin con q=2.
El simulador deberá presentar como salida la siguiente información:
- El estado del procesador (proceso que se encuentra corriendo en ese instante)
- La tabla de particiones de memoria, la cual deberá contener (Id de partición, dirección de comienzo de partición, tamaño de la partición, id de proceso asignado a la partición, fragmentación interna)
- El estado de la cola de procesos listos.
- Al finalizar la simulación se deberá presentar un informe estadístico con, tiempo de retorno y espera para cada proceso y los respectivos tiempos promedios.
### Consideraciones:
- Las presentaciones de salida deberán realizarse cada vez que llega un nuevo proceso, se termina un procesoen ejecución.
- No se permiten corridas ininterrumpidas de simulador, desde que se inicia la simulación hasta que termina el último proceso

## Diagrama de Flujo

Modelamos el siguiente diagrama de flujo para nuestro programa:

![Diagrama de Flujo TPI](https://raw.githubusercontent.com/deadour/SO-TPI/master/docs/DiagFlujo.png)

## Ejecución

Para ejecutar el simulador, se debe acceder a través de un archivo ejecutable, que se encuentra en la carpeta /ejecutable, cuyo nombre es "SimuladorOppenheimer.exe"

![Ejecutable](https://raw.githubusercontent.com/deadour/SO-TPI/master/screenshots/0.PNG)


- **💻[Ejecutable](https://github.com/deadour/SO-TPI/tree/main/ejecutable)**


El mismo posee una interfaz que permite cargar un archivo .json o .csv con procesos.

![Interfaz](https://raw.githubusercontent.com/deadour/SO-TPI/master/screenshots/1.PNG)

Una vez seleccionado el archivo, se muestran los datos cargados:

![Tabla](https://raw.githubusercontent.com/deadour/SO-TPI/master/screenshots/2.PNG)


A medida que van transcurriendo los instantes en memoria, se van mostrando los cambios de estado en los procesos:

![Tabla](https://raw.githubusercontent.com/deadour/SO-TPI/master/screenshots/3.PNG)

![Tabla](https://raw.githubusercontent.com/deadour/SO-TPI/master/screenshots/4.PNG)

Al finalizar todos los procesos, se muestra un informe estadístico.

![Tabla](https://raw.githubusercontent.com/deadour/SO-TPI/master/screenshots/5.PNG)

## Conclusión
En conclusión, la realización de este Trabajo Práctico Integrador ha sido fundamental para consolidar los conocimientos teóricos adquiridos en la materia y aplicarlos de manera práctica en el desarrollo de un simulador. A través de este proyecto, se abordaron aspectos cruciales de la planificación a corto plazo y la gestión de memoria con particiones fijas en un entorno de un solo procesador.

El diseño integral del simulador permitió no solo comprender los conceptos teóricos asociados, sino también llevarlos a la práctica mediante la implementación de algoritmos como Best-Fit para la asignación de memoria y Round-Robin para la planificación de CPU. La capacidad de cargar procesos, mantener un grado de multiprogramación específico y proporcionar información detallada sobre el estado del procesador, la memoria y la cola de procesos, contribuyó significativamente a la comprensión del ciclo de vida completo de un proceso en un sistema operativo.

Además, la presentación de un informe estadístico al finalizar la simulación permitió evaluar el rendimiento del sistema, analizando tiempos de retorno y espera para cada proceso, así como los respectivos tiempos promedios. Este enfoque no solo reforzó los conocimientos sobre la teoría de sistemas operativos, sino que también proporcionó una experiencia valiosa en la implementación práctica de estos conceptos.

## Enlaces


- **🔗[Documentación](https://github.com/deadour/SO-TPI/blob/main/docs/TPISO-Oppenheimer.pdf)**
