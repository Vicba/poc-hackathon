"use client";

import { useEffect, useRef, useState } from "react";
import { Button } from "./ui/button";
import { fabric } from "fabric";

export function QuizQuestion() {
    const [canvas, setCanvas] = useState(null);
    const canvasRef = useRef(null);

    useEffect(() => {
        setCanvas(new fabric.Canvas(canvasRef.current, {
            isDrawingMode: true,
            width: 800,
            height: 600,
            renderOnAddRemove: true,
        }));
    }, []);

    const handleSubmit = () => {
        canvas.isDrawingMode = false; // Disable drawing mode before getting the data
        const data = canvas.toDataURL();
        console.log(data);
    };

    return (
        <div className="flex flex-col h-screen">
            <header className="bg-gray-900 text-white py-4 px-6">
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                        <div className="w-full bg-gray-800 rounded-full h-2">
                            <div className="bg-green-500 h-2 rounded-full w-1/2" />
                        </div>
                        <span>1/10</span>
                    </div>
                    <div className="text-2xl font-bold">00:45</div>
                </div>
            </header>
            <main className="flex-1 flex flex-col items-center justify-center px-6 py-12 space-y-8">
                <h2 className="text-3xl font-bold">
                    Draw the Circuit of The Americas
                </h2>
                <div className="w-full max-w-3xl aspect-video bg-gray-200 rounded-lg overflow-hidden">
                    <canvas ref={canvasRef} />
                </div>
                <Button
                    className="bg-gray-900 text-white px-6 py-3 rounded-md hover:bg-gray-800 transition-colors"
                    onClick={() => handleSubmit()}
                >
                    Submit and Next
                </Button>
            </main>
        </div>
    );
}
