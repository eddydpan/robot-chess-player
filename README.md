# Chess-Bot

## Welcome!

Welcome to the Chess-bot landing page. This repository hosts a ROS package that enables a WidowX-200 robotic arm to play chess in real-time against a human player. The package allows the robot to:

- Interpret the changing chessboard using machine vision.
- Calculate the optimal move.
- Physically pick up and place chess pieces to execute its move.

---

## Meet the Team

- **Will Young**  
  Will is a mechanical engineering student at Olin College of Engineering (Class of 2024). He is enthusiastic about robotic arm control, path planning, and ensuring a robust ROS structure for the project. While not a chess master, he claims watching Gotham Chess twice makes him an expert.

- **Mia Chevere**  
  Mia is an electrical and computer engineering student at Olin College of Engineering. She’s excited about the kinematics math involved in moving the arm to precise locations—despite never having taken basic geometry!

- **Eddy Pan**  
  Eddy is an engineering with computing student at Olin College of Engineering. A former chess prodigy (4th grade), Eddy has dreamed of creating a chess bot ever since declaring his major. He’s determined to make a safer, better chess bot than those that break fingers.

- **Dan Park**  
  Dan is an engineering with computing student at Olin College of Engineering (Class of 2025). He reached the round of 16 in the JPMorgan Chess Competition, so he’s “okay” at chess.

---

## Package Structure

This ROS package is organized into the following nodes:

### **1. Perception**
- Captures camera input to identify which chess pieces occupy which squares on the board.

### **2. Movement Calculator**
- Uses information from the perception node to recreate the board and determine the robot's next move.
- The move is calculated using discrete math inspired by Eddy’s final exam.
- Sends the move decision to the Path Planner node.

### **3. Path Planner**
- Utilizes the known relationship between the chessboard and the Widow X arm to estimate the pose of each square.
- Generates waypoints to guide the arm along its trajectory.

### **4. Arm Movement Controller**
- Guides the Widow X to move along waypoints and adjusts its grip as needed to pick up and place chess pieces.

---

## Milestone 1

After the first week, the team made significant progress on three key fronts:

### **1. Computational Setup**
- Integrated the **robot bridge repository** from the Berkeley Robot and AI Laboratory to control the Widow X.
- Set up a functional simulator using the **Trossen Robotics X Series Arms Simulator** to enable testing without physical access to the robot.
- Created a collection of helpful commands for controlling the arm.
- Established a plan for deliverables by the next milestone.

### **2. Background Research**
- Researched previous uses of the Widow X, prior chess bots, and kinematic arm theory.
- Gained insights into:
  - Structuring ROS packages for the Widow X.
  - Parallel vs. forward kinematics.
  - Machine vision depth solutions.

### **3. Structure Plan**
- Developed a preliminary system architecture, detailed in the "Package Structure" section above.
- Focused on scoping the Minimum Viable Product (MVP) effectively. For example, alternative methods for pose estimation are prioritized over implementing stereo vision depth estimation.

### **4. Next Steps**
We aim to accomplish a few toy problems that will segue nicely into our project. We will focus on a pick-and-place module and a "move to (x,y,z)" module, which once integrated together alongside a basic chess engine, will act as our MVP. 

### **5. Website**
- Successfully launched this website! You’re looking at it now!

While many details of this project are still in development, the team has a solid foundation and is eager to tackle the challenges ahead.
