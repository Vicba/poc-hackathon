"use client"

import { QuizQuestion } from "@/components/quiz-question";
import { Button } from "@/components/ui/button";
import useStore from "@/hooks/useStore";
import { formatTime } from "@/lib/utils";
import { useRouter } from "next/navigation";
import { useRef } from "react";
import { useTimer } from "react-timer-hook";

export default function Quiz() {
    const router = useRouter();
    const quizQuestionRef = useRef(null);
    const { isLoggedIn, questions, currentQuestion, quizId, incrementScore, incrementCurrentQuestion, incrementTotalTime, removeQuestions, resetCurrentQuestion } = useStore();
    const { seconds, minutes, restart } = useTimer({ autoStart: true, expiryTimestamp: new Date().getTime() + 1000 * 45, onExpire: handleTimeout });

    if (!isLoggedIn) {
        router.push("/");
    }

    async function handleTimeout() {
        if (quizQuestionRef.current) {
            incrementTotalTime(45);
            quizQuestionRef.current.handleCheck();

            if (currentQuestion === questions.length - 1) {
                router.push("/quiz/result");
                resetCurrentQuestion();
                return;
            }
            incrementCurrentQuestion();
            restart(new Date().getTime() + 1000 * 45);
        } else {
            console.error("Quizquestion is not defined");
        }
    }

    const handleNext = async () => {
        if (quizQuestionRef.current) {
            incrementTotalTime(45 - seconds);
            await quizQuestionRef.current.handleCheck();

            console.log("currentQuestion", currentQuestion, questions.length - 1)

            if (currentQuestion === questions.length - 1) {
                router.push("/quiz/result");
                resetCurrentQuestion();
                return;
            }
            incrementCurrentQuestion();
            restart(new Date().getTime() + 1000 * 45);
        } else {
            console.error("Quizquestion is not defined");
        }
    }


    return (
        <div className="flex flex-col h-screen">
            <header className="bg-gray-900 text-white py-4 px-6">
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                        <div className="w-full bg-gray-800 rounded-full h-2">
                            <div className="bg-green-500 h-2 rounded-full w-1/2" />
                        </div>
                        <span>{currentQuestion + 1 + "/" + questions.length}</span>
                    </div>
                    <div className="text-2xl font-bold">{formatTime(minutes)}:{formatTime(seconds)}</div>
                </div>
            </header>
            <main className="flex-1 flex flex-col items-center justify-center px-6 py-12 space-y-8">
                <QuizQuestion ref={quizQuestionRef} question={questions[currentQuestion]} handleNext={handleNext} incrementScore={incrementScore} currentQuestion={currentQuestion} />
                <Button
                    className="bg-gray-900 text-white px-6 py-3 rounded-md hover:bg-gray-800 transition-colors"
                    onClick={handleNext}
                >
                    Submit and Next
                </Button>
            </main>
        </div>
    )
}