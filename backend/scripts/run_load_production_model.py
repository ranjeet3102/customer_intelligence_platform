from src.model_registry.loader import load_production_model

def main():

    artifact = load_production_model()
    print(f"Loaded production model:")
    print(f"Model: {artifact['model']}")
    print(f"Name: {artifact['model_name']}")
    print(f"Type: {artifact['model_type']}")
    print(f"Feature Version: {artifact['feature_version']}")
    print(f"Metrics: {artifact['metrics']}")

if __name__ == "__main__":
    main()
