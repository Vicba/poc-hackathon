export const checkDrawingScore = async ({ cirquitLabel, drawing }) => {
    const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ label: cirquitLabel, image: drawing }),
    });

    if (!response.ok) {
        throw new Error("Failed to check the drawing score");
    }

    return response.json();
}