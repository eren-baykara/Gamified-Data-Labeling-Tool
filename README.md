# ⚔️ Label Wars: Gamified Data Labeling Tool

**"Turn boring data annotation into a competitive team sport!"**

Label Wars is a collaborative, desktop-based image labeling tool designed to accelerate Computer Vision dataset preparation. By integrating gamification mechanics (leaderboards, combos, points), it boosts team motivation and labeling speed significantly.

> **Key Feature:** It transforms a mundane task like "moving files to folders" into a real-time competition among data annotators.

## 📸 Features

* **🎮 Gamification Engine:** Earn points for every labeled image.
* **🏆 Live Leaderboard:** Real-time ranking of team members stored in a shared SQLite database.
* **⚡ High-Speed Workflow:** Optimized keyboard shortcuts (1, 2, 3) allow labeling thousands of images per hour.
* **↩️ Smart Undo:** Made a mistake? The Undo function reverts the file move and adjusts the score automatically.
* **👑 Admin Panel:** A CLI tool for team leaders to manage user scores and reset competitions.

## 🛠️ Technology Stack

* **Python 3.x**: Core logic.
* **Tkinter**: Native GUI for zero-latency image rendering.
* **SQLite**: Lightweight database for tracking user scores and logs.
* **Pillow (PIL)**: High-performance image processing.

## 🚀 Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/erenbaykara/Gamified-Data-Labeling-Tool.git](https://github.com/erenbaykara/Gamified-Data-Labeling-Tool.git)
    cd Gamified-Data-Labeling-Tool
    ```

2.  **Install dependencies:**
    ```bash
    pip install Pillow
    ```

3.  **Prepare your data:**
    * Place your raw images into the `data_to_label` folder.

4.  **Run the game:**
    ```bash
    python app.py
    ```
    * *Enter your username and start the battle!*

## 🕹️ Controls

| Key | Action | Category |
| :--- | :--- | :--- |
| **1** | Move to `Single_Color` | 🟦 Single Color Items |
| **2** | Move to `Detail` | 🔍 Detailed Textures |
| **3** | Move to `Multi_Color` | 🌈 Multi-Colored Items |
| **Ctrl+Z** | Undo Last Action | ↩️ Revert Move |

## 👑 Admin Panel
To manage the leaderboard or fix scores, run the admin script:

```bash
python admin_panel.py
