"use client";

import dah from "../lib/abi.json";
import Web3 from 'web3';
import useStore from "@/hooks/useStore";
import { Button } from "@/components/ui/button";
import { useState, useEffect } from "react";

export function Overview() {

    const { address } = useStore();
    const web3 = new Web3(window.ethereum);
    const contract = new web3.eth.Contract(
        dah,
        "0xe8e9e68a61570ff81296543509722e2c5514025c"
    );
    const [overview, setOverview] = useState([]); // Initialize feedback state

    useEffect(() => {
        handleSubmit()
    }, [])

    async function handleSubmit () {
        try {
            setOverview([])
            const quizIds = await contract.methods.getQuizIds().call();
            const parsedQuizIds = quizIds.map(id => parseInt(id));
            console.log(parsedQuizIds);
            for (const quizId in parsedQuizIds) {
                const score = await contract.methods.getAverageScoreOfAddressOfQuiz(address, quizId).call()
                const parsedScore = parseInt(score);
                setOverview(prevOverview => [...prevOverview, {"quizId": quizId, "score": parsedScore}])
            }
            console.log(overview)
        } catch (error) {
            console.error(error)

        }
    }
    return (
        <div className="flex flex-col">
            <h2 className="text-3xl">Overview</h2>
            <ul className="flex flex-col">
                {overview.map((overview, index) => (
                <li key={index}>quizId: {overview.quizId} score: {overview.score}</li>
                ))}
            </ul>
        </div>
    );
}
