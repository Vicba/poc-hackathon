"use client";

import {
    forwardRef,
    useEffect,
    useImperativeHandle,
    useRef,
    useState,
} from "react";
import { Button } from "./ui/button";
import { fabric } from "fabric";
import { FabricJSCanvas, useFabricJSEditor } from "fabricjs-react";
import { checkDrawingScore } from "@/lib/requests";

export const QuizQuestion = forwardRef(
    ({ question, handleNext, incrementScore, handleTimeout }, ref) => {
        const { editor, onReady } = useFabricJSEditor();
        const canvasWrapper = useRef(null);

        useEffect(() => {
            if (!editor || !fabric || !canvasWrapper) return;

            editor.canvas.setWidth(380);
            editor.canvas.setHeight(380);
            editor.canvas.isDrawingMode = true;
            editor.canvas.renderOnAddRemove = true;
            editor.canvas.freeDrawingBrush.width = 2;
            editor.canvas.renderAll();
        }, [editor?.canvas]);

        const handleSubmit = async () => {
            editor.canvas.isDrawingMode = false;
            editor.canvas.backgroundColor = "#fff";
            const data = editor.canvas.toDataURL();
            editor.canvas.backgroundColor = "transparent";
            const base64Data = data.replace(/^data:image\/png;base64,/, "");

            console.log(question.cirquit.id);
            console.log(base64Data);

            // Assuming checkDrawingScore and currentQuestion are defined elsewhere
            const score = await checkDrawingScore({
                cirquitLabel: question.cirquit.id,
                drawing: base64Data,
            });

            incrementScore(score.prediction ? 1 : 0);
            editor.canvas.clear();
            editor.canvas.isDrawingMode = true;
        };

        const onReset = () => {
            editor.canvas.clear();
        };

        // Expose handleSubmit function to parent component
        useImperativeHandle(ref, () => ({
            handleCheck: handleSubmit,
        }));

        return (
            <>
                <h2 className="text-3xl">
                    Draw{" "}
                    <span className="font-bold">{question.cirquit.name}</span>
                </h2>
                <div
                    ref={canvasWrapper}
                    className="w-[380px] h-[380px] bg-gray-200 rounded-lg overflow-hidden relative"
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
            </>
        );
    }
);
