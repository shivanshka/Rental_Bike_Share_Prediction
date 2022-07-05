from Prediction_Application.pipeline.training_pipeline import Training_Pipeline


def main():
    train = Training_Pipeline()
    print(train.run_training_pipeline())

if __name__ == "__main__":
    main()