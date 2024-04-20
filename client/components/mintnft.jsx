"use client";

import dah from "../lib/abi.json";
import Web3 from "web3";
import { sendTransaction } from "@/web3/ethereum";
import useStore from "@/hooks/useStore";
import { Button } from "@/components/ui/button";
import { useState } from "react";

export function Mintnft() {
    const { address } = useStore();
    const web3 = new Web3(window.ethereum);
    const contract = new web3.eth.Contract(
        dah,
        "0xe8e9e68a61570ff81296543509722e2c5514025c"
    );
    const [feedback, setFeedback] = useState(""); // Initialize feedback state
    const handleSubmit = async () => {
        try {
            const method = contract.methods.mintCertificate();
            const txHash = await sendTransaction(method, contract, address);
            setFeedback("Certificate minted succesfully");
        } catch (error) {
            if (error instanceof Error) {
                const errorMessage = error.data.message.split(":")[1];
                console.log(errorMessage);
                setFeedback(errorMessage);
            } else {
                setFeedback("Failed to get certificate. Please try again!");
            }
        }
    };
    return (
        <div className="flex flex-col">
            <Button
                onClick={handleSubmit}
                variant="outline"
                type="submit"
                className="mt-6 "
            >
                Get Certificate
            </Button>
            <p>{feedback}</p>
            <a
                className="text-center underline"
                href="https://testnets.opensea.io/assets/amoy/0xe8e9e68a61570ff81296543509722e2c5514025c/1"
            >
                Check your nft
            </a>
        </div>
    );
}
