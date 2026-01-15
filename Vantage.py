"""
-------------------------------------------------------------------------
PROJECT VANTAGE: MICRO-SAFETY LAYER (PROTOTYPE)
-------------------------------------------------------------------------
Author: Aryan India Gavaskar
Platform: Python 3.10+ / OpenCV / Ultralytics YOLOv8
Hardware: Laptop Camera (Simulating Headset) -> Raspberry Pi 5 Logic

DESCRIPTION:
This script acts as the "Visual Cortex" for the Vantage system.
1. Captures real-time video from the headset (webcam).
2. Runs a quantized YOLOv8 Nano model for low-latency inference.
3. Filters for specific 'High-Stakes' hazards (Vehicles, Pedestrians, Obstacles).
4. Simulates the 'Bone Conduction' audio trigger based on proximity.
-------------------------------------------------------------------------
"""

import cv2
import math
import time
from ultralytics import YOLO

# --- CONFIGURATION ---
MODEL_PATH = "yolov8n.pt"      # Using 'Nano' model for highest FPS on Raspberry Pi
CONFIDENCE_THRESHOLD = 0.55    # Ignore low-confidence guesses to reduce false alarms
AUDIO_COOLDOWN = 2.0           # Seconds to wait before repeating the same warning

# --- HAZARD MAPPING ---
# The COCO dataset (standard YOLO) doesn't have "Stairs".
# For this prototype, we map similar shapes to represent our hazards.
# In the final version, we train on a custom 'Indian Street' dataset.
HAZARD_MAP = {
    0: "Pedestrian (Dynamic)",      # Person
    1: "Cyclist (Dynamic)",         # Bicycle
    2: "Car (Dynamic)",             # Car
    3: "Bike (Dynamic)",            # Motorcycle
    5: "Bus (Dynamic)",             # Bus
    7: "Truck (Dynamic)",           # Truck
    13: "Verticality (Bench/Step)", # Bench (Simulates Stairs/Curbs for demo)
    56: "Obstacle (Chair)"          # Chair (Simulates generic construction blocks)
}

class VantageSystem:
    def __init__(self):
        print("[INIT] Loading Vantage Logic Core...")
        
        # Load the Model
        self.model = YOLO(MODEL_PATH)
        
        # Initialize Camera (0 = Default Webcam)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1280) # Width
        self.cap.set(4, 720)  # Height
        
        # Audio Cooldown Timer (To prevent spamming the user)
        self.last_audio_time = 0
        
        print("[SUCCESS] System Active. Press 'Q' to shutdown.")

    def trigger_bone_conduction(self, message):
        """
        Simulates sending an audio signal to the bone-conduction transducers.
        In the hardware version, this triggers the I2S Amp on the Pi.
        """
        current_time = time.time()
        
        # Only speak if enough time has passed (Audio Cooldown)
        if current_time - self.last_audio_time > AUDIO_COOLDOWN:
            print(f"\n>>> [BONE CONDUCTION AUDIO]: 'Warning! {message} ahead.' <<<\n")
            self.last_audio_time = current_time

    def estimate_distance(self, box_width, frame_width):
        """
        Simple heuristic: The wider the object is in the frame, the closer it is.
        Returns: Estimated distance in meters (Approximate)
        """
        # This is a basic estimation formula for the prototype
        # Real version uses Depth Cameras or Stereo Vision
        perceived_width = box_width / frame_width
        if perceived_width > 0.8: return 0.5  # Very Close (<1m)
        if perceived_width > 0.4: return 1.5  # Close (<2m)
        return 3.0                            # Safe Distance (>3m)

    def run(self):
        while True:
            success, frame = self.cap.read()
            if not success:
                print("[ERROR] Camera disconnected.")
                break

            # Run Inference (stream=True for speed)
            results = self.model(frame, stream=True, verbose=False)
            
            height, width, _ = frame.shape

            # Process Detections
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    # Get Confidence
                    conf = math.ceil((box.conf[0] * 100)) / 100
                    
                    # Get Class ID
                    cls_id = int(box.cls[0])

                    # FILTER: Only act on relevant hazards
                    if conf > CONFIDENCE_THRESHOLD and cls_id in HAZARD_MAP:
                        
                        label = HAZARD_MAP[cls_id]
                        
                        # Get Coordinates
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        
                        # Estimate Proximity
                        obj_width = x2 - x1
                        distance = self.estimate_distance(obj_width, width)

                        # LOGIC: VISUALIZATION
                        # Color coding: Red for Close (<1.5m), Green for Safe
                        color = (0, 0, 255) if distance < 2.0 else (0, 255, 0)
                        
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
                        
                        # Text Label on Screen
                        info_text = f"{label} | {distance}m"
                        cv2.putText(frame, info_text, (x1, y1 - 10), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                        # LOGIC: AUDIO TRIGGER (The "Arbitrator" Hook)
                        # If hazard is close (<2m), trigger the bone conduction warning
                        if distance < 2.0:
                            self.trigger_bone_conduction(label)

            # Display the User's View (Debug Screen)
            cv2.imshow('Vantage Co-Pilot Debug View', frame)

            # Exit on 'Q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("[STOP] Shutting down Vantage System...")
                break

        self.cap.release()
        cv2.destroyAllWindows()

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    app = VantageSystem()
    app.run()