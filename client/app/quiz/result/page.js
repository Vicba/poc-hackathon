"use client"

import { Button } from "@/components/ui/button";
import useStore from "@/hooks/useStore";
import { useRouter } from "next/navigation";
import Web3 from "web3";
import dah from "../../../lib/abi.json";
import { sendTransaction } from "@/web3/ethereum";
import { toast } from "@/components/ui/use-toast";

export default function Result() {
    const router = useRouter();
    const { isLoggedIn, questions, score, totalTime, address, quizId, resetEverything } = useStore();
    const web3 = new Web3(window.ethereum);
    const contract = new web3.eth.Contract(
        dah,
        "0x8a2270531063d97555047acb2f79b86cc0173824"
    );

    if (!isLoggedIn) {
        router.push("/");
    }

    const handleSave = async () => {
        try {
            const method = contract.methods.uploadScoreOfLesson(quizId, score);
            const txHash = await sendTransaction(method, contract, address);
            const scoreFromBlockchain = await contract.methods.getAverageScoreOfAddressOfLesson(address, quizId).call();
            console.log(parseInt(scoreFromBlockchain))
            router.push("/");
            toast({
                title: "Score opgeslagen",
                description: `Je score is opgeslagen in de blockchain. Je score is: ${scoreFromBlockchain}`,
                status: "success",
            })
            resetEverything();
        } catch (error) {
            console.error(error);
        }
    }


    return (
        <div className="flex flex-col h-screen">
            <main className="flex-1 flex flex-col items-center justify-center px-6 py-12 space-y-8">
                <h1 className="text-3xl font-bold">Score</h1>
                <h2 className="text-lg">Je score is: <span className="font-bold">{score / questions.length * 100}%</span></h2>
                <h3>Met een tijd van <span>{totalTime}</span> seconden</h3>

                <Button onClick={handleSave}>Score opslaan</Button>
            </main>
        </div>
    )
}