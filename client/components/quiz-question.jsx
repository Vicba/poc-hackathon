"use client";

import { useEffect, useRef, useState } from "react";
import { Button } from "./ui/button";
import { fabric } from "fabric";
import { FabricJSCanvas, useFabricJSEditor } from "fabricjs-react";

export function QuizQuestion() {
    const { editor, onReady } = useFabricJSEditor();

    const canvasWrapper = useRef(null);

    useEffect(() => {
        if (!editor || !fabric || !canvasWrapper) return;

        editor.canvas.setWidth(400);
        editor.canvas.setHeight(400);
        editor.canvas.isDrawingMode = true;
        editor.canvas.renderOnAddRemove = true;
        editor.canvas.freeDrawingBrush.width = 2;
        editor.canvas.renderAll();
    }, [editor?.canvas]);

    // on resize
    useEffect(() => {
        const resizeHandler = () => {
            if (!editor || !canvasWrapper) return;

            editor.canvas.setWidth(canvasWrapper.current.offsetWidth);
            editor.canvas.setHeight(canvasWrapper.current.offsetHeight);
            editor.canvas.renderAll();
        };

        window.addEventListener("resize", resizeHandler);

        return () => {
            window.removeEventListener("resize", resizeHandler);
        };
    }, [editor?.canvas]);

    const handleSubmit = () => {
        editor.canvas.isDrawingMode = false; // Disable drawing mode before getting the data
        // set the background color to white
        editor.canvas.backgroundColor = "#fff";
        const data = editor.canvas.toDataURL();
        editor.canvas.backgroundColor = "transparent"; // reset the background color
        // remove the prefix
        const base64Data = data.replace(/^data:image\/png;base64,/, "");
        console.log(base64Data);
    };

    const onReset = () => {
        editor.canvas.clear();
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
                <div
                    ref={canvasWrapper}
                    className="w-[400px] h-[400px] bg-gray-200 rounded-lg overflow-hidden relative"
                >
                    <FabricJSCanvas
                        className="sample-canvas"
                        onReady={onReady}
                    />
                    <Button
                        className="absolute top-4 right-4 z-10"
                        variant="secondary"
                        size="sm"
                        onClick={onReset}
                    >
                        Reset
                    </Button>
                </div>
                <Button
                    className="bg-gray-900 text-white px-6 py-3 rounded-md hover:bg-gray-800 transition-colors"
                    onClick={handleSubmit}
                >
                    Submit and Next
                </Button>
            </main>
        </div>
    );
}
