"use client";

import { Button } from "@/components/ui/button";
import useStore from "@/hooks/useStore";
import Link from "next/link";
import { set } from "react-hook-form";
import Web3 from 'web3';

export default function Home() {
    const { login, logout, isLoggedIn, address } = useStore();

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

    return (
        <main className="flex min-h-screen flex-col items-center justify-center p-24">
            {!isLoggedIn ? (
                <Button onClick={connectWallet}>Login {address}</Button>
            ) : (
                <Button onClick={disconnectWallet}>Logout {address}</Button>
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