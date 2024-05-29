import modules.scripts as scripts
import gradio as gr
import os

from modules import images, script_callbacks
from modules.processing import process_images, Processed
from modules.processing import Processed
from modules.shared import opts, cmd_opts, state

class SkeletonPoseEditor(scripts.Script):
    def __init__(self) -> None:
        super().__init__()

    def title(self):
        return "3D Skeleton Pose Editor"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Accordion("Controls for 3D Skeleton", open=False):
            with gr.Row():
                reset_camera_button = gr.Button("Reset Camera", id="reset_camera")
                reset_pose_button = gr.Button("Reset Pose", id="reset_pose")
                all_reset_button = gr.Button("All Reset", id="all_reset")
            with gr.Row():
                add_body_button = gr.Button("Add Body", id="add_body")
                remove_body_button = gr.Button("Remove Body", id="remove_body")
                fixed_roll_checkbox = gr.Checkbox("Fixed Roll", id="fixed_roll")
            
                posex_html = gr.HTML('''
                    <div id="container" style="width: 512px; height: 512px;"></div>
                    <script type="module">
                        import { init, init_3d } from '/static/js/posex.js';
                        const ui = {
                            container: document.getElementById('container'),
                            reset_camera: document.getElementById('reset_camera'),
                            reset_pose: document.getElementById('reset_pose'),
                            all_reset: document.getElementById('all_reset'),
                            add_body: document.getElementById('add_body'),
                            remove_body: document.getElementById('remove_body'),
                            fixed_roll: document.getElementById('fixed_roll')
                        };
                        init(ui);
                        const animate = init_3d(ui);
                        animate();
                    </script>
                ''', css={"width": "100%", "height": "auto"})
                
                with gr.Row():
                    save_image_button = gr.Button("Save Image", id="save")
                    copy_clipboard_button = gr.Button("Copy to Clipboard", id="copy")

        return [
            reset_camera_button, reset_pose_button, all_reset_button,
            add_body_button, remove_body_button, fixed_roll_checkbox,
            save_image_button, copy_clipboard_button, posex_html
        ]

    # args is [StableDiffusionProcessing, UI1, UI2, ...]
    def run(self, p, angle, checkbox):
        # TODO: get UI info through UI object angle, checkbox
        proc = process_images(p)
        # TODO: add image edit process via Processed object proc
        return proc
