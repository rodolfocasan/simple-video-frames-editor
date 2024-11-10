# Simple Video Frames Editor

`Simple Video Frames Editor` es una aplicación de escritorio desarrollada en Python con la librería `Tkinter`, originalmente creada como una herramienta personal para facilitar el procesamiento de frames de video. Aunque se puede compartir, es importante tener en cuenta que algunas funcionalidades y flujos de trabajo están diseñados de acuerdo a mis preferencias personales y pueden no estar totalmente optimizados para otros usuarios.

## Características

- **Extraer Frames**: Selecciona uno o varios videos y extrae sus frames.
- **Unir Frames**: Selecciona una secuencia de frames para combinarlos en un video.
- **Interfaz gráfica personalizada**: La aplicación tiene un tema oscuro y una ventana responsive, ajustada a mis preferencias, lo que podría no resultar ideal para todos los usuarios.

## Advertencias

Dado que esta herramienta fue inicialmente desarrollada para uso propio, algunas decisiones de diseño y experiencia de usuario podrían ser incómodas o confusas para otras personas:

- **Flujos no estándar**: Algunas acciones pueden requerir pasos adicionales que yo prefiero, pero que pueden no seguir los flujos más intuitivos.
- **Personalización limitada**: La interfaz y las opciones de configuración son mínimas y están alineadas a mis necesidades personales.
- **Mensajes de error poco detallados**: Los mensajes de error no siempre ofrecen una descripción clara de lo que ocurrió, ya que están pensados más para mi propio debugging rápido.

## Requisitos

Para poder ejecutar esta aplicación, asegúrate de tener instalado lo siguiente:

- Python 3.x+ (la versión usada fue Python 3.11.4)
- Tkinter (que viene con la mayoría de distribuciones de Python)
- Librerías adicionales como `opencv-python` o `Pillow` para el procesamiento de imágenes y videos.

## Instalación

1. Clona este repositorio:

    ```bash
    git clone https://github.com/rodolfocasan/simple-video-frames-editor.git
    cd simple-video-frames-editor
    ```

2. (Opcional) Crea y activa un entorno virtual:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3. Instala las dependencias necesarias:

    ```bash
    pip3 install -r DOCs/requirements.txt
    ```

4. Ejecuta la aplicación:

    ```bash
    python3 main.py
    ```