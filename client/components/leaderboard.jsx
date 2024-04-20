"use client";

import dah from "../lib/abi.json";
import Web3 from 'web3';
import { useState, useEffect } from "react";

export function Leaderboard() {
    const web3 = new Web3(window.ethereum);
    const contract = new web3.eth.Contract(
        dah,
        "0xe8e9e68a61570ff81296543509722e2c5514025c"
    );
    const [leaderboard, setLeaderboard] = useState([]); // Initialize feedback state

    useEffect(() => {
        loadLeaderboard()
    }, [])

    async function loadLeaderboard() {
        try {
            setLeaderboard([])
            const addresses = await contract.methods.getAddresses().call();
            console.log(addresses)
            const quizIds = await contract.methods.getQuizIds().call();
            const parsedQuizIds = quizIds.map(id => parseInt(id));
            console.log(parsedQuizIds);
            for (const address of addresses) {
                console.log(address)
                let average = 0;
                for (const quizId in parsedQuizIds) {
                    const score = await contract.methods.getAverageScoreOfAddressOfQuiz(address, quizId).call();
                    const parsedScore = parseInt(score);
                    average += parsedScore;
                }
                average = average / parsedQuizIds.length
                setLeaderboard(prevLeaderBoard => [...prevLeaderBoard, {"address": address, "score": average}])
            }
                
            // console.log(leaderboard)
        } catch (error) {
            console.error(error)
        }
    }
    return (
        <div className="flex flex-col">
            <h2 className="text-3xl">LeaderBoard</h2>
            <ul className="flex flex-col">
                {leaderboard.map((leaderboard, index) => (
                <li key={index}>{leaderboard.address}: {leaderboard.score}</li>
                ))}
            </ul>
        </div>
    );
}
