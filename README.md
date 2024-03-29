# WhatsApp proyecto realizado para Microtec
Proyecto realizado que busca implementar el api de OpenAI, especificamente la herramienta de inteligencia artificial llamada Chat-GPT con el modelo Text DaVinci 03, en auto respuestas para WhatsApp Bussiness, apoyandose de las librerias "Flask" y "Request" del lenguaje de programación Python.

## Avances iniciales del proyecto
Implementación de registro de mensajes y contestación automatica tras recibir un mensaje. Los mensajes son, por ahora, guardados en un archivo de texto que pueden ser revisados a traves de la siguiente liga http://lilithliliana.alwaysdata.net/ , por otro lado para responder los mensajes, dado a las limitaciones del status de prueba de la API con la que se estan realizando las pruebas, solo es posible devolver el mensaje de numero agregados en la pagina de Meta.

Aqui un ejemplo de las contestaciones automaticas, estas unicamente hacen eco del mensaje del remitente para probar las respuestas que ofrece la API, cabe aclarar que para facilitar el procesamiento de las respuestas se hace uso de la libreria Heyoo.

<p align="center">
<img width="400" src="https://github.com/T-UwU/WA-Integration_Microtec/assets/72111629/1b66205f-7692-4f43-92b0-f480e4855af9">
</p>

## Actualización de avances
Se ha añadido la API de OpenAI, haciendo uso del modelo DaVinci 03 con el fin de actuar como un elemento de atención al cliente, buscando automatizar este proceso. Hace uso de información alimentada via el "prompt" para responder con información existente. Existen limitaciones presentes a causa de esta forma de implementación, esto se debe a que el sistema de "tokens" para interpretar y procesar la información que usa el modelo presenta un limite a las versiones de prueba, haciendo complicado el añadir mas información que el modelo tome en consideración.

<p align="center">
<img width="400" src="https://github.com/T-UwU/WA-Integration_Microtec/assets/72111629/ebb59e20-d91d-4fac-9e20-99a28dc4652e">
</p>

## Segunda actualización de avances
Se modifico la forma en la que funciona el bot, utilizando Llama Index para manejar grandes cantidades de información de manera eficiente y permitiendo que el bot tenga acceso a esta sin necesidad de saturar el prompt cada vez que se hace una llamada. De igual forma se implementaron metodos de API con el fin de poder realizar consultas en la API de Credicel y poder informar al usuario de los valores que retornen estas consultas, de momento los metodos de consulta involucrados se limitan a la consulta de saldo con fecha de consulta y la recuperación de la TAG a traves de cuatro diferentes metodos. Tambien se reescribio buena parte del codigo para hacerlo mas legible.
