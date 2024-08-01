from microdot import Microdot, Response, send_file
from microdot.websocket import with_websocket 
from microdot.utemplate import Template
from robot_car import RobotCar
from utils import github_download
    
    
def download_files():
    github_download("aefrank", "esp32-wifi-robot-car", "static/css/custom.css")
    github_download("aefrank", "esp32-wifi-robot-car", "static/css/entireframework.min.css")
    github_download("aefrank", "esp32-wifi-robot-car", "static/js/custom.js")
    github_download("aefrank", "esp32-wifi-robot-car", "templates/index.html")
        
        
download_files()

# Web aoo
app = Microdot()
Response.default_content_type = "text/html"
PORT = 80


# Pico W GPIO Pin
LEFT_MOTOR_PIN_1 = 16
LEFT_MOTOR_PIN_2 = 17
RIGHT_MOTOR_PIN_1 = 18
RIGHT_MOTOR_PIN_2 = 19

motor_pins = (LEFT_MOTOR_PIN_1, LEFT_MOTOR_PIN_2, RIGHT_MOTOR_PIN_1, RIGHT_MOTOR_PIN_2)

# Create an instance of our robot car
robot_car = RobotCar(motor_pins, 20000)

car_commands = {
    "forward": robot_car.move_forward,
    "reverse": robot_car.move_backward,
    "left": robot_car.turn_left,
    "right": robot_car.turn_right,
    "stop": robot_car.stop,
}


# App Route
@app.route("/")
async def index(request):
    # print(f"Current Speed: {robot_car.get_current_speed()}")
    return Template("index.html").render(current_speed=robot_car.get_current_speed()) 


@app.route("/ws")
@with_websocket
async def executeCarCommands(request, ws):
    while True:
        websocket_message = await ws.receive()

        if "speed" in websocket_message:
            # WebSocket message format: "speed : 20"
            speedMessage = websocket_message.split(":")
            robot_car.change_speed(speedMessage[1])
        else:
            command = car_commands.get(websocket_message)
            if command is not None:
                command()
        ws.send("OK")


@app.route("/shutdown")
async def shutdown(request):
    request.app.shutdown()
    return "The server is shutting down..."


@app.route("/static/<path:path>")
def static(request, path):
    if ".." in path:
        # directory traversal is not allowed
        return "Not found", 404
    return send_file("static/" + path)


if __name__ == "__main__":
    print("Starting app...")
    try:
        app.run(port=PORT)
    finally:
        print("Shutting down app...")
        robot_car.deinit()
