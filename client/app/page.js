"use client";

import { Button } from "@/components/ui/button";
import useStore from "@/hooks/useStore";
import Link from "next/link";
import { set } from "react-hook-form";

export default function Home() {
    const { isLoggedIn, setIsLoggedIn } = useStore();

    const connectWallet = async () => {
        if (typeof window.ethereum !== 'undefined') {
            try {
                const accounts = await window.ethereum.request({
                    method: 'eth_requestAccounts',
                })

                if (accounts.length === 0) {
                    console.log('No account connected')
                } else {
                    const web3 = new Web3(window.ethereum)
                    await setIsLoggedIn(true)
                }
            } catch (error) {
                console.error('Error connecting wallet:', error.message)
            }
        } else {
            console.log('Ethereum provider not found')
        }
    }

    const disconnectWallet = () => {
        setIsLoggedIn(false);
        store.commit("logout");
    }

    return (
        <main className="flex min-h-screen flex-col items-center justify-center p-24">
            {!isLoggedIn ? (
                <Button onClick={connectWallet}>Login</Button>
            ) : (
                <Button onClick={disconnectWallet}>Logout</Button>
            )}
            {/* <Button onClick={connectWallet}>Login</Button> */}
            <div className="mt-10">
                <Link href="/test-score" className="underline text-gray-400 hover:text-gray-700 underline-offset-4">
                    Test score
                </Link>
            </div>
        </main>
    );
}