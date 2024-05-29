document.addEventListener("DOMContentLoaded", function() {
    console.log("Script loaded - Test Page");

    var canvas2D = document.getElementById('canvas-container');
    if (!canvas2D) {
        console.error("Canvas element not found!");
        return;
    }

    var ctx = canvas2D.getContext('2d');
    if (!ctx) {
        console.error("Unable to get canvas context!");
        return;
    }

    var initial_joints = {
        "nose": [250, 50],
        "neck": [250, 100],
        "right_shoulder": [300, 100],
        "right_elbow": [350, 150],
        "right_wrist": [400, 200],
        "left_shoulder": [200, 100],
        "left_elbow": [150, 150],
        "left_wrist": [100, 200],
        "right_hip": [300, 250],
        "right_knee": [300, 350],
        "right_ankle": [300, 450],
        "left_hip": [200, 250],
        "left_knee": [200, 350],
        "left_ankle": [200, 450],
        "right_eye": [270, 40],
        "left_eye": [230, 40],
        "right_ear": [280, 50],
        "left_ear": [220, 50],
        "mouth": [250, 60]
    };

    var joints = initial_joints;
    var selectedJoint = null;

    var colors = {
        "torso": "white",
        "right_arm": "green",
        "left_arm": "blue",
        "right_leg": "yellow",
        "left_leg": "purple",
        "face": "orange"
    };

    var image = new Image();
    image.src = 'data:image/png;base64,' + initial_image_data;

    image.onload = function() {
        drawSkeleton();  // Draw initial skeleton once
    };

    canvas2D.addEventListener('mousedown', function(event) {
        if (event.target.id === "canvas-container") {
            controls.enabled = true; // Enable camera controls
        }
        var x = event.offsetX;
        var y = event.offsetY;
        selectedJoint = null;  // Reset selected joint
        for (var joint in joints) {
            var dx = joints[joint][0] - x;
            var dy = joints[joint][1] - y;
            var distance = dx * dx + dy * dy;
            if (distance < 100) {  // Click within 10px radius
                selectedJoint = joint;
                break;
            }
        }
        if (event.target.id !== "canvas-container") {
            controls.enabled = false; // Disable camera controls
        }
    });

    canvas2D.addEventListener('mousemove', function(event) {
        if (selectedJoint) {
            var x = event.offsetX;
            var y = event.offsetY;
            joints[selectedJoint] = [x, y];
            ctx.clearRect(0, 0, canvas2D.width, canvas2D.height);
            drawSkeleton();
        }
    });

    canvas2D.addEventListener('mouseup', function() {
        selectedJoint = null;
    });

    function drawSkeleton() {
        ctx.fillStyle = "black";
        ctx.fillRect(0, 0, canvas2D.width, canvas2D.height);

        ctx.lineWidth = 2;

        function drawLine(joint1, joint2, color) {
            ctx.strokeStyle = color;
            ctx.beginPath();
            ctx.moveTo(joints[joint1][0], joints[joint1][1]);
            ctx.lineTo(joints[joint2][0], joints[joint2][1]);
            ctx.stroke();
        }

        drawLine("nose", "neck", colors["torso"]);
        drawLine("neck", "right_shoulder", colors["right_arm"]);
        drawLine("right_shoulder", "right_elbow", colors["right_arm"]);
        drawLine("right_elbow", "right_wrist", colors["right_arm"]);
        drawLine("neck", "left_shoulder", colors["left_arm"]);
        drawLine("left_shoulder", "left_elbow", colors["left_arm"]);
        drawLine("left_elbow", "left_wrist", colors["left_arm"]);
        drawLine("neck", "right_hip", colors["torso"]);
        drawLine("right_hip", "right_knee", colors["right_leg"]);
        drawLine("right_knee", "right_ankle", colors["right_leg"]);
        drawLine("neck", "left_hip", colors["torso"]);
        drawLine("left_hip", "left_knee", colors["left_leg"]);
        drawLine("left_knee", "left_ankle", colors["left_leg"]);

        drawLine("nose", "right_eye", colors["face"]);
        drawLine("right_eye", "right_ear", colors["face"]);
        drawLine("nose", "left_eye", colors["face"]);
        drawLine("left_eye", "left_ear", colors["face"]);
        drawLine("nose", "mouth", colors["face"]);

        for (var joint in joints) {
            ctx.beginPath();
            ctx.arc(joints[joint][0], joints[joint][1], 5, 0, 2 * Math.PI);
            ctx.fillStyle = "white";
            ctx.fill();
            ctx.strokeStyle = "white";
            ctx.stroke();
        }
    }


});
