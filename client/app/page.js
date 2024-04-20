"use client";

import { Button } from "@/components/ui/button";
import useStore from "@/hooks/useStore";
import { QUIZZES } from "@/lib/quizzes";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { set } from "react-hook-form";
import Web3 from 'web3';

export default function Home() {
    const router = useRouter();

    const { login, logout, isLoggedIn, address, resetEverything, setQuestions, setQuizId } = useStore();

    const connectWallet = async () => {
        if (typeof window.ethereum !== 'undefined') {
            try {
                const accounts = await window.ethereum.request({
                    method: 'eth_requestAccounts',
                })

                if (accounts.length === 0) {
                    console.log('No account connected')
                } else {
                    const web3 = new Web3(window.ethereum);
                    await login(accounts[0]);
                }
            } catch (error) {
                console.error('Error connecting wallet:', error.message)
            }
        } else {
            console.log('Ethereum provider not found')
        }
    }

    const disconnectWallet = () => {
        logout();
    }

    const startQuiz = (quizId) => {
        try {
            // Set store values
            resetEverything();
            setQuizId(quizId);
            const quiz = QUIZZES.find((q) => q.id === quizId);
            setQuestions(quiz.questions);

            // Redirect to quiz page
            router.push('/quiz');
        } catch (error) {
            console.error('Error starting quiz:', error.message)
        }
    }

    return (
        <main className="flex min-h-screen flex-col items-center justify-center p-24">
            {!isLoggedIn ? (
                <Button onClick={connectWallet}>Login {address}</Button>
            ) : (
                <Button onClick={disconnectWallet}>Logout {address}</Button>
            )}
            {isLoggedIn && (
                <div className="mt-10">
                    <Button variant="secondary" onClick={() => startQuiz(1)}>
                        Start Quiz #1
                    </Button>
                </div>
            )}
            <div className="mt-10">
                <Link href="/test-score" className="underline text-gray-400 hover:text-gray-700 underline-offset-4">
                    Test score
                </Link>
            </div>
        </main>
    );
}