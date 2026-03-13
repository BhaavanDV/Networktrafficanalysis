import os

# Define the full folder & file structure
project_structure = {
    "NetworkTrafficAnalysis": {
        "data": {
            "raw": {},
            "processed": {},
            "metadata": {}
        },
        "notebooks": {
            "01_data_exploration.ipynb": None,
            "02_feature_engineering.ipynb": None,
            "03_model_training.ipynb": None,
            "04_model_evaluation.ipynb": None
        },
        "src": {
            "__init__.py": None,
            "data": {
                "load_data.py": None,
                "preprocess.py": None,
                "feature_engineering.py": None
            },
            "models": {
                "train_model.py": None,
                "evaluate_model.py": None,
                "predict.py": None,
                "model_utils.py": None
            },
            "network": {
                "capture.py": None,
                "packet_analysis.py": None,
                "traffic_simulation.py": None
            },
            "dashboard": {
                "app.py": None,
                "layout.py": None,
                "callbacks.py": None,
                "components": {
                    "graphs.py": None,
                    "tables.py": None
                },
                "assets": {
                    "style.css": None,
                    "script.js": None
                }
            },
            "services": {
                "ml_service.py": None,
                "alert_service.py": None,
                "db_service.py": None
            },
            "utils": {
                "logger.py": None,
                "config.py": None,
                "helpers.py": None
            }
        },
        "tests": {},
        "logs": {},
        "output": {},
        "deployment": {}
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if content is None:
            # It's a file
            open(path, 'w').close()
        else:
            # It's a directory
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)

# Run the script
create_structure(".", project_structure)
print("Project structure created successfully!")