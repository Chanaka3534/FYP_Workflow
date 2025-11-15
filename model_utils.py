import joblib
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError

def load_models():
    # Load LSTM model
    model_lstm = load_model('lstm_model.h5', compile=False)
    model_lstm.compile(optimizer=Adam(learning_rate=0.001), loss=MeanSquaredError())

    # Load XGBoost model
    model_xgb = joblib.load('xgboost_model.pkl')

    # Load scalers
    scaler_X = joblib.load('scaler_X.pkl')
    scaler_y = joblib.load('scaler_y.pkl')

    # Load label encoder
    le = joblib.load('label_encoder.pkl')

    return model_lstm, model_xgb, scaler_X, scaler_y, le
