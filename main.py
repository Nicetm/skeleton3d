import gradio as gr
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image, ImageDraw
import base64
from io import BytesIO

app = FastAPI()

# Servir la carpeta static como estática
app.mount("/static", StaticFiles(directory="static"), name="static")

# Añadir una ruta para verificar la carga de script.js
@app.get("/")
async def read_root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page</title>
        <script>
            var initial_image_data = 'PLACEHOLDER_FOR_IMAGE_DATA';
            var initial_joints = PLACEHOLDER_FOR_JOINTS;
        </script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.134.0/examples/js/controls/OrbitControls.js"></script>
        <script src="/static/skeleton3d.js"></script>
    </head>
    <body>
        <h1>Test Page</h1>
        <canvas id="canvas-container" width="512" height="512"></canvas>
    </body>
    </html>
    """
    # Generate initial image data
    joints = {
        "nose": (250, 50),
        "neck": (250, 100),
        "right_shoulder": (300, 100),
        "right_elbow": (350, 150),
        "right_wrist": (400, 200),
        "left_shoulder": (200, 100),
        "left_elbow": (150, 150),
        "left_wrist": (100, 200),
        "right_hip": (300, 250),
        "right_knee": (300, 350),
        "right_ankle": (300, 450),
        "left_hip": (200, 250),
        "left_knee": (200, 350),
        "left_ankle": (200, 450),
        "right_eye": (270, 40),
        "left_eye": (230, 40),
        "right_ear": (280, 50),
        "left_ear": (220, 50),
        "mouth": (250, 60)
    }

    colors = {
        "torso": "red",
        "right_arm": "green",
        "left_arm": "blue",
        "right_leg": "yellow",
        "left_leg": "purple",
        "face": "orange"
    }

    def generate_skeleton_image(joints):
        width, height = 512, 768  # Nuevo tamaño del canvas
        image = Image.new('RGB', (width, height), (0, 0, 0))  # Fondo negro
        draw = ImageDraw.Draw(image)
        
        # Conectar las articulaciones con líneas estilo OpenPose
        draw.line([joints["nose"], joints["neck"]], fill=colors["torso"], width=2)
        draw.line([joints["neck"], joints["right_shoulder"]], fill=colors["right_arm"], width=2)
        draw.line([joints["right_shoulder"], joints["right_elbow"]], fill=colors["right_arm"], width=2)
        draw.line([joints["right_elbow"], joints["right_wrist"]], fill=colors["right_arm"], width=2)
        draw.line([joints["neck"], joints["left_shoulder"]], fill=colors["left_arm"], width=2)
        draw.line([joints["left_shoulder"], joints["left_elbow"]], fill=colors["left_arm"], width=2)
        draw.line([joints["left_elbow"], joints["left_wrist"]], fill=colors["left_arm"], width=2)
        draw.line([joints["right_hip"], joints["right_knee"]], fill=colors["right_leg"], width=2)
        draw.line([joints["right_knee"], joints["right_ankle"]], fill=colors["right_leg"], width=2)
        draw.line([joints["left_hip"], joints["left_knee"]], fill=colors["left_leg"], width=2)
        draw.line([joints["left_knee"], joints["left_ankle"]], fill=colors["left_leg"], width=2)
        draw.line([joints["neck"], joints["right_hip"]], fill=colors["torso"], width=2)
        draw.line([joints["neck"], joints["left_hip"]], fill=colors["torso"], width=2)
        
        # Conectar los puntos de la cara
        draw.line([joints["nose"], joints["right_eye"]], fill=colors["face"], width=2)
        draw.line([joints["nose"], joints["left_eye"]], fill=colors["face"], width=2)
        draw.line([joints["right_eye"], joints["right_ear"]], fill=colors["face"], width=2)
        draw.line([joints["left_eye"], joints["left_ear"]], fill=colors["face"], width=2)
        draw.line([joints["nose"], joints["mouth"]], fill=colors["face"], width=2)

        # Dibujar puntos en las articulaciones
        for joint in joints.values():
            draw.ellipse((joint[0] - 5, joint[1] - 5, joint[0] + 5, joint[1] + 5), fill=(255, 255, 255))
        
        return image

    def pil_to_base64(img):
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_data = base64.b64encode(buffered.getvalue()).decode()
        return img_data

    initial_image = generate_skeleton_image(joints)
    initial_image_data = pil_to_base64(initial_image)

    html_content = html_content.replace("PLACEHOLDER_FOR_IMAGE_DATA", initial_image_data)
    html_content = html_content.replace("PLACEHOLDER_FOR_JOINTS", str(joints).replace("'", '"'))

    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
