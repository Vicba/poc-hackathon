"use client"

import { QuizQuestion } from "@/components/quiz-question";
import { Button } from "@/components/ui/button";
import useStore from "@/hooks/useStore";
import { formatTime } from "@/lib/utils";
import { useRouter } from "next/navigation";
import { useRef, useState } from "react";
import { useTimer } from "react-timer-hook";

export default function Quiz() {
    const router = useRouter();
    const quizQuestionRef = useRef(null);
    const { isLoggedIn, questions, currentQuestion, quizId, incrementScore, incrementCurrentQuestion, incrementTotalTime, removeQuestions, resetCurrentQuestion } = useStore();
    const { seconds, minutes, restart } = useTimer({ autoStart: true, expiryTimestamp: new Date().getTime() + 1000 * 45, onExpire: handleTimeout });
    const [loading, setLoading] = useState(false);

    if (!isLoggedIn) {
        router.push("/");
    }

    async function handleTimeout() {
        if (quizQuestionRef.current) {
            setLoading(true);
            incrementTotalTime(45);
            quizQuestionRef.current.handleCheck();

            if (currentQuestion == questions.length - 1) {
                router.push("/quiz/result");
                resetCurrentQuestion();
                setLoading(false);
                return;
            }
            console.log("incrementing")
            incrementCurrentQuestion();
            restart(new Date().getTime() + 1000 * 45);
            setLoading(false);
        } else {
            console.error("Quizquestion is not defined");
            setLoading(false);
        }
    }

    const handleNext = async () => {
        if (quizQuestionRef.current) {
            setLoading(true);
            incrementTotalTime(45 - seconds);
            await quizQuestionRef.current.handleCheck();

            console.log("currentQuestion", currentQuestion, questions.length - 1)

            if (currentQuestion == questions.length - 1) {
                router.push("/quiz/result");
                setLoading(false);
                return;
            }
            console.log("incrementing")
            incrementCurrentQuestion();
            restart(new Date().getTime() + 1000 * 45);
            setLoading(false);
        } else {
            console.error("Quizquestion is not defined");
            setLoading(false);
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
            {loading && (
                <div className="fixed inset-0 w-full h-full top-0 bottom-0 bg-slate-800 bg-opacity-10">
                    <main className="flex-1 flex flex-col items-center justify-center px-6 py-12 space-y-8">
                        <div role="status">
                            <svg aria-hidden="true" className="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-slate-800" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor" />
                                <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill" />
                            </svg>
                            <span className="sr-only">Loading...</span>
                        </div>
                    </main>
                </div>
            )}
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