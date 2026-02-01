function predict() {

    const data = {
        GENDER: Number(document.getElementById("GENDER").value),
        AGE: Number(document.getElementById("AGE").value),
        SMOKING: Number(document.getElementById("SMOKING").value),
        YELLOW_FINGERS: Number(document.getElementById("YELLOW_FINGERS").value),
        ANXIETY: Number(document.getElementById("ANXIETY").value),
        PEER_PRESSURE: Number(document.getElementById("PEER_PRESSURE").value),
        CHRONIC_DISEASE: Number(document.getElementById("CHRONIC_DISEASE").value),
        FATIGUE: Number(document.getElementById("FATIGUE").value),
        ALLERGY: Number(document.getElementById("ALLERGY").value),
        WHEEZING: Number(document.getElementById("WHEEZING").value),
        ALCOHOL_CONSUMING: Number(document.getElementById("ALCOHOL_CONSUMING").value),
        COUGHING: Number(document.getElementById("COUGHING").value),
        SHORTNESS_OF_BREATH: Number(document.getElementById("SHORTNESS_OF_BREATH").value),
        SWALLOWING_DIFFICULTY: Number(document.getElementById("SWALLOWING_DIFFICULTY").value),
        CHEST_PAIN: Number(document.getElementById("CHEST_PAIN").value)
    };

    if (!data.AGE || data.AGE <= 0) {
        alert("Please enter a valid age.");
        return;
    }

    fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(result => {
        const resultElement = document.getElementById("result");
        
        resultElement.innerText = result.result;

        if(result.prediction_code === 1) {
            resultElement.style.color = "red";
            resultElement.style.background = "#ffe6e6";
        } else {
            resultElement.style.color = "green";
            resultElement.style.background = "#e6ffec";
        }
    })
    .catch(err => {
        alert("Failed to connect to the API. Is the backend running?");
        console.error(err);
    });
}