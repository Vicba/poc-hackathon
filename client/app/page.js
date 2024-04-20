"use client";

import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function Home() {
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
            await accountStore.login()  
          }
        } catch (error) {
          console.error('Error connecting wallet:', error.message)
        }
      } else {
        console.log('Ethereum provider not found')
      }
    }

    const disconnectWallet = () => {
      accountStore.logout()
      store.commit("logout");
    }

    return (
        <main className="flex min-h-screen flex-col items-center justify-center p-24">
            {/* {!store.isLoggedIn?(
            <Button onClick={connectWallet}>Login</Button>
            ): (<Button onClick={disconnectWallet}>Logout</Button>)} */}
            <Button onClick={connectWallet}>Login</Button>
            <div className="mt-10">
                <Link href="/test-score" className="underline text-gray-400 hover:text-gray-700 underline-offset-4">
                    Test score
                </Link>
            </div>
        </main>
    );
}