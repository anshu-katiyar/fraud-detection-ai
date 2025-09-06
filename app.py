from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
from datetime import datetime

app = Flask(__name__)

# Load optimized model and scaler
model_data = pickle.load(open("model.pkl", "rb"))
model = model_data['model']
scaler = model_data['scaler']

# Transaction history
transaction_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        amount = float(request.form["amount"])
        time = int(request.form["time"])
        location = request.form["location"]
        device = request.form["device"]
        frequency = int(request.form.get("frequency", 1))

        # Encode features
        loc_value = 1 if location.lower() != "india" else 0
        dev_value = 1 if device.lower() == "mobile" else 0

        # Create feature array
        features = np.array([[amount, time, loc_value, dev_value, frequency]])
        features_scaled = scaler.transform(features)

        # Get prediction and confidence
        prediction = model.predict(features_scaled)[0]
        confidence = model.predict_proba(features_scaled)[0].max()

        # Risk assessment
        risk_level = "High" if confidence > 0.8 else "Medium" if confidence > 0.6 else "Low"
        
        if prediction == 1:
            result = f"❌ Fraudulent Transaction Detected! (Confidence: {confidence:.1%}, Risk: {risk_level})"
            status = "fraud"
        else:
            result = f"✅ Genuine Transaction (Confidence: {confidence:.1%}, Risk: {risk_level})"
            status = "genuine"

        # Store transaction
        transaction_history.append({
            'amount': amount, 'time': time, 'location': location,
            'device': device, 'result': status, 'confidence': confidence,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    except Exception as e:
        result = f"⚠️ Error: {str(e)}"
        status = "error"

    return render_template("index.html", prediction_text=result)

@app.route("/api/predict", methods=["POST"])
def api_predict():
    try:
        data = request.json
        features = np.array([[data['amount'], data['time'], 
                            1 if data['location'].lower() != 'india' else 0,
                            1 if data['device'].lower() == 'mobile' else 0,
                            data.get('frequency', 1)]])
        features_scaled = scaler.transform(features)
        
        prediction = model.predict(features_scaled)[0]
        confidence = model.predict_proba(features_scaled)[0].max()
        
        return jsonify({
            'prediction': 'fraud' if prediction == 1 else 'genuine',
            'confidence': float(confidence),
            'risk_level': 'High' if confidence > 0.8 else 'Medium' if confidence > 0.6 else 'Low'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/history")
def history():
    return render_template("history.html", transactions=transaction_history[-10:])

@app.route("/payment")
def payment():
    return render_template("payment.html")

@app.route("/payment/success", methods=["POST"])
def payment_success():
    try:
        data = request.json
        # Store payment info (in production, save to database)
        payment_info = {
            'payment_id': data.get('payment_id'),
            'plan': data.get('plan'),
            'amount': data.get('amount'),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify({'status': 'success', 'message': 'Payment recorded'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == "__main__":
    # For production deployment
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
